import os

basedir = os.path.abspath(os.path.dirname(__file__))
sqlite_path = "sqlite:///"


class Config:
    SECRET_KEY = os.environ.get("BMAT_TM_SECRET_KEY") or "my_secret"
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DEV_DATABASE_URL"
    ) or sqlite_path + os.path.join(basedir, "data-dev.sqlite")


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or sqlite_path + os.path.join(basedir, "data.sqlite")


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("TEST_DATABASE_URL")
        or sqlite_path
        + os.path.join(basedir, "data-test.sqlite")
        + "?check_same_thread=False"
    )


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
