# ECR module: one repository per image (frontend, backend).
#
# Immutable tags matter here: with mutable tags, redeploying "latest"
# doesn't tell you WHICH commit is actually running, and a bad push can
# silently overwrite a known-good image. Immutable tags force every
# build to get a unique tag (e.g. the Jenkins BUILD_NUMBER or git SHA),
# so you can always trace a running container back to an exact commit,
# and roll back deterministically.

resource "aws_ecr_repository" "backend" {
  name                 = "${var.project_name}-backend"
  image_tag_mutability = "IMMUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = { Name = "${var.project_name}-backend" }
}

resource "aws_ecr_repository" "frontend" {
  name                 = "${var.project_name}-frontend"
  image_tag_mutability = "IMMUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = { Name = "${var.project_name}-frontend" }
}

# Keep only the last N images per repo to control storage cost.
locals {
  keep_recent_policy = jsonencode({
    rules = [
      {
        rulePriority = 1
        description  = "Keep only the last 10 images"
        selection = {
          tagStatus   = "any"
          countType   = "imageCountMoreThan"
          countNumber = 10
        }
        action = {
          type = "expire"
        }
      }
    ]
  })
}

resource "aws_ecr_lifecycle_policy" "backend" {
  repository = aws_ecr_repository.backend.name
  policy     = local.keep_recent_policy
}

resource "aws_ecr_lifecycle_policy" "frontend" {
  repository = aws_ecr_repository.frontend.name
  policy     = local.keep_recent_policy
}
