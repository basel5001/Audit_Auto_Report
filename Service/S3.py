from botocore.exceptions import ClientError
import helper
import boto3

# audit-iap-automation
# class UploadFileS3:
#     def __init__(self, logger, profile):
#         self.logger = logger
s3 = boto3.client("s3")

def upload_file(file_path, bucket, file_name):
    print("Uploading file to S3 bucket")
    # try:
    response = s3.upload_file(
        str(file_path),  # File name
        str(bucket),  # Bucket name
        str(file_name),  # Object name
    )
    print("File has been uploaded")
    # print(response)

def download_file(file_path, bucket, file_name):
    print("Downloading file from S3 bucket")
    response = s3.download_file(
        str(file_path),  # File name
        str(bucket),  # Bucket name
        str(file_name),  # Object name
        )
    print("File has been downloaded")
    # print(response)
    # except ClientError as e:
    #     print(e)
    #     return print("An error occurred. File was not uploaded.")
    # return self.logger.info("File has been uploaded.")
    
