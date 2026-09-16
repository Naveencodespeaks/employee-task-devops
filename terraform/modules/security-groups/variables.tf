variable "project_name" {
  type = string
}

variable "vpc_id" {
  type = string
}

variable "app_port" {
  description = "Port the backend/frontend containers listen on behind the ALB"
  type        = number
  default     = 8000
}

variable "trusted_ssh_cidr" {
  description = "CIDR allowed to SSH into EC2 (your IP/32). Prefer AWS SSM Session Manager instead where possible."
  type        = string
  default     = "203.0.113.1/32" # placeholder -- replace with your real IP
}
