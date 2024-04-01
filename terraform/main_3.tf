# Description: Terraform example 3.
# Date: Sun. 2/18/24

# Resource: A resource is a single infrastructure object, such as a network, a server,
# an application, etc.

# Module: A module is a container for multiple resources that are used together. 

module "vpc" {
  source = "terraform-aws-modules/vpc/aws"
  name = "my-vpc"
  cidr = "10.0.0.0/16"
  azs = ["us-east-1a", "us-east-1b"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnets = ["10.0.101.0/24", "10.0.102.0/24"]
  enable_nat_gateway = true
  enable_vpn_gateway = true
}

module "ec2" {
  source = "terraform-aws-modules/ec2-instance/aws"
  name = "my-ec2-instance"
  instance_count = 1
  ami = "ami-0c94855ba95c574c8"
  instance_type = "t2.micro"
  subnet_id = module.vpc.private_subnets[0]
  vpc_security_group_ids = [aws_security_group.sg.id]
}

resource "aws_security_group" "sg" {
  name = "allow_ssh"
  vpc_id = module.vpc.vpc_id

  ingress {
    from_port = 22
    to_port = 22
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
