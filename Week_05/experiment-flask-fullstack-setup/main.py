# os: For interacting with environment variables and file paths
import os
# Flask: The core web application framework
from flask import Flask
# LocalDevelopmentConfig: A custom class from application/config.py that holds dev settings
from application.config import LocalDevelopmentConfig
# db: The SQLAlchemy instance initialized in application/database.py
from application.database import db

# f_app: flask_application_instance
f_app = None

def init_app():
    # Setup Flask app factory
    app_inst = Flask(__name__, template_folder="templates") # app_inst: app_instance
    
    if os.getenv('ENV', "development") == "production":
      raise Exception("Production config not found.")
    else:
      print("Starting Local Development")
      app_inst.config.from_object(LocalDevelopmentConfig)
    
    # Initialize DB with app
    db.init_app(app_inst)
    app_inst.app_context().push()
    return app_inst

f_app = init_app()

# Load controllers (routes)
from application.controllers import *

if __name__ == '__main__':
    # Run the Flask app
    f_app.run(host='0.0.0.0', port=8080)
