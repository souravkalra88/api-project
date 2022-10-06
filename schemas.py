from marshmallow import Schema,fields 


class DataSchems(Schema):
    id = fields.Str(dump_only = True)
    Contact = fields.Str(required = True)
    Gender = fields.Str(required = True)
    dob = fields.Str(required = True)
    user_id = fields.Str(required = True)
    
class DataUpdateSchema(Schema): 
    user_id = fields.Str(load_only = True)
    Contact = fields.Str()
    Gender = fields.Str()
    dob = fields.Str()    
    
class UsersSchema(Schema):
    id  = fields.Str(dump_only = True)   
    user_name = fields.Str(required = True)
    _password = fields.Str(required = True)
    