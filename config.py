import os
from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))
'''
you need to make some decisions, which you pass to the framework
as a list of configuration variables.
'''
class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess' # cryptographic key, useful to generate signatures or tokens.
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
		'sqlite:///' + os.path.join(basedir, 'app.db')
	SQLALCHEMY_TRACK_MODIFICATIONS = False # signal the application every time a change is about to made in the database.
	MAIL_SERVER = os.environ.get('MAIL_SERVER')
	MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
	MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
	ADMINS = ['gauravchopracg@gmail.com']
	POSTS_PER_PAGE=3
	ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
	LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')