from pydoc import describe
import uuid
import hashlib
from flask import request  
from flask.views import MethodView
from flask_smorest import Blueprint,abort
from db import users
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
        # user_data = request.get_json()
        user_id = uuid.uuid4().hex 
        user_data["_password"] = hashlib.sha256(user_data["_password"].encode()).hexdigest()
        
        for u in users.values() :
            if u["user_name"] == user_data["user_name"] :
                return abort(404, message = "Same user already exists.")
        new_user = {**user_data , "user_id" : user_id }
        users[user_id] = new_user
    
        return new_user,201  