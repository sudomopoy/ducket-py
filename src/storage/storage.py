from abc import ABC, abstractmethod

class Storage(ABC):
    @abstractmethod
    def put_object_from_file(self, object_name, file_path, expiration_time=None):
        pass
    @abstractmethod
    def put_object(self, object_name, data, length, content_type='application/octet-stream'):
        pass
    @abstractmethod
    def get_object(self, object_name):
        pass
    @abstractmethod
    def delete_object(self, object_name):
        pass
    @abstractmethod
    def get_presigned_url(self, object_name, expiration_time=None):
        pass

    @abstractmethod
    def create_bucket(self, bucket_name):
        pass

    @abstractmethod
    def bucket_exists(self, bucket_name):
        pass

    @abstractmethod
    def list_objects(self, prefix=None):
        pass

    @abstractmethod
    def copy_object(self, source_object_name, dest_object_name):
        pass

    @abstractmethod
    def get_object_metadata(self, object_name):
        pass

    @abstractmethod
    def get_object_size(self, object_name):
        pass

    @abstractmethod
    def get_object_content_type(self, object_name):
        pass

    @abstractmethod
    def get_object_last_modified(self, object_name):
        pass

