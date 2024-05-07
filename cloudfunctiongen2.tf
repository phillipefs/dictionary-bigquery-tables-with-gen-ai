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

resource "google_cloudfunctions_function_iam_member" "invoker" {
  project        = google_cloudfunctions2_function.default.project
  region         = google_cloudfunctions2_function.default.location
  cloud_function = google_cloudfunctions2_function.default.name

  role   = "roles/cloudfunctions.invoker"
  member = "allUsers"
}

# data "google_iam_policy" "invoker" {
#   binding {
#     role = "roles/run.invoker"
#     members = [
#       "allUsers",
#     ]
#   }
# }

# resource "google_cloudfunctions2_function_iam_policy" "invoker" {
#   location    = google_cloudfunctions2_function.default.location
#   cloud_function = google_cloudfunctions2_function.default.name
#   policy_data = data.google_iam_policy.invoker.policy_data
# }

# data "google_iam_policy" "admin" {
#   binding {
#     role = "roles/run.invoker"
#     members = [
#       "allUsers",
#     ]
#   }
# }

# resource "google_cloud_run_service_iam_policy" "policy" {
#   location = google_cloudfunctions2_function.default.location
#   project = "datapipelines-419810"
#   service = google_cloudfunctions2_function.default.name
#   policy_data = data.google_iam_policy.admin.policy_data

#   depends_on = [
#     google_cloudfunctions2_function.default
#   ]
# }