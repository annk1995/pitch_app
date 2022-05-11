import os
# parent Config class contains configurations that are used in both production and development stages.
class Config:
    '''
    General configuration parent class
    '''
    # email configurations
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")



# ProdConfig subclass contains configurations that are used in production stages of our application and inherits from the parent Config class.
class ProdConfig(Config):
    '''
    Production  configuration child class
    Args:
        Config: The parent configuration class with General configuration settings
    '''
    pass


# DevConfig subclass contains configurations that are used in development stages of our application and inherits from the parent Config class.
class DevConfig(Config):
    '''
    Development  configuration child class
    Args:
        Config: The parent configuration class with General configuration settings
    '''

    DEBUG = True


config_options = {
    'development': DevConfig,
    'production': ProdConfig
}