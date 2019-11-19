class Development:
    DEBUG = True
    SECRET_KEY = 'b65/0464/2009'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:root@127.0.0.1:5432/cust_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class Production:
    pass