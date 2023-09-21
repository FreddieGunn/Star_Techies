import os


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "SET_ALTERNATIVE_SECRET_KEY"
    SECRET_REFRESH_KEY = os.environ.get("SECRET_REFRESH_KEY") or "SET_ALTERNATIVE_SECRET_REFRESH_KEY"
