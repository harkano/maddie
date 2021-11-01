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
#Handle Replicate functionality
        # if file.get('Metadata','replicate'):
        #     key = file['Metadata']['replicate']
        #     try:
        #         file = s3_client.get_object(
        #             Bucket=BUCKET,
        #             Key=f'{key}.json'
        #         )
        #         if file.get('Body'):
        #             file_body = file.get('Body')
        #             return_dict = json.loads(file_body.read())
        #             return_dict['replicate_key'] = key
        #             return return_dict
        #     except Exception as e:
        #         if f'{e}' == EXISTING_KEY_ERROR_MESSAGE:
        #             return None
        #         logger.error(f'An error occurred while interacting with s3:\n{e}')
        #
        #     raise e
#Handles normal case
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

def get_char_files_from_dir(key, s3_client):
    if not key:
        return
    response = s3_client.list_objects_v2(Bucket=BUCKET, Prefix=f'{key}')
    for content in response.get('Contents', []):
        yield content.get('Key')
    return


def get_bytes_from_json(json_to_parse):
    return bytearray(json.dumps(json_to_parse), 'latin-1')


def upload_to_s3(content, key, s3_client):
    #Take the replicate key from the json, kill it and move it to metadata
    if content.get('replicate_key'):
        key = content['replicate_key']
        content.pop('replicate_key')
        s3_client.put_object(
            Body=get_bytes_from_json(content), Bucket=BUCKET, Key=f'{key}.json', Metadata={'replicate': key}
        )
    else: #normal case for any other json updates
        s3_client.put_object(
        Body=get_bytes_from_json(content), Bucket=BUCKET, Key=f'{key}.json'
        )
    logger.info('Finished uploading')

def s3_delete(key, s3_client):
    s3_client.delete_object(Bucket=BUCKET, Key=f'{key}.json')
    logger.info('Deleting channel file ' + key )