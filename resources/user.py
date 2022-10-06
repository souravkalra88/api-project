from pydoc import describe
import uuid
import hashlib
from flask import request  
from flask.views import MethodView
from flask_smorest import Blueprint,abort
from models.user import UserModel
from db import db 
from sqlalchemy.exc import SQLAlchemyError
from schemas import  UsersSchema 

blp = Blueprint("users" , __name__ , description = "operations on users")

@blp.route("/user/<string:user_id>")
class User(MethodView):
    def get(self, user_id):
        try:
            return users[user_id]
        except KeyError:
            return abort(404, message = "User not found. ") 
    
    def delete(self, user_id):
        try:
            del users[user_id]
            return {"msg": "User deleted. "}
        except KeyError:
            abort(404, message = "User not found. ")
            
            
            
            
@blp.route("/user")
class UserList(MethodView):
    def get(self):
        return {"users" : list(users.values())}
    
    
    @blp.arguments(UsersSchema)
    def post(self,user_data):
        user_data = request.get_json()
        user_data["_password"] = hashlib.sha256(user_data["_password"].encode()).hexdigest()
        new_user = UserModel(**user_data)
        
        try:
            db.session.add(new_user)
            db.session.commit()
        except SQLAlchemyError as e :
            return abort(500 , message = "EROOR OCCURED with data->. {}".format(e) )    
       
    
        return {"user" : new_user} , 201  
    
   