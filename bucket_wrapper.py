import boto3
from botocore.exceptions import ClientError
from boto3 import logging
import sys


class BucketWrapper:
    def __init__(self, s3_bucket) -> None:
        self.bucket = s3_bucket
        self.name = s3_bucket.name
        #self.logger = logging.getLogger()


    def get_objects(self, client):
        try:
            response = client.list_objects_v2(Bucket=self.name)
            objects = list(o['Key'] for o in response['Contents'])

            logging.info('Got objects: %s', objects)

        except ClientError:
            logging.exception('Could not get objects')
            raise
        else:
            return objects
        
    def get_object(self, client, object_id):
        pass

    def add_object(self, client, object_id):
        pass

