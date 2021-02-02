import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, 'con.env'))


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'information.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.environ.get('SECRET_KEY') or '123456789'

    URL_AUTH = 'https://api.getresponse.com/v3/accounts'
    URL_TAGS = 'https://api.getresponse.com/v3/tags'
    URL_SEGMENTS = 'https://api.getresponse.com/v3/search-contacts'
    KEY = 'pgeu0bwiitvuijtmtwo369npkgr5m813'

    HEADERS_AUTH = {'X-Auth-Token': 'api-key ' + KEY,
                    'X-Domain': 'test.getresponseservices.ru',
                    'Content-Type': 'application/json'
                    }
