import base64
import boto3
from botocore.exceptions import ClientError
import logging
import os
from dotenv import load_dotenv
from sqlalchemy import BLOB

load_dotenv()

session = boto3.Session(
    aws_access_key_id= os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key= os.getenv('AWS_SECRET_ACCESS_KEY'),
)


def upload_file(bucket_name):

    s3_client = boto3.client('s3')
    try:

        with open("./static/samplevids/Recording.mp3", "rb") as f:
            s3_client.upload_fileobj(f, bucket_name, 'Recording.mp3')

        return None
    
    except ClientError as e:
        logging.error(e)
        return None

def download_file(bucket_name, obj_name, file_name):
    s3_client = boto3.client('s3')
    try:
        with open(file_name, 'wb') as f:
            s3_client.download_fileobj(bucket_name, obj_name, f)

    except ClientError as e:
        logging.error(e)
        return None
    


download_file('riffbucket', 'placeholder_video.mp4', './static/samplevids/new_video.mp4')

