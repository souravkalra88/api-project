from flask.views import MethodView
from flask_smorest import Blueprint , abort
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    jwt_required,
)
from db import db
import hashlib
from models import UserModel
from schemas import UserLoginSchema
from blocklist import BLOCKLIST


blp = Blueprint("Users" , "users" , description = "login on users. " )

@blp.route("/login")
class UserRegister(MethodView):
    
    @blp.arguments(UserLoginSchema)
    def post(self , user_data):
        user = UserModel.query.filter(UserModel.user_name == user_data["user_name"]).first()
        if user and user._password == hashlib.sha256(user_data["_password"].encode()).hexdigest() :
            access_token =  create_access_token(identity = user.user_id)   
            return {"access_token": access_token}
        
        return abort (401 , message = "Invalid crdentials. ")
        
    
    @blp.route("/logout")
    class UserLogout(MethodView):
        @jwt_required()
        def post(self):
            jti = get_jwt()["jti"]
            BLOCKLIST.add(jti)
            return {"message": "Successfully logged out"}, 200    