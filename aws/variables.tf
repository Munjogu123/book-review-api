variable "aws_region" {
  description = "The AWS region to launch our EC2 instance"
  type        = string
  default     = "eu-north-1"
}

variable "aws_availability_zone" {
  description = "AWS Availability zones"
  type        = string
  default     = "eu-north-1a"
}
