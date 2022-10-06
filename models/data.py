from enum import unique
from db import db

class DataModel(db.Model):
    __tablename__ = "datas"
    
    id = db.Column(db.Integer , primary_key=True)
    Contact = db.Column(db.String(13) , unique = True , nullable = False)    
    Gender = db.Column(db.String(10) , unique = False , nullable = False)
    dob = db.Column(db.String(25) , unique = False , nullable = False)
    user_id = db.Column(db.Integer,db.ForeignKey("users.user_id") , unique = True , nullable = False)
    users = db.relationship("UserModel" , back_populates = "datas" )
    