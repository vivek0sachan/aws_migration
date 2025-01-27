import boto3
from botocore.exceptions import ClientError
import os
from dotenv import load_dotenv

load_dotenv()

access_key = os.getenv('access_key_main')
secret = os.getenv('secret_main')

# list all the buckets
def load_s3_file_name(cwd,access_key, secret):
    
    s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret)
    bucket_list = s3.list_buckets()


    for bucket in bucket_list['Buckets']:
        try:
            bucket_region = s3.get_bucket_location(Bucket=bucket['Name'])['LocationConstraint']
            if bucket_region is None:
                bucket_region = 'us-east-1'  #region need to be manually fed , will update later for full auto
            print(bucket["Name"],':',bucket_region,"fetching...")
            s3_specific_bucket = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret, region_name=bucket_region)    
            with open (os.path.join(cwd,bucket['Name']+'.txt'), 'w') as f:
                paginator = s3_specific_bucket.get_paginator('list_objects_v2')
                for page in paginator.paginate(Bucket=bucket['Name']):
                    if 'Contents' in page:
                        for content in page['Contents']:
                            if content['Key'].endswith('/'):
                                pass
                            else:
                                f.write(content['Key'] + '\n')
                        
        except Exception as e:
            print(f"Error fetching contents of bucket {bucket['Name']}: {e}")
        
                        
key2 = os.getenv('key2')
secret2 = os.getenv('secret2')

def bucket_list(wd,access_key, secret,key2, secret2):
    s3=boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret)
    bucket_list1=s3.list_buckets()
    s3=boto3.client('s3', aws_access_key_id=key2, aws_secret_access_key=secret2)
    bucket_list2=s3.list_buckets()
    
    bucekts_old=[]
    bucket_new=[]
    for buckets in bucket_list1['Buckets']:
        bucekts_old.append(buckets['Name'])
    print(bucekts_old)
    for bucket in bucket_list2['Buckets']:
        bucket_new.append(bucket['Name'])
    print(bucket_new)

wd=os.getcwd()
cwd=os.path.join(wd,'secondary_files')
load_s3_file_name(cwd,key2, secret2)
cwd=os.path.join(wd,'main_files')
load_s3_file_name(cwd,access_key, secret)

# bucket_list(wd,access_key, secret,key2, secret2)


# !!!!!!!this is for case where we have partial success in migration and there are some files left that havent been copied to new buckets
# !! make sure to copy over bucket settings and pemissions before commiting to migration