import os
from flask import Flask
from flask_smorest import Api  

from db import db 
import models        

from resources.data import blp as DataBlueprint
from resources.user import blp as UserBlueprint
from resources.dose_info import blp as DoseInfoBlueprint



    
app = Flask(__name__)

    # Running on http://127.0.0.1:5000



app.config["API_TITLE"] = "Stores REST API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config[
            "OPENAPI_SWAGGER_UI_URL"
        ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

api = Api(app)
    
with app.app_context():
        db.create_all()

api.register_blueprint(UserBlueprint)
api.register_blueprint(DataBlueprint)
api.register_blueprint(DoseInfoBlueprint) 
    



@app.route("/")
def home():
    return "Hello, Flask!"