
variable "server_port" {
	description = "Port that the webserver will listen on"
	type = number
	default=8080
}

output "ServerDNS" {
	description = "Public DNS name of the web server"
	value = "http://${aws_instance.example.public_dns}:${var.server_port}/"	
}
output "ServerIP" {
	description = "Public IP address of the web server"
	value=aws_instance.example.public_ip
}

resource "aws_instance" "example" {
	ami = "ami-099b1e41f3043ce3a"
	instance_type = "t2.micro"
	user_data = <<-EOF
							#!/bin/bash
							echo "Hello, world" > index.html
							nohup busybox httpd -f -p ${var.server_port} &
							EOF
	user_data_replace_on_change = true
	vpc_security_group_ids = [aws_security_group.instance.id]
  tags = {
  	Name = "terraform-example"
  }
}

resource "aws_security_group" "instance" {
	name = "terraform-example-instance"

	ingress {
		from_port = var.server_port
		to_port = var.server_port
		protocol = "tcp" 
		cidr_blocks = ["0.0.0.0/0"]
	}
}