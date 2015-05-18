import os
basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

OPENID_PROVIDERS = [
    {'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id', 'src': 'static/images/google.png'},
    {'name': 'Yahoo', 'url': 'https://me.yahoo.com', 'src': 'static/images/yahoo.png'},
    {'name': 'AOL', 'url': 'http://openid.aol.com/<username>', 'src': 'static/images/aol.png'},
    {'name': 'Flickr', 'url': 'http://www.flickr.com/<username>', 'src': 'static/images/flickr.png'},
    {'name': 'MyOpenID', 'url': 'https://www.myopenid.com', 'src': 'static/images/moID.png'}]

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

POST_PER_PAGE = 3