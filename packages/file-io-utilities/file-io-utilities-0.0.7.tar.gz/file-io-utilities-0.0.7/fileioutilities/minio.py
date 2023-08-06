import os
from .file_io import FileIO
import boto3, os
from operator import attrgetter
from alidaargparser import get_asset_property

def upload_s3(bucket, local_path, remote_path):
    if os.path.isfile(local_path):  
        bucket.upload_file(local_path, "/".join(remote_path.split("/")[1:]))
    else:
        try:
            for path, subdirs, files in os.walk(local_path):
                for file in files:
                    dest_path = path.replace(local_path,"")
                    __s3file = os.path.normpath(remote_path + '/' + dest_path + '/' + file)
                    __local_file = os.path.join(path, file)
                    bucket.upload_file(__local_file, __s3file)
        except Exception as e:
            print(" ... Failed!! Quitting Upload!!")
            print(e)
            raise e

def isfile_s3(bucket, key: str) -> bool:
    """Returns T/F whether the file exists."""
    objs = list(bucket.objects.filter(Prefix=key))
    return len(objs) == 1 and objs[0].key == key


def download_s3(bucket, remote_path, local_path=None):
    if isfile_s3(bucket, remote_path):
        bucket.download_file(remote_path, local_path)
    else:
        for obj in bucket.objects.filter(Prefix=remote_path):
            target = obj.key if local_path is None \
                else os.path.join(local_path, os.path.relpath(obj.key, remote_path))
            if not os.path.exists(os.path.dirname(target)):
                os.makedirs(os.path.dirname(target))
            if obj.key[-1] == '/':
                continue
            bucket.download_file(obj.key, target)


class Minio(FileIO):

    storage_type = os.path.basename(__file__).split('.py')[0]
    
    def __init__(self, name=None):
        super().__init__()
        self.name=name

        self.endpoint_url = get_asset_property(asset_name=self.name, property='minIO_URL')
        self.aws_access_key_id = get_asset_property(asset_name=self.name, property='minIO_ACCESS_KEY')
        self.aws_secret_access_key = get_asset_property(asset_name=self.name, property='minIO_SECRET_KEY')

        self.s3 = boto3.resource('s3', 
            endpoint_url= self.endpoint_url,
            aws_access_key_id = self.aws_access_key_id, 
            aws_secret_access_key = self.aws_secret_access_key)

    def upload(self, local_path, remote_path=None):
        if remote_path is None:
            remote_path = self.get_remote_path()
        # Upload model to Minio
        upload_s3(bucket = self.s3.Bucket(remote_path.split("/")[0]),
                        remote_path = "/".join(remote_path.split("/")[1:]),
                        local_path = local_path)

    def download(self, local_path, remote_path=None):
        if remote_path is None:
            remote_path = self.get_remote_path()
        # Dowload model from Minio to disk
        download_s3(bucket = self.s3.Bucket(remote_path.split("/")[0]),
                            remote_path="/".join(remote_path.split("/")[1:]), 
                            local_path=local_path)

    def get_modification_time(self):
        path = self.get_remote_path()
        bucket = self.s3.Bucket(path.split("/")[0])
        
        if isfile_s3(bucket, "/".join(path.split("/")[1:])):
            object = self.s3.Object(path.split("/")[0], "/".join(path.split("/")[1:]))
            return object.last_modified
        else:
            objs = bucket.objects.filter(Prefix="/".join(path.split("/")[1:]))

            # sort the objects based on 'obj.last_modified'
            sorted_objs = sorted(objs, key=attrgetter('last_modified'))
            latest = sorted_objs.pop()
            return latest.last_modified

