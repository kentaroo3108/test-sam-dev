import json
import urllib.request
import os


def lambda_handler(event, context):
    message = event['Records'][0]['Sns']['Message']
    post_slack(message)


def post_slack(message):
    send_data = {
        "username": "起動テンプレート更新の結果通知",
        "text": message
    }
    send_text = json.dumps(send_data)
    request = urllib.request.Request(
        os.environ["SLACK_INCOMING_URL"],
        data=send_text.encode("utf-8"),
        method="POST"
    )
    with urllib.request.urlopen(request) as response:
        response_body = response.read().decode("utf-8")
    return response_body
