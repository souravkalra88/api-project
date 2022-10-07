import uuid
from flask import request  
from flask.views import MethodView
from flask_smorest import Blueprint,abort
from models.dose_info import DoseInfoModel
from db import db
from schemas import DoseInfoUpdateSchema, DoseInfoSchemas
from sqlalchemy.exc import SQLAlchemyError

blp = Blueprint("dose_info" , __name__ , description = "data about dose_info")

@blp.route("/dose_info/<int:dose_id>")
class Dosage_Info(MethodView):  
    @blp.response(200 , DoseInfoSchemas)
    def get(self,dose_id):
        t_dose = DoseInfoModel.query.get_or_404(dose_id)
        return t_dose  
        
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
            
            
    def delete(self, dose_id):
        dose = DoseInfoModel.query.get_or_404(dose_id)
        db.session.delete(dose)
        db.session.commit()
        return {"msg": "deleted dose data successfully"} ,200         


@blp.route("/dose_info")
class DoseList(MethodView):
    @blp.response(200 , DoseInfoSchemas(many = True))
    def get(self):
        return DoseInfoModel.query.all()
     
    
     
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
    
