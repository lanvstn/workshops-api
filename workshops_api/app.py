import logging
from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from werkzeug.contrib.fixers import ProxyFix

from workshops_api.database import db
from workshops_api.config import config

config.load_config('.')

# Initialize app
app = Flask(__name__)

# Set up logging for gunicorn
if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

# Set up CORS
CORS(app, origins=config.config['app']['allowed_origin'])

# Flask app configuration
app.config['SQLALCHEMY_DATABASE_URI'] = config.config['app']['db_connectionstring']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
if config.config['app']['enable_proxyfix']:
    app.wsgi_app = ProxyFix(app.wsgi_app)

# Set up SQLAlchemy and Flask-RESTful
db.init_app(app)
api = Api(app)

# Set up resources in separate file to avoid importing resources in app.py.
# That way app can be imported from resources without circular imports
import workshops_api.create_resources
