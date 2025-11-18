output "bucket_name" {
  description = "Cloud Storage bucket name"
  value       = google_storage_bucket.ml_pipeline_bucket.name
}

output "bucket_url" {
  description = "Cloud Storage bucket URL"
  value       = "gs://${google_storage_bucket.ml_pipeline_bucket.name}"
}

output "function_url" {
  description = "Cloud Function URL"
  value       = google_cloudfunctions_function.sentiment_endpoint.https_trigger_url
}

output "function_name" {
  description = "Cloud Function name"
  value       = google_cloudfunctions_function.sentiment_endpoint.name
}

output "pubsub_topic" {
  description = "Pub/Sub topic name"
  value       = google_pubsub_topic.twitter_stream.name
}

output "pubsub_subscription" {
  description = "Pub/Sub subscription name"
  value       = google_pubsub_subscription.twitter_stream_sub.name
}

output "service_account_email" {
  description = "Service account email for Cloud Functions"
  value       = google_service_account.cloud_function_sa.email
}

