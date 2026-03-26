import boto3
import json

# This deliberately invokes your Lambda with bad input to trigger errors
lambda_client = boto3.client('lambda', region_name='eu-west-2')

print("Sending bad requests to trigger errors...")
for i in range(5):
    response = lambda_client.invoke(
        FunctionName='cardiac-contraction-api',
        InvocationType='RequestResponse',
        Payload=json.dumps({"invalid": "data"})
    )
    print(f"Invocation {i+1}: Status {response['StatusCode']}")

print("Done! Check your email and CloudWatch for alerts.")