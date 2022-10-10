from email import message
from pydoc import describe
from flask_jwt_extended import get_jwt, jwt_required
from flask import request  
from flask.views import MethodView
from flask_smorest import Blueprint,abort
from sqlalchemy.exc import SQLAlchemyError
from models import DataModel
from db import db 

from schemas import DataSchems, DataUpdateSchema

blp = Blueprint("data" , __name__ , description = "operations on data. ")

@blp.route("/data/<int:id>")
class Data(MethodView):
    @jwt_required()
    @blp.response(200 ,DataSchems)
    def get(self , id):
        t_data = DataModel.query.get_or_404(id)
        return t_data
    @jwt_required()
    @blp.arguments(DataUpdateSchema)    
    @blp.response(200 ,DataSchems)
    def put(self,t_data ,id):
        t_data = request.get_json()
        user_data = DataModel.query.get_or_404(id)
        
        if user_data :
            user_data.Contact = t_data["Contact"]
            user_data.Gender = t_data["Gender"]
            user_data.dob = t_data["dob"]
        else :
            user_data = DataModel(id = id , **t_data)
        db.session.add(user_data)
        db.session.commit()
                
        return user_data 
            
    @jwt_required()    
    def delete(self , id):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required.")
        user_data = DataModel.query.get_or_404(id)
        db.session.delete(user_data)
        db.session.commit()
        return {"msg": "deleted data successfully"} ,200
    
            
            
@blp.route("/data")
class DataList(MethodView):
    @jwt_required()
    @blp.response(200 , DataSchems(many = True))
    def get(self):
        return DataModel.query.all()    
    
    @jwt_required()
    @blp.arguments(DataSchems)
    @blp.response(201 , DataSchems)
    def post(self,user_data):
        user_data = request.get_json()
        new_data = DataModel(**user_data)
    
        try:
            db.session.add(new_data)
            db.session.commit()
        except SQLAlchemyError as e :
           return abort(500 , message = "EROOR OCCURED with data->. {}".format(e) )
            
        return new_data  