# configure AWS provider with region and profile
provider "aws" {
  region  = var.aws_region
  profile = "fred"
}

# Get your public IP dynamically
data "http" "myip" {
  url = "https://checkip.amazonaws.com/"
}

# create a VPC
resource "aws_vpc" "test_vpc" {
  cidr_block = "10.0.0.0/16"

  tags = {
    Name = "api_vpc"
  }

  enable_dns_hostnames = true
  enable_dns_support   = true
}

# create a public subnet
resource "aws_subnet" "public_subnet" {
  vpc_id                  = aws_vpc.test_vpc.id
  cidr_block              = "10.0.0.0/24"
  availability_zone       = var.aws_availability_zone
  map_public_ip_on_launch = true

  tags = {
    Name = "public-subnet"
  }
}

# create a private subnet
resource "aws_subnet" "private_subnet" {
  vpc_id            = aws_vpc.test_vpc.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = var.aws_availability_zone

  tags = {
    Name = "private-subnet"
  }
}

# create an internet gateway
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.test_vpc.id

  tags = {
    Name = "test-igw"
  }
}

# create route tables
resource "aws_route_table" "public_route" {
  vpc_id = aws_vpc.test_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }

  tags = {
    Name = "public-rt"
  }
}

resource "aws_route_table" "private_route" {
  vpc_id = aws_vpc.test_vpc.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.nat.id
  }

  tags = {
    Name = "private-rt"
  }
}

# route table association
resource "aws_route_table_association" "public" {
  subnet_id      = aws_subnet.public_subnet.id
  route_table_id = aws_route_table.public_route.id
}

resource "aws_route_table_association" "private" {
  subnet_id      = aws_subnet.private_subnet.id
  route_table_id = aws_route_table.private_route.id
}

# allocate elastic ip to nat gateway
resource "aws_eip" "nat_eip" {
  domain = "vpc"

  tags = {
    Name = "nat-eip"
  }
}

# create a NAT gateway
resource "aws_nat_gateway" "nat" {
  allocation_id = aws_eip.nat_eip.id
  subnet_id     = aws_subnet.public_subnet.id

  tags = {
    Name = "nat-gw"
  }

  depends_on = [aws_internet_gateway.igw]
}

# create web server security group
resource "aws_security_group" "webserver" {
  name        = "webserversg"
  description = "security group for webservers"
  vpc_id      = aws_vpc.test_vpc.id
  tags = {
    Name = "WebServerSG"
  }
}

# allow ssh, http, and https traffic to webserver
resource "aws_vpc_security_group_ingress_rule" "allow_ssh_webserver" {
  security_group_id = aws_security_group.webserver.id
  cidr_ipv4         = "${chomp(data.http.myip.response_body)}/32"
  from_port         = 22
  ip_protocol       = "tcp"
  to_port           = 22
}

resource "aws_vpc_security_group_ingress_rule" "allow_http" {
  security_group_id = aws_security_group.webserver.id
  cidr_ipv4         = "0.0.0.0/0"
  from_port         = 80
  ip_protocol       = "tcp"
  to_port           = 80
}

resource "aws_vpc_security_group_ingress_rule" "allow_https" {
  security_group_id = aws_security_group.webserver.id
  cidr_ipv6         = "::/0"
  from_port         = 443
  ip_protocol       = "tcp"
  to_port           = 443
}

# adding egress rules for all traffic
resource "aws_vpc_security_group_egress_rule" "allow_all_traffic_webserver" {
  security_group_id = aws_security_group.webserver.id
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "-1"
}

# create database server security group
resource "aws_security_group" "dbserver" {
  name        = "dbserversg"
  description = "security group for database servers"
  vpc_id      = aws_vpc.test_vpc.id
  tags = {
    Name = "DBServerSG"
  }
}

# allow ssh, and Postgres traffic to dbserver from instances in the webserver
resource "aws_vpc_security_group_ingress_rule" "allow_ssh_db" {
  security_group_id            = aws_security_group.dbserver.id
  referenced_security_group_id = aws_security_group.webserver.id
  from_port                    = 22
  ip_protocol                  = "tcp"
  to_port                      = 22
}

resource "aws_vpc_security_group_ingress_rule" "allow_postgres" {
  security_group_id            = aws_security_group.dbserver.id
  referenced_security_group_id = aws_security_group.webserver.id
  from_port                    = 5432
  ip_protocol                  = "tcp"
  to_port                      = 5432
}

# adding egress rules for all traffic
resource "aws_vpc_security_group_egress_rule" "allow_all_traffic_db" {
  security_group_id = aws_security_group.dbserver.id
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "-1"
}

# create an EC2 instance
data "aws_ssm_parameter" "ubuntu_ami" {
  name = "/aws/service/canonical/ubuntu/server/24.04/stable/current/amd64/hvm/ebs-gp3/ami-id"
}

# webserver instance
resource "aws_instance" "web_instance" {
  ami                         = data.aws_ssm_parameter.ubuntu_ami.value
  instance_type               = "t3.micro"
  key_name                    = "fredssh"
  vpc_security_group_ids      = [aws_security_group.webserver.id]
  subnet_id                   = aws_subnet.public_subnet.id
  associate_public_ip_address = true
  user_data_base64            = filebase64("webserver.sh")

  tags = {
    Name = "webserver-instance"
  }
}

# dbserver instance
resource "aws_instance" "db_instance" {
  ami                    = data.aws_ssm_parameter.ubuntu_ami.value
  instance_type          = "t3.micro"
  key_name               = "fredssh"
  vpc_security_group_ids = [aws_security_group.dbserver.id]
  subnet_id              = aws_subnet.private_subnet.id
  user_data_base64       = filebase64("dbserver.sh")

  tags = {
    Name = "dbserver-instance"
  }
}
