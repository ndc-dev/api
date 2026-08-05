# =============================================================================
# Artifact Registry
#
# 現在の deploy.bat はレガシーな Container Registry (gcr.io) にpushしている。
# GCRは2025年に新規pushの受付を終了しており、Artifact Registryの薄いエイリアスとして
# 動いているだけの状態。将来 deploy.bat / Dockerfile のpush先をこちらへ切り替えるための
# リポジトリを先行して用意する（現状の稼働には影響しない。切り替えは別途対応）。
# =============================================================================

resource "google_project_service" "artifactregistry" {
  project = data.google_project.current.project_id
  service = "artifactregistry.googleapis.com"

  disable_on_destroy = false
}

resource "google_artifact_registry_repository" "api" {
  location      = "asia-northeast1"
  repository_id = var.service_name
  format        = "DOCKER"
  description   = "Container images for the ndc-dev/api Cloud Run service"

  labels = local.common_labels

  # 古いイメージの自動削除でストレージコスト抑制
  cleanup_policies {
    id     = "keep-recent-versions"
    action = "KEEP"
    most_recent_versions {
      keep_count = 5
    }
  }

  cleanup_policies {
    id     = "delete-old-untagged"
    action = "DELETE"
    condition {
      tag_state  = "UNTAGGED"
      older_than = "86400s" # 1日
    }
  }

  depends_on = [google_project_service.artifactregistry]
}

output "artifact_registry_url" {
  value       = "${google_artifact_registry_repository.api.location}-docker.pkg.dev/${data.google_project.current.project_id}/${google_artifact_registry_repository.api.repository_id}"
  description = "Artifact Registry repository URL for future docker push/pull (未使用・移行用に先行作成)"
}
