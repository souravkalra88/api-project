from db import db 
 
class DoseInfoModel(db.Model):
    __tablename__ = "doses"
    
    dose_id = db.Column(db.Integer , primary_key=True)
    date_of_vacc = db.Column(db.String(13) , unique = False , nullable = False)
    dose_number = db.Column(db.Integer , unique = False , nullable = False)
    name_of_vacc = db.Column(db.Integer , unique = False , nullable = False)
    user_id = db.Column(db.Integer,db.ForeignKey("users.user_id") , unique = True , nullable = False)
    users = db.relationship("UserModel" , back_populates = "doses" ) 