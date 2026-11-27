import os


class Config:
  SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  MAX_CONTENT_LENGTH = 5 * 1024 * 1024


class DevelopmentConfig(Config):
  DEBUG = True
  SQLALCHEMY_DATABASE_URI = os.environ.get(
      "DATABASE_URL", "sqlite:///data.sqlite"
  )


class TestingConfig(Config):
  TESTING = True
  WTF_CSRF_ENABLED = False
  SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class ProductionConfig(Config):
  DEBUG = False
  SQLALCHEMY_DATABASE_URI = os.environ.get(
      "DATABASE_URL", "sqlite:///prod.sqlite"
  )


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}