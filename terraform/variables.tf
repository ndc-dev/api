variable "service_name" {
  type        = string
  default     = "api"
  description = "Cloud Run service name"
}

# =============================================================================
# Cloud Run リソース設定
# =============================================================================

variable "cloud_run_image" {
  type        = string
  default     = "asia-northeast1-docker.pkg.dev/ndc-dev-255301/api/api:latest"
  description = "Container image。gcr.io は完全に廃止され読み取りもできない状態だったため Artifact Registry に移行した。deploy.bat が gcloud run deploy でイメージだけ差し替えるため、実体は lifecycle.ignore_changes で無視する。"
}

variable "cloud_run_cpu" {
  type        = string
  default     = "1"
  description = "vCPU per instance"
}

variable "cloud_run_memory" {
  type        = string
  default     = "512Mi"
  description = "Memory per instance"
}

variable "cloud_run_min_instances" {
  type        = number
  default     = 0
  description = "Minimum instance count. 低トラフィックの開発者向けAPIなのでゼロスケールを許容する。"
}

variable "cloud_run_max_instances" {
  type        = number
  default     = 2
  description = "Maximum instance count（暴走コスト防止の安全弁）"
}

variable "cloud_run_concurrency" {
  type        = number
  default     = 80
  description = "Max concurrent requests per instance"
}
