provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "framke_results" {
  bucket = "framke-analysis-results-bucket"

  tags = {
    Name        = "FramkeAnalysisBucket"
    Environment = "Dev"
    Tool        = "Framke"
  }
}
