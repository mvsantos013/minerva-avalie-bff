import os
import io
import boto3
import pandas as pd
import json
from io import StringIO, BytesIO
from src.constants import BUCKET_FILES

s3 = boto3.client('s3')


def file_exists(path):
    try:
        s3.head_object(Bucket=BUCKET_FILES, Key=path)
        return True
    except:
        return False


def save_to_s3(path, data):
    s3.put_object(Key=path, Body=data, Bucket=BUCKET_FILES)


def read_csv(path, delimiter=','):
    return pd.read_csv('s3://' + BUCKET_FILES + '/' + path, sep=delimiter)


def read_json(path):
    obj = s3.get_object(Bucket=BUCKET_FILES, Key=path)
    return json.loads(obj['Body'].read())


def save_df_to_s3(path, df, format='csv'):
    if format == 'csv':
        buffer = StringIO()
        df.to_csv(buffer, index=False)
        data = buffer.getvalue()
        save_to_s3(BUCKET_FILES, path, data)
    elif format == 'xlsx':
        buffer = BytesIO()
        df.to_excel(buffer, index=False)
        data = buffer.getvalue()
        save_to_s3(BUCKET_FILES, path, data)
    else:
        raise Exception('Invalid format.')


def list_files(prefix):
    result = s3.list_objects_v2(Bucket=BUCKET_FILES, Prefix=prefix)
    if 'Contents' not in result:
        return []
    return result['Contents']


def download_file(path):
    response = s3.get_object(Bucket=BUCKET_FILES, Key=path)
    obj = response['Body'].read()
    return io.BytesIO(obj)


def upload_file(path, file):
    file.seek(0)
    s3.upload_fileobj(file, BUCKET_FILES, path)


def upload_excel(path, file):
    file.seek(0)
    s3.upload_fileobj(
        file,
        BUCKET_FILES,
        path,
        ExtraArgs={
            'ContentType': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        },
    )

def delete_file(path):
    s3.delete_object(Bucket=BUCKET_FILES, Key=path)