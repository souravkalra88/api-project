from marshmallow import Schema,fields 



class PlainDataSchems(Schema):
    id = fields.Int(dump_only = True)
    Contact = fields.Str(required = True)
    Gender = fields.Str(required = True)
    dob = fields.Str(required = True)
    
class PlainUsersSchema(Schema):
    user_id  = fields.Int(dump_only = True)   
    user_name = fields.Str(required = True)
    _password = fields.Str(required = True)  
    
    
class PLainDoseInfo(Schema):
    dose_id = fields.Int(dump_only = True)
    date_of_vacc = fields.Str(required = True)
    dose_number = fields.Str(required = True)
    name_of_vacc = fields.Str(required = True)      
    
    
class DataUpdateSchema(Schema): 
    
    Contact = fields.Str()
    Gender = fields.Str()
    dob = fields.Str()    
    
class DoseInfoUpdateSchema(Schema):
    date_of_vacc  = fields.Str()   
    dose_number = fields.Int()
    name_of_vacc = fields.Str() 
    
    
class DataSchems(PlainDataSchems):
    user_id = fields.Int(required = True , load_only = True)
    user = fields.Nested(PlainUsersSchema() , dump_only = True)

class UsersSchema(PlainUsersSchema):
    datas = fields.List(fields.Nested(PlainDataSchems(), dump_only = True))
    doses = fields.List(fields.Nested(PLainDoseInfo(), dump_only = True)) 
   
class DoseInfoSchemas(PLainDoseInfo):
    user_id = fields.Int(required = True , load_only = True)
    user = fields.Nested(PlainUsersSchema() , dump_only = True)    
    
        
    
    


   
    
    
    
    
    
class DoseInfoSchemas(Schema):
    dose_id = fields.Str(dump_only = True)
    dose_number = fields.Str(required = True)
    name_of_vacc = fields.Str(required = True)
    date_of_vacc = fields.Str(required = True)
    user_id = fields.Str(required = True)
    
class DoseInfoUpdateSchema(Schema):
    user_id = fields.Str(load_only = True)
    date_of_vacc = fields.Str(required = True)
    dose_number = fields.Str(required = True)
    name_of_vacc = fields.Str(required = True)
            
    
    
class UserLoginSchema(Schema):
    user_id  = fields.Int(dump_only = True)   
    user_name = fields.Str(required = True)
    _password = fields.Str(required = True , load_only = True)    
    