data "archive_file" "source" {
  type        = "zip"
  source_dir  = "${path.module}/cloud_function"
  output_path = "${path.module}/tmp/function.zip"
}

# Add source code zip to the Cloud Function's bucket (Cloud_function_bucket) 
resource "google_storage_bucket_object" "zip" {
  source       = data.archive_file.source.output_path
  content_type = "application/zip"
  name         = "src-${data.archive_file.source.output_md5}.zip"
  bucket       = "c-functions-data-pipelines"
  depends_on = [
    data.archive_file.source
  ]
}

resource "google_cloudfunctions2_function" "default" {
  name = "data-dictionary-bigquery"
  location = var.region
  description = "Data Dictionary with GenAI"

  build_config {
    runtime     = "python39"
    entry_point = "hello_get" 
    environment_variables = {
      BUILD_CONFIG_TEST = "build_test"
    }
    source {
      storage_source {
        bucket = "c-functions-data-pipelines"
        object = google_storage_bucket_object.zip.name
      }
    }
  }

  service_config {
    max_instance_count  = 3
    min_instance_count = 1
    available_memory    = "256M"
    timeout_seconds     = 60
    environment_variables = {
        SERVICE_CONFIG_TEST = "config_test"
    }
    ingress_settings = "ALLOW_ALL"
    all_traffic_on_latest_revision = true
    service_account_email = "datapipeline@datapipelines-419810.iam.gserviceaccount.com"
  }

  depends_on = [
    google_storage_bucket_object.zip
  ]
}

resource "google_cloud_run_service_iam_binding" "default" {
  location = google_cloudfunctions2_function.default.location
  service  = google_cloudfunctions2_function.default.name
  role     = "roles/run.invoker"
  members = [
    "allUsers"
  ]
}