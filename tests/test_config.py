class TestConfig:
    
    SECRET_KEY = '677306db4d65b4cd908094b8d74370db'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../tests/test.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True
