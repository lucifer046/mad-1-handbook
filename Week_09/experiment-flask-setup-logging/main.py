import os
# logging: Standard Python library for tracking events, errors, and diagnostic information
import logging
from flask import Flask
from application.config import LocalDevelopmentConfig
from application.database import db

# Setup global logging configuration
# format: timestamp, level, name, thread, message
logging.basicConfig(
    filename='debug.log', 
    level=logging.DEBUG, 
    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s'
)

# f_app: flask_application_instance
f_app = None

def init_app():
    # Setup Flask app factory
    app_inst = Flask(__name__, template_folder="templates") # app_inst: app_instance
    
    if os.getenv('ENV', "development") == "production":
      app_inst.logger.error("Production config missing!")
      raise Exception("Production config not setup.")
    else:
      app_inst.logger.info("Initializing Local Development...")
      app_inst.config.from_object(LocalDevelopmentConfig)
    
    # Initialize DB and context
    db.init_app(app_inst)
    app_inst.app_context().push()
    app_inst.logger.info("App factory initialization complete.")
    return app_inst

f_app = init_app()

# Load route controllers
from application.controllers import *

if __name__ == '__main__':
    # Start server
    f_app.run(host='0.0.0.0', port=8080)
