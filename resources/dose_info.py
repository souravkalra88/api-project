import uuid
from flask import request  
from flask.views import MethodView
from flask_jwt_extended import get_jwt, jwt_required
from flask_smorest import Blueprint,abort
from models.dose_info import DoseInfoModel
from db import db
from schemas import DoseInfoUpdateSchema, DoseInfoSchemas
from sqlalchemy.exc import SQLAlchemyError

blp = Blueprint("dose_info" , __name__ , description = "data about dose_info")

@blp.route("/dose_info/<int:dose_id>")
class Dosage_Info(MethodView):  
    @jwt_required()
    @blp.response(200 , DoseInfoSchemas)
    def get(self,dose_id):
        t_dose = DoseInfoModel.query.get_or_404(dose_id)
        return t_dose  
    @jwt_required()    
    @blp.arguments(DoseInfoUpdateSchema) 
    @blp.response(200 ,DoseInfoSchemas)    
    def put(self,t_dose ,dose_id):
        t_dose = request.get_json()
        dose = DoseInfoModel.query.get_or_404(dose_id)
        
        if dose :
            dose.date_of_vacc = t_dose["date_of_vacc"]
            dose.dose_number = t_dose["dose_number"]
            dose.name_of_vacc = t_dose["name_of_vacc"]
            
        else :
            dose = DoseInfoModel(dose_id = dose_id , **t_dose) 
        
        db.session.add(dose)
        db.session.commit()
        
        return dose        
            
    @jwt_required()        
    def delete(self, dose_id):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required.")
        
        dose = DoseInfoModel.query.get_or_404(dose_id)
        db.session.delete(dose)
        db.session.commit()
        return {"msg": "deleted dose data successfully"} ,200         


@blp.route("/dose_info")
class DoseList(MethodView):
    @jwt_required()
    @blp.response(200 , DoseInfoSchemas(many = True))
    def get(self):
        return DoseInfoModel.query.all()
     
    
    @jwt_required() 
    @blp.response(201 , DoseInfoSchemas)
    def post(self):
        
        dose = request.get_json()
        n_dose = DoseInfoModel(**dose)
        
        try:
            db.session.add(n_dose)
            db.session.commit()
            
        except SQLAlchemyError as e :
           return abort(500 , message = "EROOR OCCURED with dose_data->. {}".format(e) )    
    
        return n_dose  
    
