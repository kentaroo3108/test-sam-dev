import json
import boto3
from datetime import datetime
from aws_lambda_powertools import Logger

ec2_client = boto3.client('ec2', region_name='ap-northeast-1')
ec2_resource = boto3.resource('ec2', region_name='ap-northeast-1')
sns_client = boto3.client("sns")
logger = Logger(service="launch_update")
TOPIC_ARN = "arn:aws:sns:ap-northeast-1:282012472062:send-message-from-lambda-to-chatbot"


def create_ami(instance_id):
    try:
        instance = ec2_resource.Instance(instance_id)
        image = instance.create_image(
            Name=f'{instance_id}_{datetime.now().strftime("%Y%m%d%H%M%S")}',
            NoReboot=True
        )
        print(image)
        image.create_tags(
            Tags=[
                {
                    'Key': 'Name',
                    'Value': "Hoge"
                },
                {
                    'Key': 'Origin',
                    'Value': instance.id
                },
                {
                    'Key': 'env',
                    'Value': 'prod'
                }
            ]
        )
        #image.wait_until_exists(Filters=[{'Name': 'state', 'Values': ['available']}])
        launch_template_name = 'test-auto-20201030'
        # latest_launch_template_version_num = launch_template['LaunchTemplates'][0]['LatestVersionNumber']print(latest_launch_template_version_num)
        launch_template_version = ec2_client.describe_launch_template_versions(
            LaunchTemplateName=launch_template_name,
        )
        launch_template_data = launch_template_version['LaunchTemplateVersions'][0]['LaunchTemplateData']
        launch_template_data['ImageId'] = image.id
        new_launch_template_version = ec2_client.create_launch_template_version(
            LaunchTemplateName=launch_template_name,
            LaunchTemplateData=launch_template_data
        )
        new_launch_template_version_number = str(new_launch_template_version[
            'LaunchTemplateVersion']['VersionNumber'])
        ec2_client.modify_launch_template(
            LaunchTemplateName=launch_template_name,
            DefaultVersion=new_launch_template_version_number
        )

        logger.info("Upgrade the launch template to" +
                    " " + new_launch_template_version_number)
        send_message_sns()

    except Exception as e:
        logger.info(e)
        send_message_sns


def send_message_sns():
    response = sns_client.publish(
        TopicArn=TOPIC_ARN,
        Message="test-hoge-test",
        Subject="hoge",
        MessageStructure="hoge"
    )
    return response


def lambda_handler(event, context):
    #instance_id = event['instance_id']
    create_ami("i-0151c2e6299498c6f")
    print("hogee")aaassas
