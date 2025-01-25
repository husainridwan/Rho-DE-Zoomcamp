# Rho-DE-Zoomcamp

This repository contains the work done for my Data Engineering Zoomcamp. 

## Table of Contents

- [Setup](#setup)
- [Ingesting Data](#ingesting-data)
- [Database Management with pgAdmin](#database-management-with-pgadmin)
- [Scripts](#scripts)
- [Docker Compose](#docker-compose)
- [AWS Setup with Terraform](#Terraform)

## Setup

### PostgreSQL Database

To set up the PostgreSQL database, check the #setup.yml file:

### pgAdmin

To set up pgAdmin for database management, check the #setup.yml file:

### Ingesting Data

To ingest data into the PostgreSQL database, check the #setup.yml file:

### Database Management with pgAdmin

Access pgAdmin by navigating to http://localhost:8080 in your web browser. Use the following credentials to log in:
Email: admin@admin.com
Password: root

### Scripts

- ingestData.py
This script downloads a CSV file, unzips it, and ingests the data into the PostgreSQL database in chunks.

- uploadata.ipynb
This Jupyter Notebook contains code for data analysis and manipulation using pandas and numpy.

- Docker Compose
You can use Docker Compose to manage the services. Check the docker-compose.yml file:

### AWS Setup with Terraform

#### Prerequisites
- Install Terraform: [Terraform Installation Guide](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli)
- Configure AWS CLI with your credentials: [AWS CLI Configuration](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-quickstart.html)

#### Terraform Configuration
- Initialize Terraform: terraform init
- Apply the Configuration: terraform apply
  - Review the plan and confirm the apply by typing yes.

#### Terraform Resources
The Terraform configuration includes the following resources:

- S3 Bucket: Creates an S3 bucket with versioning and lifecycle rules.
- Redshift Cluster: Creates a Redshift cluster within the database.

- Example main.tf Configuration
You can find the example main.tf configuration here.

- Variables Definition
Define the necessary variables in variables.tf:

- Providing Variable Values
Provide the values for the variables using a terraform.tfvars file or environment variables.
