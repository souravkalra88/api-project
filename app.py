import os
from flask import Flask, jsonify
from flask_smorest import Api  
from flask_jwt_extended import JWTManager
from blocklist import BLOCKLIST
from db import db 
import models        
 
from resources.data import blp as DataBlueprint
from resources.user import blp as UserBlueprint
from resources.dose_info import blp as DoseInfoBlueprint
from resources.user_login import blp as UserLoginBlueprint


    
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

app.config["JWT_SECRET_KEY"] = "143079928960885030643450889404084499991"

jwt = JWTManager(app)
 
@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:
        return {"is_admin": True}
    return {"is_admin": False} 
   
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return (
        jsonify({"message": "The token has expired.", "error": "token_expired"}),
        401,
    )

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return (
        jsonify(
            {"message": "Signature verification failed.", "error": "invalid_token"}
        ),
        401,
    )

@jwt.unauthorized_loader
def missing_token_callback(error):
    return (
        jsonify(
            {
                "description": "Request does not contain an access token.",
                "error": "authorization_required",
            }
        ),
        401,
    )    

@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    return jwt_payload["jti"] in BLOCKLIST


@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return (
        jsonify(
            {"description": "The token has been revoked.", "error": "token_revoked"}
        ),
        401,
    )    
    
with app.app_context():
        db.create_all()

api.register_blueprint(UserBlueprint)
api.register_blueprint(DataBlueprint)
api.register_blueprint(DoseInfoBlueprint) 
api.register_blueprint(UserLoginBlueprint)



@app.route("/")
def home():
    return "Hello, Flask!"