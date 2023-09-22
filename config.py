import os


# Add any config variables here
class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "SET_ALTERNATIVE_SECRET_KEY"
    SECRET_REFRESH_KEY = os.environ.get("SECRET_REFRESH_KEY") or "SET_ALTERNATIVE_SECRET_REFRESH_KEY"
    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID") or "AKIAWCGHFW6O6VSEWJ6V"
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY") or "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"
    AWS_BUCKET_NAME = os.environ.get("AWS_BUCKET_NAME") or "springboard-hackathon"
    AWS_REGION = os.environ.get("AWS_REGION") or "us-east-1"
