# =============================================================================
# Cloud Run API
# =============================================================================

resource "google_project_service" "run" {
  project = data.google_project.current.project_id
  service = "run.googleapis.com"

  disable_on_destroy = false
}

# =============================================================================
# Cloud Run Service
# =============================================================================

resource "google_cloud_run_v2_service" "api" {
  name     = var.service_name
  location = "asia-northeast1"

  # NDCデータ(NDC8/NDC9)のオープンな検索APIとして公開している
  ingress = "INGRESS_TRAFFIC_ALL"

  # 2019年から稼働中の本番サービス。誤destroyを防ぐ
  deletion_protection = true

  template {
    service_account       = google_service_account.cloud_run.email
    execution_environment = "EXECUTION_ENVIRONMENT_GEN2"

    scaling {
      min_instance_count = var.cloud_run_min_instances
      max_instance_count = var.cloud_run_max_instances
    }

    max_instance_request_concurrency = var.cloud_run_concurrency

    labels = local.common_labels

    containers {
      image = var.cloud_run_image

      resources {
        limits = {
          cpu    = var.cloud_run_cpu
          memory = var.cloud_run_memory
        }
        cpu_idle          = var.cloud_run_min_instances == 0
        startup_cpu_boost = true
      }

      ports {
        container_port = 8080
      }
    }
  }

  traffic {
    type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
    percent = 100
  }

  labels = local.common_labels

  depends_on = [
    google_project_service.run,
  ]

  # deploy.bat の `gcloud run deploy --image ...` がイメージを直接差し替えるため、
  # image の差分は無視する（Terraformに戻されて古いイメージへ戻ることを防ぐ）
  lifecycle {
    ignore_changes = [
      client,
      client_version,
      template[0].containers[0].image,
    ]
  }
}

# =============================================================================
# 公開アクセス許可 (allUsers) — 既存の実運用と同じ設定を明示化
# =============================================================================

resource "google_cloud_run_v2_service_iam_member" "public_invoker" {
  project  = google_cloud_run_v2_service.api.project
  location = google_cloud_run_v2_service.api.location
  name     = google_cloud_run_v2_service.api.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}

# =============================================================================
# Outputs
# =============================================================================

output "cloud_run_service_name" {
  value       = google_cloud_run_v2_service.api.name
  description = "Cloud Run service name"
}

output "cloud_run_url" {
  value       = google_cloud_run_v2_service.api.uri
  description = "Cloud Run service default URL"
}
