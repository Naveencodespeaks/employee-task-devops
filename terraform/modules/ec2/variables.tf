variable "project_name" {
  type = string
}

variable "instance_type" {
  type    = string
  default = "t3.micro"
}

variable "public_subnet_id" {
  type = string
}

variable "security_group_id" {
  type = string
}

variable "instance_profile_name" {
  type = string
}

variable "key_pair_name" {
  description = "Existing EC2 key pair name for SSH access (leave blank to rely on SSM only)"
  type        = string
  default     = ""
}
