# main.tf
terraform {
  required_providers {
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "~> 5.4.0"
    }
  }
  required_version = ">= 1.0.0"
}

# Provider configurations
provider "cloudflare" {
  api_token = var.cloudflare_deployment_api_token
}

# Get the Cloudflare zone for the domain
data "cloudflare_zone" "domain_zone" {
  zone_id = var.cloudflare_zone_id
}

# The build script creates a data source containing the script source code compiled from TypeScript into Javascript, encoded as base64 and wrapped into a JSON object required by Terraform for data sources.
# I found this approach of using a data source more elegant/terraform-native than using a null resource or pre-compiling the script before running Terraform.
data "external" "worker_script" {
  program = ["${path.module}/worker/build.sh", "${path.module}/worker"]
}

# We then need to unwrap the base64 encoded string and decode it so we can use it below in the worker configuration.
locals {
  worker_script_content = base64decode(data.external.worker_script.result.content)
}

# Create Cloudflare R2 bucket
resource "cloudflare_r2_bucket" "website_bucket" {
  account_id    = var.cloudflare_account_id
  name          = var.bucket_name
  location      = var.bucket_location
  jurisdiction  = "default"
  storage_class = "Standard"
}

# Create Cloudflare Worker script
resource "cloudflare_workers_script" "r2_website_worker" {
  script_name        = "${var.bucket_name}-worker"
  account_id         = var.cloudflare_account_id
  content            = local.worker_script_content
  compatibility_date = var.worker_compatibility_date
  main_module        = "worker.js"

}

# Create a Worker route to associate the worker with a hostname pattern
resource "cloudflare_workers_route" "r2_website_route" {
  zone_id = data.cloudflare_zone.domain_zone.zone_id
  pattern = var.subdomain == "@" ? "${var.domain_name}/*" : "${var.subdomain}.${var.domain_name}/*"
  script  = cloudflare_workers_script.r2_website_worker.script_name
}

# The custom domain exposes our S3 bucket through the CloudFlare CDN, with a nice DNS name.
resource "cloudflare_r2_custom_domain" "custom_domain" {
  account_id  = var.cloudflare_account_id
  bucket_name = cloudflare_r2_bucket.website_bucket.name
  domain      = var.subdomain == "@" ? "${var.domain_name}/*" : "${var.subdomain}.${var.domain_name}"
  enabled     = true
  zone_id     = data.cloudflare_zone.domain_zone.zone_id
  min_tls     = "1.0"
}
