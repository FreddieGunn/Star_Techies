import os


# Add any config variables here
class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "SET_ALTERNATIVE_SECRET_KEY"
    SECRET_REFRESH_KEY = os.environ.get("SECRET_REFRESH_KEY") or "SET_ALTERNATIVE_SECRET_REFRESH_KEY"
    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
    AWS_BUCKET_NAME = os.environ.get("AWS_BUCKET_NAME")
    AWS_REGION = os.environ.get("AWS_REGION")
