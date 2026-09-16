# EC2 module: a single application host running Docker Compose.
#
# This is the "beginner-friendly first AWS deployment" from the design
# doc -- one instance running docker-compose, sitting in a public
# subnet, behind the ALB. Later phases replace this with ECS/EKS.

data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-*-x86_64"]
  }
}

resource "aws_instance" "app" {
  ami                    = data.aws_ami.amazon_linux.id
  instance_type          = var.instance_type
  subnet_id              = var.public_subnet_id
  vpc_security_group_ids = [var.security_group_id]
  iam_instance_profile   = var.instance_profile_name
  key_name               = var.key_pair_name

  # Installs Docker + Docker Compose plugin and enables the service on
  # first boot. Application deployment itself is handled by
  # Jenkins/GitHub Actions via SSH afterwards, not by this script.
  user_data = <<-EOF
    #!/bin/bash
    dnf update -y
    dnf install -y docker
    systemctl enable docker
    systemctl start docker
    mkdir -p /usr/local/lib/docker/cli-plugins
    curl -SL https://github.com/docker/compose/releases/latest/download/docker-compose-linux-x86_64 \
      -o /usr/local/lib/docker/cli-plugins/docker-compose
    chmod +x /usr/local/lib/docker/cli-plugins/docker-compose
    usermod -aG docker ec2-user
    mkdir -p /opt/employee-task-devops
  EOF

  tags = {
    Name = "${var.project_name}-app-host"
  }
}
