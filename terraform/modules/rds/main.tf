# RDS module: managed PostgreSQL in the private subnets.
#
# db_subnet_group spans both private subnets (RDS requires >= 2 AZs
# even for a single instance, so it can fail over into a Multi-AZ
# setup later without re-architecting the network).

resource "aws_db_subnet_group" "postgres" {
  name       = "${var.project_name}-db-subnet-group"
  subnet_ids = var.private_subnet_ids

  tags = { Name = "${var.project_name}-db-subnet-group" }
}

resource "aws_db_instance" "postgres" {
  identifier     = "${var.project_name}-db"
  engine         = "postgres"
  engine_version = "16"
  instance_class = var.instance_class

  allocated_storage = var.allocated_storage_gb
  storage_type      = "gp3"

  db_name  = var.db_name
  username = var.db_username
  password = var.db_password # pass via -var, tfvars (gitignored), or a secrets manager -- never hardcode

  db_subnet_group_name   = aws_db_subnet_group.postgres.name
  vpc_security_group_ids = [var.rds_security_group_id]

  publicly_accessible = false
  multi_az             = var.multi_az

  backup_retention_period = var.backup_retention_days
  skip_final_snapshot     = var.skip_final_snapshot

  tags = { Name = "${var.project_name}-db" }
}
