import os


class Config:
    SECRET_KEY = os.environ.get("BMAT_TM_SECRET_KEY") or "my_secret"
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


class TestingConfig(Config):
    TESTING = True
    DEBUG = True


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
