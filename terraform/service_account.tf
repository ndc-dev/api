# =============================================================================
# Cloud Run 専用サービスアカウント
#
# それまでサービスアカウント未指定で、デフォルトのCompute Engineサービスアカウント
# （プロジェクトに roles/editor を持つ）で動いていた。main.py はNDCデータを
# 起動時にコンテナ内のzipから読むだけで、GCP APIを一切呼ばないアプリケーションなので、
# 本来必要な権限はゼロ。プロジェクトIAMロールは意図的に何も付与していない。
# 将来アプリがGCP APIを呼ぶようになった場合は、そのAPIに必要な最小権限だけを追加すること。
#
# Cloud Run基盤自体のログ・メトリクス収集（Cloud Logging/Monitoringへの標準出力の
# 取り込みや稼働メトリクス）はプラットフォーム側の機能で、このSAのIAMロールとは無関係に動く。
# =============================================================================

resource "google_service_account" "cloud_run" {
  account_id   = "${var.service_name}-run"
  display_name = "api Cloud Run runtime"
  description  = "Runtime service account for the ndc-dev/api Cloud Run service. No project IAM roles granted (app calls no GCP APIs)."
}

output "cloud_run_service_account_email" {
  value       = google_service_account.cloud_run.email
  description = "Cloud Run runtime service account email"
}
