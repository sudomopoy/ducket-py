import logging

from minio import Minio
from minio.error import S3Error
from datetime import timedelta
import os

from storage.storage import Storage

# Initialize MinIO client



class MinioStorage(Storage):
    def __init__(self, endpoint_url, access_key, secret_key, secure, bucket_name):
        self.bucket_name = bucket_name
        self.minio_client = Minio(
            endpoint_url,
            access_key,
            secret_key,
            secure
        )

    def put_object_from_file(self, object_name,file_path, expiration_time=None):
        self.minio_client.fput_object(self.bucket_name, object_name, file_path)

        if expiration_time is not None:
            self.minio_client.set_object_retention(self.bucket_name, object_name, retention_period=expiration_time)
            
    def put_object(self, object_name, data, length, content_type='application/octet-stream'):
        try:
            self.minio_client.put_object(self.bucket_name, object_name, data, length, content_type)
        except S3Error as e:
            logging.error(f"Error occurred while putting object: {e}")
            
    def get_object(self, object_name):
        try:
            # Get the object from MinIO
            response = self.minio_client.get_object(self.bucket_name, object_name)
            return response.read()  # Read the object data
        except S3Error as e:
            logging.error(f"Error occurred while getting object: {e}")
            return None

    def delete_object(self, object_name):
        try:
            # Delete the object from MinIO
            self.minio_client.remove_object(self.bucket_name, object_name)
            logging.info(f"Object '{object_name}' deleted successfully.")
        except S3Error as e:
            logging.error(f"Error occurred while deleting object: {e}")


    def get_presigned_url(self, object_name, expiration_time=None):
        try:
            if expiration_time is None:
                expiration_time = timedelta(days=7)
            return self.minio_client.presigned_get_object(self.bucket_name, object_name, expires=expiration_time)
        except S3Error as e:
            logging.error(f"Error occurred while getting presigned URL: {e}")
            return None

    def create_bucket(self, bucket_name):
        try:
            self.minio_client.make_bucket(bucket_name)
        except S3Error as e:
            logging.error(f"Error occurred while creating bucket: {e}")

    def bucket_exists(self, bucket_name):
        try:
            return self.minio_client.bucket_exists(bucket_name)
        except S3Error as e:
            logging.error(f"Error occurred while checking bucket existence: {e}")
            return False

    def list_objects(self, prefix=None):
        try:
            objects = self.minio_client.list_objects(self.bucket_name, prefix=prefix)
            return [obj.object_name for obj in objects]
        except S3Error as e:
            logging.error(f"Error occurred while listing objects: {e}")
            return []

    def copy_object(self, source_object_name, dest_object_name):
        try:
            self.minio_client.copy_object(
                self.bucket_name, 
                dest_object_name,
                f"{self.bucket_name}/{source_object_name}"
            )
        except S3Error as e:
            logging.error(f"Error occurred while copying object: {e}")

    def get_object_metadata(self, object_name):
        try:
            return self.minio_client.stat_object(self.bucket_name, object_name)
        except S3Error as e:
            logging.error(f"Error occurred while getting object metadata: {e}")
            return None

    def get_object_size(self, object_name):
        try:
            stat = self.minio_client.stat_object(self.bucket_name, object_name)
            return stat.size
        except S3Error as e:
            logging.error(f"Error occurred while getting object size: {e}")
            return None

    def get_object_content_type(self, object_name):
        try:
            stat = self.minio_client.stat_object(self.bucket_name, object_name)
            return stat.content_type
        except S3Error as e:
            logging.error(f"Error occurred while getting object content type: {e}")
            return None

    def get_object_last_modified(self, object_name):
        try:
            stat = self.minio_client.stat_object(self.bucket_name, object_name)
            return stat.last_modified
        except S3Error as e:
            logging.error(f"Error occurred while getting object last modified time: {e}")
            return None
__instance = None

def get_storage(endpoint_url, access_key, secret_key, secure, bucket_name) -> Storage:
    global __instance
    if __instance is None:
        __instance = MinioStorage(endpoint_url, access_key, secret_key, secure, bucket_name)

    return __instance
