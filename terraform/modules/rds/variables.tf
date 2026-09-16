variable "project_name" {
  type = string
}

variable "private_subnet_ids" {
  type = list(string)
}

variable "rds_security_group_id" {
  type = string
}

variable "instance_class" {
  type    = string
  default = "db.t4g.micro"
}

variable "allocated_storage_gb" {
  type    = number
  default = 20
}

variable "db_name" {
  type    = string
  default = "employee_task_db"
}

variable "db_username" {
  type    = string
  default = "postgres"
}

variable "db_password" {
  description = "Master password for RDS. Provide via terraform.tfvars (gitignored) or -var, never commit it."
  type        = string
  sensitive   = true
}

variable "multi_az" {
  type    = bool
  default = false
}

variable "backup_retention_days" {
  type    = number
  default = 7
}

variable "skip_final_snapshot" {
  description = "true for learning/dev so `terraform destroy` doesn't hang waiting for a snapshot; set false in real prod"
  type        = bool
  default     = true
}
