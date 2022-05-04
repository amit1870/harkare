'''
This module will contain helper functions.
'''

import secrets
from datetime import datetime, timedelta
from django.utils import timezone
from minio import Minio
from minio.error import S3Error

from harkare.settings import Path, MINIO, MEDIA_ROOT


def generate_hex_string(code_len=22):
    return secrets.token_urlsafe(code_len)

def is_expired(set_date_time, by_hour=1):
    current_date_time = timezone.now()

    if current_date_time - timedelta(by_hour) > set_date_time:
        return True

    return False


def handle_uploaded_file(f, rename='siyaram'):
    rename = f"{rename}"
    FILE_PATH = f"{MEDIA_ROOT}/{rename}"
    url_string = ''

    saved_response = save_file(f, FILE_PATH)
    if saved_response:
        url_string = upload_file_to_minio(FILE_PATH, rename)
        delete_file(FILE_PATH)

    return url_string


def save_file(f, file_path):
    success = True
    try:    
        with open(file_path, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
    except FileNotFoundError:
        print('Heroku Upload Error')
        success = False
    except Exception as e:
        print(e)
        success = False

    return success

def upload_file_to_minio(file_path, object_name):

    client = get_minio_client()

    bucket_name = MINIO['bucket_name']

    # Check if bucket exists otherwise create it.

    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)

    # upload file to minio
    result = client.fput_object(bucket_name, object_name, file_path)

    url = get_minio_url(client, bucket_name, result.object_name, days=7)

    return url

def delete_file(file_path):
    Path.unlink(Path(file_path), missing_ok=True)


def remove_file_from_minio(client, bucket_name, object_name):
    result = client.remove_object(bucket_name, object_name)
    return result

def get_minio_client():

    # Create a client with the MinIO server playground, its access key
    # and secret key.

    client = Minio(
        MINIO['endpoint'],
        access_key=MINIO['access_key'],
        secret_key=MINIO['secret_key'],
        secure=False
    )
    return client


def get_minio_url(client, bucket_name, object_name, days=7):
    url = client.get_presigned_url(
        "GET",
        bucket_name,
        object_name,
        expires=timedelta(days=days),
    )

    return url

