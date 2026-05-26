import os
from flask import Flask
# Api: The main entry point for the Flask-RESTful extension, used to register Resources
from flask_restful import Api
from application.config import LocalDevelopmentConfig
from application.database import db

# f_app: flask_application_instance, r_api: restful_api_instance
f_app = None
r_api = None

def init_app():
    # Setup Flask app factory
    app_inst = Flask(__name__, template_folder="templates") # app_inst: app_instance
    if os.getenv('ENV', "development") == "production":
      raise Exception("Production config not found.")
    else:
      print("Starting Local Development")
      app_inst.config.from_object(LocalDevelopmentConfig)
    
    # Initialize DB and REST API
    db.init_app(app_inst)
    api_inst = Api(app_inst) # api_inst: restful_api_instance
    app_inst.app_context().push()  
    return app_inst, api_inst

f_app, r_api = init_app()

# Load MVC controllers
from application.controllers import *

# Load and register REST Resources
from application.api import UserAPI
r_api.add_resource(UserAPI, "/api/user", "/api/user/<string:username>")

if __name__ == '__main__':
    # Run the Flask app
    f_app.run(host='0.0.0.0', port=8080)
