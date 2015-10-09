import os
from logging import NOTSET, DEBUG, WARN, INFO, ERROR, CRITICAL

__all__ = ['ConfigFactory']

class ConfigFactory(object):
    """
    Generates the configuration for the current environment
    """
    
    @staticmethod
    def build_config():
        """
        Based on whether or not an environment-specific variable or
        variables is/are present, chooses the appropriate configuration
        """
        
        # TODO: change once hosting environment is known
        if os.getenv('ON_PRODUCTION') is not None:
            return _ProductionConfig()
        return _DevelopmentConfig()


class _BaseConfig(object):
    """
    The configuration keys common to all config types
    """
    
    def _build_sql_uri():
        # TODO: change once hosting environment is known
        mysql_parameters = {
            'username': os.getenv('MYSQL_USERNAME', 'root'),
            'password': os.getenv('MYSQL_PASSWORD', ''),
            'host': os.getenv('MYSQL_HOST', 'localhost'),
            'port': os.getenv('MYSQL_PORT', 3306),
            'database': 'conversationIM'
        }

        return 'mysql://{username}:{password}@{host}:{port}/{database}'.format(**mysql_parameters)

    DEBUG = False
    TESTING = False
    BUNDLE_ERRORS = True
    SECRET_KEY = os.getenv('CONVERSATIONIM_API_SECRET', 'https://open.spotify.com/track/64i1dyG9Td5z5Q0TCG17Pb')
    LOGGING_LEVEL = NOTSET
    SQLALCHEMY_DATABASE_URI = _build_sql_uri()

class _DevelopmentConfig(_BaseConfig):
    """
    The configuration keys and their corresponding settings 
    for a development environment
    """
    
    DEBUG = True
    TESTING = True
    LOGGING_LEVEL = INFO

class _ProductionConfig(_BaseConfig):
    """
    The configuraiton keys and their corresponding settings
    for a production environment
    """
    
    LOGGING_LEVEL = ERROR