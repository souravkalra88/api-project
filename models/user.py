from db import db

class UserModel(db.Model):
    __tablename__ = "users"
    
    user_name = db.Column(db.String(255)  ,unique = True , nullable=False)
    _password = db.Column(db.String(255) ,unique = False ,  nullable=False)
    user_id = db.Column(db.Integer, primary_key=True)
    datas = db.relationship("DataModel", back_populates="users")
    doses = db.relationship("DoseInfoModel", back_populates="users")
    
    
    