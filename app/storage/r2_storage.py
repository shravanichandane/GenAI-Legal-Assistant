import os
import boto3
from typing import Optional
from botocore.exceptions import ClientError
from app.storage.base import StorageProvider
import asyncio

class R2StorageProvider(StorageProvider):
    """
    Storage provider for Cloudflare R2 (S3-compatible).
    Used for production deployments.
    """

    def __init__(self):
        self.bucket_name = os.getenv("R2_BUCKET_NAME")
        self.account_id = os.getenv("CF_ACCOUNT_ID")
        self.access_key_id = os.getenv("R2_ACCESS_KEY_ID")
        self.secret_access_key = os.getenv("R2_SECRET_ACCESS_KEY")
        
        if not all([self.bucket_name, self.account_id, self.access_key_id, self.secret_access_key]):
            raise ValueError("R2 storage credentials are not fully configured in environment variables.")

        self.endpoint_url = f"https://{self.account_id}.r2.cloudflarestorage.com"
        
        self.s3_client = boto3.client(
            's3',
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.access_key_id,
            aws_secret_access_key=self.secret_access_key,
            region_name='auto'  # R2 requires region to be 'auto' or 'us-east-1' depending on SDK version
        )

    async def upload_file(self, file_name: str, file_data: bytes, content_type: str = "application/octet-stream") -> str:
        # Wrap boto3 blocking call in asyncio
        def _upload():
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=file_name,
                Body=file_data,
                ContentType=content_type
            )
            # R2 doesn't have a default public URL unless a custom domain is set up.
            # Returning a generic S3 URI for internal tracking.
            return f"s3://{self.bucket_name}/{file_name}"
            
        return await asyncio.to_thread(_upload)

    async def download_file(self, file_name: str) -> Optional[bytes]:
        def _download():
            try:
                response = self.s3_client.get_object(Bucket=self.bucket_name, Key=file_name)
                return response['Body'].read()
            except ClientError as e:
                if e.response['Error']['Code'] == 'NoSuchKey':
                    return None
                raise
                
        return await asyncio.to_thread(_download)

    async def delete_file(self, file_name: str) -> bool:
        def _delete():
            try:
                self.s3_client.delete_object(Bucket=self.bucket_name, Key=file_name)
                return True
            except ClientError:
                return False
                
        return await asyncio.to_thread(_delete)
