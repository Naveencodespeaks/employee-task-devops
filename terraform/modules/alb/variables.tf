variable "project_name" {
  type = string
}

variable "vpc_id" {
  type = string
}

variable "public_subnet_ids" {
  type = list(string)
}

variable "alb_security_group_id" {
  type = string
}

variable "instance_id" {
  type = string
}

variable "app_port" {
  type    = number
  default = 8000
}

variable "acm_certificate_arn" {
  description = "ARN of an ACM certificate for the app's domain. Create/validate this in AWS Certificate Manager first (see README HTTPS section)."
  type        = string
  default     = ""
}
