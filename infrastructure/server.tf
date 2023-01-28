resource "aws_subnet" "myapp-subnet-1" {
  vpc_id            = aws_vpc.myapp-vpc.id
  cidr_block        = var.subnet_cidr_block
  availability_zone = var.avail_zone
  tags = {
    Name = "${var.env_prefix}-subnet-1"
  }
}

resource "aws_default_security_group" "default-sg" {

  vpc_id = aws_vpc.myapp-vpc.id

  # Incoming
  ingress {

    from_port = 22
    # We can make this 1000 to have ports 22 -> 1000 all open
    to_port = 22

    protocol = "tcp"

    # range of ip addresses that can access through these ports. /32 means we have only one address.

    cidr_blocks = ["0.0.0.0/0"]
  }

  # Incoming 2 - Allow access to anyone into web server
  ingress {

    from_port = 80
    to_port   = 80

    protocol = "tcp"

    # range of ip addresses that can access through these ports. /32 means we have only one address.

    cidr_blocks = ["0.0.0.0/0"]
  }

  # Incoming 3 - Allow access to anyone into web server ( VIA TLS )
  ingress {

    from_port = 443
    to_port   = 443

    protocol = "tcp"

    # range of ip addresses that can access through these ports. /32 means we have only one address.

    cidr_blocks = ["0.0.0.0/0"]
  }

  # Outgoing
  egress {
    from_port       = 0
    to_port         = 0
    protocol        = "-1"
    cidr_blocks     = ["0.0.0.0/0"]
    prefix_list_ids = []
  }

  tags = {
    Name = "${var.env_prefix}-default-sg"
  }
}

data "aws_ami" "latest-amazon-linux-image" {
  most_recent = true
  # owner can be amazon, community, .... we get it from the AMI list on the gui AWS
  owners = ["amazon"]
  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }
  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

resource "aws_instance" "myapp-server" {
  ami           = data.aws_ami.latest-amazon-linux-image.id
  instance_type = var.instance_type

  subnet_id              = aws_subnet.myapp-subnet-1.id
  vpc_security_group_ids = [aws_default_security_group.default-sg.id]
  availability_zone      = var.avail_zone

  associate_public_ip_address = true
  key_name                    = aws_key_pair.ssh-key.key_name

  user_data = file("entry-script.sh")
  tags = {
    Name = "${var.env_prefix}-server"
  }
}
