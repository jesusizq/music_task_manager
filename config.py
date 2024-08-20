import os

basedir = os.path.abspath(os.path.dirname(__file__))
sqlite_path = "sqlite:///"


class Config:
    SECRET_KEY = os.environ.get("BMAT_TM_SECRET_KEY") or "my_secret"
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    RABBITMQ_HOST = os.environ.get("RABBITMQ_BROKER", "localhost")
    RABBITMQ_PORT = os.environ.get("RABBITMQ_PORT", 5672)
    RABBITMQ_USER = os.environ.get("RABBITMQ_USER", "user")
    RABBITMQ_QUEUE = os.environ.get("RABBITMQ_QUEUE", "task_queue")
    STORAGE_PATH = os.environ.get("STORAGE_PATH", "../local_storage")


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
