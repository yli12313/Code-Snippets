# Description: Terraform example 4.
# Date: Mon. 2/19/24

module "db" {
  source  = "terraform-aws-modules/rds/aws"
  version = "~> 2.0"

  identifier = "demodb"

  engine            = "mysql"
  engine_version    = "5.7"
  instance_class    = "db.t2.micro"
  allocated_storage = 20

  name     = "mydb"
  username = "foo"
  password = "foobarbaz"
  port     = "3306"

  vpc_security_group_ids = [aws_security_group.db_sg.id]
  subnet_ids             = aws_subnet.db_subnet.*.id

  multi_az = false

  storage_encrypted = true
  kms_key_id        = aws_kms_key.db.arn

  skip_final_snapshot = true
}

resource "aws_security_group" "db_sg" {
  name = "db_sg"
  description = "Allow inbound traffic"
  vpc_id = var.vpc_id

  ingress {
    from_port   = 3306
    to_port     = 3306
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_subnet" "db_subnet" {
  count                   = 2
  vpc_id                  = var.vpc_id
  cidr_block              = count.index == 0 ? "10.0.1.0/24" : "10.0.2.0/24"
  availability_zone       = count.index == 0 ? "us-west-2a" : "us-west-2b"
  map_public_ip_on_launch = true
}

resource "aws_kms_key" "db" {
  description = "KMS key for RDS DB"
}
