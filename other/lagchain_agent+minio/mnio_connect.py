from minio import Minio
from minio.error import  S3Error
import io
from langchain.agents import tool
import json
#load the minio creds file
file_path='credentials_minio.json'
with open(file_path ,'r') as file:
    data=json.load(file)
#store the access and secret keys
access_key=data.get('accessKey')
secret_key=data.get('secretKey')
#print(access_key,seret_key)

#connect to the minio server
minio_url = '127.0.0.1:9000'

# Create MinIO client object
minio_client = Minio(minio_url,
                     access_key=access_key,
                     secret_key=secret_key,
                     secure=False)  # Change to True if your MinIO server uses HTTPS

# Print list of buckets
print(minio_client.list_buckets())
bucket_name = "test"

try:
    # Check if bucket exists
    if not minio_client.bucket_exists(bucket_name):
        # Create the bucket because it does not exist
        minio_client.make_bucket(bucket_name)
        print(f"Bucket '{bucket_name}' created successfully.")
    else:
        print(f"Bucket '{bucket_name}' already exists.")
except S3Error as err:
    print(f"Error encountered: {err}")


#create function to upload a file to bucket
# Modify the function signature to accept only two or three arguments
@tool
def upload_file_to_minio(bucket: str, source_file_name: str, destination_file_name: str = None):
    """
    Uploads a file to MinIO.
    Parameters:
        bucket_name (str): The name of the bucket.
        source_file_name (str): The name of the object from local system.
        destination_file_name (str, optional): The name of the object to create in the bucket.
    """


    # If destination_file_name is not provided, use source_file_name as the destination file name
    if destination_file_name is None:
        destination_file_name = source_file_name

    minio_client.fput_object(bucket, destination_file_name, source_file_name)

    return f"File {source_file_name} uploaded successfully to bucket {bucket}."

@tool
def nof_lines(source_file):
    '''
    count the number of lines in source file
    :param source_file:
    :return:
    '''
    with open(source_file,'r') as file:
        data=file.read()
        lines=len(data.split('\n'))
    return lines
