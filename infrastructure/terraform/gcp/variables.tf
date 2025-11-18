variable "project_id" {
  description = "GCP Project ID"
  type        = string
}

variable "region" {
  description = "GCP Region"
  type        = string
  default     = "us-central1"
}

variable "zone" {
  description = "GCP Zone"
  type        = string
  default     = "us-central1-a"
}

variable "bucket_name" {
  description = "Cloud Storage bucket name for models and data"
  type        = string
}

variable "function_name" {
  description = "Cloud Function name"
  type        = string
  default     = "sentiment-endpoint"
}

variable "environment" {
  description = "Environment (dev, staging, prod)"
  type        = string
  default     = "dev"
}

