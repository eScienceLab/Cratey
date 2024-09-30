import os


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious')


class DevelopmentConfig(Config):
    DEBUG = True
    ENV = 'development'


class ProductionConfig(Config):
    DEBUG = False
    ENV = 'production'
