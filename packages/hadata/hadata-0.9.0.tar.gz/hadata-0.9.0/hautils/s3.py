import logging
import os

import boto3
from botocore.exceptions import ClientError

from dotenv import load_dotenv

from hautils.missconfig import MissingConfiguration

load_dotenv(override=False)

ACCESS_KEY = os.getenv("ACCESS_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

if ACCESS_KEY is None or SECRET_KEY is None:
    raise MissingConfiguration

def get_s3_client():
    # Upload the file
    s3_client = boto3.client(
        's3',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        region_name='ap-southeast-1')
    return s3_client


def upload_file(s3_client, file_obj, object_name=None):
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_obj
    try:
        s3_client.upload_fileobj(file_obj, S3_BUCKET_NAME, f"{object_name}")
    except ClientError as e:
        logging.error(e)
        return False
    return True


def upload_file_2(s3_client, file_obj, object_name=None):
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_obj
    try:
        s3_client.upload_file(file_obj, S3_BUCKET_NAME, f"{object_name}")
    except ClientError as e:
        logging.error(e)
        return False
    return True


def delete_file(file_obj):
    try:
        s3 = boto3.client(
            "s3", aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY
        )
        s3.delete_object(Bucket=S3_BUCKET_NAME, Key=file_obj)
        return True
    except Exception as ex:
        print(str(ex))
        return False


def create_presigned_url(object_name, expiration):
    s3_client = get_s3_client()
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': S3_BUCKET_NAME,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    return response
