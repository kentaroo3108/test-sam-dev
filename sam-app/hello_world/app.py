import json

def lambda_handler(event, context):
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello world8",
            # "location": ip.text.replace("\n", "")
        }),
    }
