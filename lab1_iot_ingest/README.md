# Lab 1 – IoT Ingest Pipeline (API → Lambda → S3)

## Goal
Create a serverless endpoint to receive machine telemetry and store it in S3 partitioned by day and machine.

## Prerequisites
- AWS CLI configured
- AWS SAM CLI installed (`sam`)
- Python 3.10+ for local testing

## Deploy (SAM)
```bash
cd lab1_iot_ingest
sam build
sam deploy --guided
# choose a stack name and region; accept creating IAM roles