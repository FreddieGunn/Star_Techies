from api import api, s3_client

bucket_info = s3_client.head_bucket(Bucket=api.config['AWS_BUCKET_NAME'])


def get_bucket():
    print(bucket_info['ResponseMetadata']['HTTPStatusCode'])
    print(bucket_info['ResponseMetadata']['HTTPHeaders']['x-amz-bucket-region'])
    s3_client.download_file(api.config['AWS_BUCKET_NAME'], 'Springboard_test.png', 'Springboard_test.png')
