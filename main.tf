module "bigquery-dataset-jp-steamdb" {
  source  = "./modules/bigquery"
  dataset_id                  = "steamdb_sales"
  dataset_name                = "steamdb_sales"
  description                 = "Dataset de vendas da SteamDB"
  project_id                  = var.project_id
  location                    = var.region
  delete_contents_on_destroy  = true
  deletion_protection = false
  access = [
    {
      role = "OWNER"
      special_group = "projectOwners"
    },
    {
      role = "READER"
      special_group = "projectReaders"
    },
    {
      role = "WRITER"
      special_group = "projectWriters"
    }
  ]
  tables=[
    {
        table_id           = "tb_steamdb_sales",
        description        = "vendas da SteamDB"
        time_partitioning  = {
          type                     = "DAY",
          field                    = "data",
          require_partition_filter = false,
          expiration_ms            = null
        },
        range_partitioning = null,
        expiration_time = null,
        clustering      = ["name","Started", "Release"],
        labels          = {
          name    = "data_pipeline"
          project  = "steamdb_sales"
        },
        deletion_protection = true
        schema = file("./bigquery/schema/steamdb-sales/tb_steamdb_sales.json")
    }
  ]
}

module "bucket-raw" {
  source  = "./modules/gcs"

  name       = "data-pipeline-jp-steamdb-raw"
  project_id = var.project_id
  location   = var.region
}

module "bucket-curated" {
  source  = "./modules/gcs"

  name       = "data-pipeline-jp-steamdb-curated"
  project_id = var.project_id
  location   = var.region
}

module "bucket-pyspark-tmp" {
  source  = "./modules/gcs"

  name       = "data-pipeline-jp-steamdb-pyspark-tmp"
  project_id = var.project_id
  location   = var.region
}

module "bucket-pyspark-code" {
  source = "./modules/gcs"

  name       = "data-pipeline-jp-steamdb-pyspark-code"
  project_id = var.project_id
  location   = var.region
}