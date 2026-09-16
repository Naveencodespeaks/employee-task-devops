terraform {
  required_version = ">= 1.7"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

module "vpc" {
  source       = "../../modules/vpc"
  project_name = var.project_name
}

module "security_groups" {
  source           = "../../modules/security-groups"
  project_name     = var.project_name
  vpc_id           = module.vpc.vpc_id
  app_port         = var.app_port
  trusted_ssh_cidr = var.trusted_ssh_cidr
}

module "ecr" {
  source       = "../../modules/ecr"
  project_name = var.project_name
}

module "iam" {
  source       = "../../modules/iam"
  project_name = var.project_name
}

module "ec2" {
  source                 = "../../modules/ec2"
  project_name           = var.project_name
  public_subnet_id       = module.vpc.public_subnet_ids[0]
  security_group_id      = module.security_groups.ec2_sg_id
  instance_profile_name  = module.iam.instance_profile_name
  key_pair_name          = var.key_pair_name
}

module "rds" {
  source                = "../../modules/rds"
  project_name          = var.project_name
  private_subnet_ids    = module.vpc.private_subnet_ids
  rds_security_group_id = module.security_groups.rds_sg_id
  db_password            = var.db_password
}

module "alb" {
  source                 = "../../modules/alb"
  project_name           = var.project_name
  vpc_id                 = module.vpc.vpc_id
  public_subnet_ids      = module.vpc.public_subnet_ids
  alb_security_group_id  = module.security_groups.alb_sg_id
  instance_id            = module.ec2.instance_id
  app_port               = var.app_port
  acm_certificate_arn    = var.acm_certificate_arn
}
