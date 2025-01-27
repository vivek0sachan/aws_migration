import os
import boto3
from dotenv import load_dotenv
import uuid

load_dotenv()

access_key = os.getenv('access_key_main')
secret = os.getenv('secret_main')

access_key2 = os.getenv('key2')
secret2 = os.getenv('secret2')

cwd=os.getcwd()
wd=os.path.join(cwd,'comparison_files')

file_id=1

for file in os.listdir(wd):
    with open(os.path.join(wd,file), 'r') as f:
        missing_files = f.read().splitlines()
    source_bucket = file.split('_')[0]
    destination_bucket=source_bucket+'-v1'
    print(f"Comparing {source_bucket} and {destination_bucket}")
    

    missed_files = []
    s3_source = boto3.resource('s3', aws_access_key_id=access_key, aws_secret_access_key=secret).Bucket(source_bucket)
    s3_destination = boto3.resource('s3', aws_access_key_id=access_key2, aws_secret_access_key=secret2).Bucket(destination_bucket)
    os.makedirs(os.path.join(cwd,source_bucket), exist_ok=True)
    for file in missing_files:
        try:
            local_file_path = os.path.join(cwd, source_bucket, file)
            os.makedirs(os.path.dirname(local_file_path), exist_ok=True)
            s3_source.download_file(file, local_file_path)
            print(f"Downloaded {file} from {source_bucket}")
        except:
            try:
                file_id = file_id + 1
                str_id=str(file_id)
                local_file_path = os.path.join(cwd, source_bucket, str_id)
                s3_source.download_file( file, local_file_path)
                s3_destination.upload_file(local_file_path, file)
                print(f"Uploaded {file} to {destination_bucket}")
                #delete the file
                os.remove(local_file_path)
                
            except Exception as e:
                print(f"Error uploading  to  {e}")
                
    # s3_destination = boto3.resource('s3', aws_access_key_id=access_key2, aws_secret_access_key=secret2).Bucket(destination_bucket)
    source_directory = os.path.join(cwd, source_bucket)
    for dir_name,subdir_list,file_list in os.walk(source_directory):
        for fname in file_list:
            source_path = os.path.join(dir_name, fname)

            destination_path = os.path.relpath(source_path, source_directory)

            destination_path = destination_path.replace("\\", "/")

            # Upload file
            s3_destination.upload_file(source_path, destination_path)
            print(f"Uploaded {source_path} to {destination_path}")
            
#

    