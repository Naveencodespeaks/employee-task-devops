# IAM module: least-privilege role for the EC2 app host.
#
# The instance needs to (a) pull images from ECR and (b) optionally use
# SSM Session Manager instead of SSH. It does NOT get broad AWS access --
# this is the "IAM least privilege" requirement from the design doc.

resource "aws_iam_role" "ec2_app_role" {
  name = "${var.project_name}-ec2-app-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "ec2.amazonaws.com" }
    }]
  })

  tags = { Name = "${var.project_name}-ec2-app-role" }
}

# Amazon-managed policy that grants read-only ECR pull permissions --
# enough to `docker pull` from our repositories, nothing more.
resource "aws_iam_role_policy_attachment" "ecr_read" {
  role       = aws_iam_role.ec2_app_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
}

# Lets you connect via `aws ssm start-session` instead of opening SSH
# to the internet -- recommended over the SSH security-group rule.
resource "aws_iam_role_policy_attachment" "ssm_managed_instance" {
  role       = aws_iam_role.ec2_app_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

resource "aws_iam_instance_profile" "ec2_app_profile" {
  name = "${var.project_name}-ec2-app-profile"
  role = aws_iam_role.ec2_app_role.name
}
