# Terraform configuration for GCP ML Pipeline Infrastructure

terraform {
  required_version = ">= 1.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }

  backend "gcs" {
    bucket = "ml-pipeline-terraform-state"
    prefix = "terraform/state"
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# Cloud Storage Bucket for models and data
resource "google_storage_bucket" "ml_pipeline_bucket" {
  name          = var.bucket_name
  location      = var.region
  force_destroy = false

  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }

  lifecycle_rule {
    condition {
      age = 30
    }
    action {
      type = "Delete"
    }
  }
}

# Pub/Sub Topic for streaming data
resource "google_pubsub_topic" "twitter_stream" {
  name = "twitter-stream"
}

# Pub/Sub Subscription
resource "google_pubsub_subscription" "twitter_stream_sub" {
  name  = "twitter-stream-subscription"
  topic = google_pubsub_topic.twitter_stream.name

  ack_deadline_seconds = 20

  expiration_policy {
    ttl = "300000.5s"
  }

  retry_policy {
    minimum_backoff = "10s"
  }
}

# Service Account for Cloud Functions
resource "google_service_account" "cloud_function_sa" {
  account_id   = "ml-pipeline-function-sa"
  display_name = "ML Pipeline Cloud Function Service Account"
}

# IAM role for Cloud Function
resource "google_project_iam_member" "cloud_function_storage" {
  project = var.project_id
  role    = "roles/storage.objectViewer"
  member  = "serviceAccount:${google_service_account.cloud_function_sa.email}"
}

# Cloud Function for sentiment prediction
resource "google_cloudfunctions_function" "sentiment_endpoint" {
  name        = var.function_name
  description = "ML Pipeline Sentiment Analysis Endpoint"
  runtime     = "python39"
  region      = var.region

  available_memory_mb   = 2048
  source_archive_bucket = google_storage_bucket.ml_pipeline_bucket.name
  source_archive_object = "functions/sentiment-endpoint.zip"
  timeout               = 540
  entry_point           = "gcp_sentiment_endpoint"

  service_account_email = google_service_account.cloud_function_sa.email

  environment_variables = {
    MODEL_PATH = "gs://${var.bucket_name}/models/sentiment_model"
    PROJECT_ID = var.project_id
  }

  # HTTP trigger (Gen 1)
  https_trigger_url = null
}

# IAM policy for Cloud Function (public access)
resource "google_cloudfunctions_function_iam_member" "invoker" {
  cloud_function = google_cloudfunctions_function.sentiment_endpoint.name
  role           = "roles/cloudfunctions.invoker"
  member         = "allUsers"
}

# Dataflow Job Template (for Spark Streaming)
resource "google_dataflow_job" "spark_streaming" {
  name              = "sentiment-analysis-streaming"
  template_gcs_path = "gs://dataflow-templates/latest/Word_Count"
  temp_gcs_location = "gs://${var.bucket_name}/temp"
  parameters = {
    inputTopic = google_pubsub_topic.twitter_stream.id
  }
  region = var.region
}

# Vertex AI Dataset (optional)
resource "google_vertex_ai_dataset" "training_data" {
  display_name        = "sentiment-training-data"
  metadata_schema_uri = "gs://google-cloud-aiplatform/schema/dataset/metadata/tabular_1.0.0.yaml"
  region              = var.region
}

