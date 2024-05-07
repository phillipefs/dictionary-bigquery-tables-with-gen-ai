resource "google_storage_bucket" "static" {
 name          = "data-dictionary-bigquery"
 location      = "us-central1"
 storage_class = "STANDARD"

 uniform_bucket_level_access = true
}

resource "google_storage_bucket" "c_function" {
  name          = "c-functions-data-pipelines"
  location      = "us-central1"
  storage_class = "STANDARD"
  uniform_bucket_level_access = true
}