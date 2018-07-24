from django.conf import settings
from django.utils.crypto import get_random_string
import os
import boto3


def get_client():
    s3 = boto3.resource('s3')
    return s3.meta.client


def get_bucket():
    return settings.AWS_STORAGE_BUCKET_NAME


def get_path():
    filename = f'{get_random_string()}.pdf'
    return os.path.join('uploads/cv/', filename)


def upload(filepath):
    client = get_client()
    path = get_path()
    client.upload_file(filepath, get_bucket(), path, {"ACL": 'public-read'})
    return f"https://{get_bucket()}.s3.amazonaws.com/{path}"
