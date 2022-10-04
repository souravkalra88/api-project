from pydoc import describe
import uuid
from flask import request  
from flask.views import MethodView
from flask_smorest import Blueprint,abort
from db import data,users

blp = Blueprint("data" , __name__ , description = "operations on data. ")

@blp.route("/data/<string:id>")
class Data(MethodView):
    def get(self , id):
        try:
            return data[id]  
        except KeyError:  
            return abort(404, message = "Data not found. ")
        
        
    def put(self,id):
        user_data = request.get_json()
        try:
            t_data = data[id]
            t_data |= user_data
            return t_data
        except KeyError:
            abort(404 , message = "data not found. ")    
        
    def delete(self , id):
        try:
            del data[id]
            return {"msg": "User Data deleted. "} 
        except KeyError:
            abort(404 , "User Data not found. ")
            
            
@blp.route("/data")
class DataList(MethodView):
    def get(self):
        return {"data" : list(data.values())}    
    
    def post(self):
        user_data = request.get_json()
        if user_data["user_id"] not in users:
            return abort(404 , message="Data not found")
    
    
        id = uuid.uuid4().hex
        new_data = {**user_data , "id" : id}
        data[id]=new_data 
    
        return new_data , 201      
    
      