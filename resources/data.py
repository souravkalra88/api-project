from email import message
from pydoc import describe
import uuid
from flask import request  
from flask.views import MethodView
from flask_smorest import Blueprint,abort
from sqlalchemy.exc import SQLAlchemyError
from models import DataModel
from db import db 

from schemas import DataSchems, DataUpdateSchema

blp = Blueprint("data" , __name__ , description = "operations on data. ")

@blp.route("/data/<string:id>")
class Data(MethodView):
    def get(self , id):
        try:
            return data[id]  
        except KeyError:  
            return abort(404, message = "Data not found. ")
        
    @blp.arguments(DataUpdateSchema)    
    def put(self,user_data ,id):
        # user_data = request.get_json()
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
    
    @blp.arguments(DataSchems)
    def post(self,user_data):
        user_data = request.get_json()
        new_data = DataModel(**user_data)
    
        try:
            db.session.add(new_data)
            db.session.commit()
        except SQLAlchemyError as e :
           return abort(500 , message = "EROOR OCCURED with data->. {}".format(e) )
            
                
    
        
    
        return new_data , 201   