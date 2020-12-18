import boto3
from aws_lambda_powertools import Logger
import os

ec2_client = boto3.client('ec2', region_name='ap-northeast-1')
ec2_resource = boto3.resource('ec2', region_name='ap-northeast-1')
logger = Logger(service="launch_update")


def lambda_handler(event, context):
    try:
        launch_update(image)
    except Exception as e:
        logger.info(e)


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
    logger.info("Upgrade the launch template to" +
                " " + new_launch_template_version_number)ss
