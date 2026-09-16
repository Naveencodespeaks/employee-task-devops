output "alb_dns_name" {
  value = module.alb.alb_dns_name
}

output "ec2_public_ip" {
  value = module.ec2.public_ip
}

output "rds_endpoint" {
  value = module.rds.endpoint
}

output "backend_ecr_repo_url" {
  value = module.ecr.backend_repository_url
}

output "frontend_ecr_repo_url" {
  value = module.ecr.frontend_repository_url
}
