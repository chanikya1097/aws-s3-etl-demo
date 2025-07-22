variable "aws_region" {
  default = "us-east-1"
}

variable "glue_job_name" {
  default = "chanikya-etl-job"
}

variable "script_s3_path" {
  default = "s3://aws-s3-etl-demo/etl/etl_script.py"
}
