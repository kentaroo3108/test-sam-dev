import boto3
from datetime import datetime
from aws_lambda_powertools import Logger
import os


ec2_client = boto3.client('ec2', region_name='ap-northeast-1')
ec2_resource = boto3.resource('ec2', region_name='ap-northeast-1')
logger = Logger(service="launch_updates")
sns_client = boto3.client("sns")

TOPIC_ARN = os.environ["SNS_TOPIC_ARN"]


def lambda_handler(event, context):
    try:
        instance_id = event['instance_id']
        env = event['env']
        image = create_ami(env=env, instance_id=instance_id)
        launch_update(image)
        send_message_sns("sucsess!!")
    except Exception as e:
        logger.info(e)
        send_message_sns("error!!")


def create_ami(env, instance_id):
    instance = ec2_resource.Instance(instance_id)
    image = instance.create_image(
        Name=f'{env}_{instance_id}_{datetime.now().strftime("%Y%m%d%H%M%S")}',
        NoReboot=True
    )
    n_tag = [tag for tag in instance.tags if tag['Key'] == 'Name'][0]['Value']
    image.create_tags(
        Tags=[
            {
                'Key': 'Name',
                'Value': n_tag
            },
            {
                'Key': 'Origin',
                'Value': instance.id
            },
            {
                'Key': 'env',
                'Value': env
            }
        ]
    )
    # image.wait_until_exists(
    #    Filters=[{'Name': 'state', 'Values': ['available']}]
    # )
    logger.info("create AMI sucsess.")
    return image


def launch_update(image):
    launch_template_name = os.environ["TEMPLATE_NAME"]
    launch_template_version = ec2_client.describe_launch_template_versions(
        LaunchTemplateName=launch_template_name,
    )
    launch_template_data = launch_template_version[
        'LaunchTemplateVersions'][0]['LaunchTemplateData']
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
    logger.info("Upgrade the launch template tooo" +
                " " + new_launch_template_version_number)


def send_message_sns(message):
    response = sns_client.publish(
        TopicArn=TOPIC_ARN,
        Message=message
    )
    return response
