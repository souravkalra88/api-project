from pydoc import describe
import uuid
import hashlib
from flask import jsonify, request  
from flask.views import MethodView
from flask_jwt_extended import get_jwt, jwt_required
from flask_smorest import Blueprint,abort
from sqlalchemy import JSON
from models.user import UserModel
from db import db 
from sqlalchemy.exc import SQLAlchemyError
from schemas import  PlainUsersSchema, UsersSchema 
import json 
blp = Blueprint("users" , __name__ , description = "operations on users")

@blp.route("/user/<int:user_id>")
class User(MethodView):
    @jwt_required()
    @blp.response(200 , UsersSchema )
    def get(self, user_id):
        t_user = UserModel.query.get_or_404(user_id)
        return t_user
    @jwt_required()
    def delete(self, user_id):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required.")
        t_user = UserModel.query.get_or_404(user_id)
        db.session.delete(t_user)
        db.session.commit()
        return {"msg": "User deleted successfully"} , 200
            
            
            
            
@blp.route("/user")
class UserList(MethodView):
    @jwt_required()
    @blp.response(200 , UsersSchema(many = True))
    def get(self):
        
        return UserModel.query.all()
    
    @jwt_required()
    @blp.arguments(UsersSchema)
    @blp.response(201 , UsersSchema)
    def post(self,user_data):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required.")
        user_data = request.get_json()
        user_data["_password"] = hashlib.sha256(user_data["_password"].encode()).hexdigest()
        new_user = UserModel(**user_data)
        
        try:
            db.session.add(new_user)
            db.session.commit()
        except SQLAlchemyError as e :
            return abort(500 , message = "EROOR OCCURED with data->. {}".format(e) )    
       
    
        return new_user 
    
    
    
   