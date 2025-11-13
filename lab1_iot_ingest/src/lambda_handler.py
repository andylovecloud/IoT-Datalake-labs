import json
import boto3
import os
from datetime import datetime, timezone

s3 = boto3.client("s3")
BUCKET = os.environ.get("BUCKET_NAME")

def lambda_handler(event, context):
    # support direct invocation or API Gateway HTTP API
    try:
        if isinstance(event, dict) and "body" in event and event["body"]:
            body = json.loads(event["body"])
        else:
            body = event if isinstance(event, dict) else {}
    except Exception as e:
        return {"statusCode": 400, "body": json.dumps({"error": "invalid JSON", "detail": str(e)})}

    required = ["machine_id", "temperature", "vibration", "timestamp"]
    missing = [k for k in required if k not in body]
    if missing:
        return {"statusCode": 400, "body": json.dumps({"error": f"missing fields: {missing}"})}

    # Key pattern for partitioning
    day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    key = f"iot_data/day={day}/machine={body['machine_id']}/{datetime.now(timezone.utc).isoformat()}.json"

    try:
        s3.put_object(Bucket=BUCKET, Key=key, Body=json.dumps(body).encode("utf-8"))
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": "s3 put failed", "detail": str(e)})}

    return {"statusCode": 200, "body": json.dumps({"message": "stored", "s3_key": key})}