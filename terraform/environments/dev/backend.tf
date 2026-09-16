# Remote state: S3 stores the state file itself; DynamoDB provides
# state locking so two people (or two CI runs) can't apply at once and
# corrupt the state. Create the S3 bucket and DynamoDB table ONCE,
# manually or via a separate bootstrap config, before pointing this
# backend block at them (a backend block can't create its own backend).
#
#   aws s3api create-bucket --bucket employee-task-devops-tfstate --region ap-south-1
#   aws dynamodb create-table --table-name employee-task-devops-tflock \
#     --attribute-definitions AttributeName=LockID,AttributeType=S \
#     --key-schema AttributeName=LockID,KeyType=HASH \
#     --billing-mode PAY_PER_REQUEST
#
# Note: newer Terraform/AWS provider versions support S3-native locking
# (use_lockfile = true) as a DynamoDB-free alternative -- check the
# currently recommended approach in the Terraform AWS provider docs.
terraform {
  backend "s3" {
    bucket         = "employee-task-devops-tfstate"
    key            = "dev/terraform.tfstate"
    region         = "ap-south-1"
    dynamodb_table = "employee-task-devops-tflock"
    encrypt        = true
  }
}
