import json
import boto3
from dotenv import load_dotenv
import os
import logging

load_dotenv()
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO) #set logging level to INFO, DEBUG if we want the full dump
BUCKET = os.getenv('BUCKET')
EXISTING_KEY_ERROR_MESSAGE = 'An error occurred (NoSuchKey) when calling the GetObject operation: The specified key does not exist.'

def get_s3_client():
    ACCESS_KEY = os.getenv('ACCESS_KEY')
    SECRET_KEY = os.getenv('SECRET_KEY')

    s3_client = boto3.client(
        's3',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY
    )

    return s3_client


def info_from_s3(key, s3_client):
    if not key:
        return

    try:
        file = s3_client.get_object(
            Bucket=BUCKET,
            Key=f'{key}.json'
        )

        if file.get('Body'):
            file_body = file.get('Body')
            return json.loads(file_body.read())

    except Exception as e:
        if f'{e}' == EXISTING_KEY_ERROR_MESSAGE:
            return None
        logger.error(f'An error occurred while interacting with s3:\n{e}')

        raise e


def get_files_from_dir(key, s3_client):
    if not key:
        return

    return s3_client.list_objects_v2(Bucket=BUCKET, Prefix=f'{key}/')


def get_bytes_from_json(json_to_parse):
    return bytearray(json.dumps(json_to_parse), 'latin-1')


def upload_to_s3(content, key, s3_client):
    s3_client.put_object(
        Body=get_bytes_from_json(content), Bucket=BUCKET, Key=f'adventures/{key}.json'
    )
    logger.info('Finished uploading')