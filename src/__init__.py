from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import os
from src.exercise_categories import exercise_categories
from src.database import db
from flask import Swagger, swag_from
from src.config.swagger import template, swagger_config

def create_app(test_config=None):
    
    app = Flask(__name__, instance_relative_config=True)
    
    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY = os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DB_URI"),
            
            SWAGGER={
                'title': "Workout Organizer API",
                'uiversion': 3
            }
        )
    else:
        app.config.from_mapping(test_config)
        
    db.app=app
    db.init_app(app)
    app.app_context().push()
    db.create_all()
    
    app.register_blueprint(exercise_categories)
    
    Swagger(app, config=swagger_config, template=template)
    
    return app