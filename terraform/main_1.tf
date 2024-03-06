# Description: Terraform example 1.
# Date: Fri. 2/16/24

# 'provider' block:
# - Configures the AWS provider and sets the region.
provider "aws" {
    region = "us-west-2"
}

# 'aws_instance' resource:
# - Creates EC2 instance with specific ami and instance type.
# - Assigns tags and a security group.
resource "aws_instance" "example" {
    ami = "ami-0c94855ba95c574c8"
    instance_type = "t2.micro"

    tags = {
        Name = "example-instance"
    }

    vpc_security_group_ids = [aws_security_group.example.id]
}

# 'aws_security_group' resource:
# - Creates a security group with specific ingress and egress rules.
resource "aws_security_group" "example" {
    # Caveat: This is the name of the security group as it will appear
    # in AWS once it's created.
    name = "example"
    description = "Example security group"

    ingress {
        from_port = 22
        to_port = 22
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    egress {
        from_port = 0
        to_port = 0
        protocol = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }
}