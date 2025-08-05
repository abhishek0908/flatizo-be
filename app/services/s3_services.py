# services/storage/s3.py

import boto3
from botocore.exceptions import ClientError
from app.services.storage.base import StorageService
from app.config.settings_config import AWSConfig  # Updated import
import uuid


class S3StorageService(StorageService):
    def __init__(self):
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=AWSConfig.ACCESS_KEY,
            aws_secret_access_key=AWSConfig.SECRET_KEY,
            region_name=AWSConfig.REGION,
        )
        self.bucket_name = AWSConfig.BUCKET_NAME

    def upload_file(self, file_obj, filename, content_type):
        key = f"{uuid.uuid4()}_{filename}"
        try:
            self.s3.upload_fileobj(
                Fileobj=file_obj,
                Bucket=self.bucket_name,
                Key=key,
                ExtraArgs={"ContentType": content_type},
            )
            return (
                f"https://{self.bucket_name}.s3.{AWSConfig.REGION}.amazonaws.com/{key}"
            )
        except ClientError as e:
            raise Exception("Upload failed") from e

    def delete_file(self, key: str):
        try:
            self.s3.delete_object(Bucket=self.bucket_name, Key=key)
        except ClientError as e:
            raise Exception("Delete failed") from e
