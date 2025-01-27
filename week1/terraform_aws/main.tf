resource "aws_s3_bucket" "rho_ny_taxi_bucket" {
  bucket = var.s3_bucket_name

  tags = {
    Name        = "NY Taxi Data Bucket"
    Environment = "Dev"
  }
}
# Enable versioning
resource "aws_s3_bucket_versioning" "rho_ny_taxi_bucket_versioning" {
  bucket = aws_s3_bucket.rho_ny_taxi_bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}

# Lifecycle configuration
resource "aws_s3_bucket_lifecycle_configuration" "rho_ny_taxi_lifecycle" {
  bucket = aws_s3_bucket.rho_ny_taxi_bucket.id
  rule {
    id     = "NY Taxi Data Expiration Rule"
    status = "Enabled"

    expiration {
      days = 30
    }
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "encryption" {
  bucket = aws_s3_bucket.rho_ny_taxi_bucket.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "block_public" {
  bucket                  = aws_s3_bucket.rho_ny_taxi_bucket.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_redshift_cluster" "rho_ny_taxi_redshift" {
  cluster_identifier  = "rho-ny-taxi-redshift"
  node_type           = "dc2.large"
  cluster_type        = "single-node"
  master_username     = var.master_username
  master_password     = var.master_password
  database_name       = var.db_name
  skip_final_snapshot = true

  tags = {
    Name        = "NY Taxi Redshift Cluster"
    Environment = "Dev"
  }
}