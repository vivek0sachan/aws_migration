import boto3
import os

access_key = os.getenv('access_key_main')
secret = os.getenv('secret_main')

key2 = os.getenv('key2')
secret2 = os.getenv('secret2')

s3_source = boto3.client('s3', region_name='ap-south-2', aws_access_key_id=access_key, aws_secret_access_key=secret)
s3_destination = boto3.client('s3', region_name='ap-south-1', aws_access_key_id=key2, aws_secret_access_key=secret2)

source_bucket_name = 'souce bucket'
destination_bucket_name = 'destination bucket'

def sync_buckets(src_bucket_name, dest_bucket_name):
    # List all objects in the source bucket
    src_objects = s3_source.list_objects(Bucket=src_bucket_name)['Contents']

    for src_object in src_objects:
        file_name = src_object['Key']

        # Download the object to a local file
        s3_source.download_file(src_bucket_name, file_name, file_name)

        # Upload the local file to the destination bucket
        s3_destination.upload_file(file_name, dest_bucket_name, file_name)

        # Delete the local file
        os.remove(file_name)

sync_buckets(source_bucket_name, destination_bucket_name)


# !!!!!!!!!!!!!!!!!  only run  this if aws is failing to start sync / copy   idk why the console command for copy failed but its still letting me download from bucket