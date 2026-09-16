variable "project_name" {
  type    = string
  default = "employee-task-prod"
}

variable "aws_region" {
  type    = string
  default = "ap-south-1"
}

variable "app_port" {
  type    = number
  default = 8000
}

variable "trusted_ssh_cidr" {
  description = "Your IP in CIDR form, e.g. 203.0.113.5/32. Prefer SSM Session Manager and skip SSH entirely where possible."
  type        = string
}

variable "key_pair_name" {
  description = "Existing EC2 key pair name (leave blank to rely on SSM only)"
  type        = string
  default     = ""
}

variable "db_password" {
  description = "RDS master password -- set via terraform.tfvars (gitignored) or TF_VAR_db_password env var"
  type        = string
  sensitive   = true
}

variable "acm_certificate_arn" {
  description = "ACM certificate ARN for your domain (created/validated outside Terraform, or add an aws_acm_certificate resource here once you own a real domain)"
  type        = string
  default     = ""
}
