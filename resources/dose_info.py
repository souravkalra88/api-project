import uuid
from flask import request  
from flask.views import MethodView
from flask_smorest import Blueprint,abort

from schemas import DoseInfoUpdateSchema, DoseInfoSchemas

blp = Blueprint("dose_info" , __name__ , description = "data about dose_info")

@blp.route("/dose_info/<string:dose_id>")
class Dosage_Info(MethodView):  
    def get(self,dose_id):
        try:
            return dose_info[dose_id]  
        except KeyError:  
            return abort(404, message = "Data not found. ")
        
    @blp.arguments(DoseInfoUpdateSchema)     
    def put(self,dose ,dose_id):
        try:
            # dose = request.get_json()
            t_dose = dose_info[dose_id]
            t_dose |= dose 
            return t_dose
        except KeyError:
            abort(404 , message = "Dose_Info not found. ") 
            
    def delete(self, dose_id):
        try:
            del dose_info[dose_id]
            return {"msg": "User Dose_Data deleted. "} 
        except KeyError:
            abort(404 , "User Data not found. ")        


@blp.route("/dose_info")
class DoseList(MethodView):
    def get(self):
        return {"dose_info" : list(dose_info.values())} 
    
    @blp.arguments(DoseInfoSchemas)
    def post(self,dose):
        
        if dose["user_id"] not in users :
            return abort(404 , message="Dose_info not found") 
        
        else:
            for doses in dose_info.values():
                if dose["user_id"] == doses["user_id"] and dose["name_of_vacc"] == doses["name_of_vacc"] and dose["dose_number"] == doses["dose_number"] :
                    return abort(404 , message="Duplicate DoseInfo exists")
           
                
        
        dose_id = uuid.uuid4().hex
        new_dose_data = {**dose , "dose_id" : dose_id}
        dose_info[dose_id]= new_dose_data
    
        return new_dose_data , 201   
    
