import boto3

class BucketWrapper:
    def __init__(self, s3_bucket) -> None:
        self.bucket = s3_bucket
        self.name = s3_bucket.name
    

    def get_objects(self, client):
        response = client.list_objects_v2(Bucket=self.name)

        objects = []
        for o in response['Contents']:
            objects.append(o['Key'])

        return objects
        
        
    