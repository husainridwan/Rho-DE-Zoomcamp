variable "master_username" {
  description = "The master username for the Redshift cluster"
  type        = string
}

variable "master_password" {
  description = "The master password for the Redshift cluster"
  type        = string
  sensitive   = false
}

variable "aws_region" {
  description = "The AWS region to deploy resources"
  type        = string
}

variable "s3_bucket_name" {
  description = "Amazon S3 bucket"
  type        = string
}

variable "db_name" {
  description = "The name of the Redshift database"
  type        = string
}