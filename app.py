from email.mime import message
import uuid
from flask import Flask,request
from flask_smorest import abort 
from db import users , data

app = Flask(__name__)

# Running on http://127.0.0.1:5000

@app.route("/")
def home():
    return "Hello, Flask!"




@app.get("/user")  
def get_users():
    return {"users" : list(users.values())}

@app.get("/user/<string:user_id>")
def get_user(user_id):
    try:
        return users[user_id]
    except KeyError:
        return abort(404, message = "User not found. ")
@app.get("/data/<string:id>")
def get_user_data(id):
    try:
        return data[id]  
    except KeyError:  
        return abort(404, message = "Data not found. ")



@app.get("/data")  
def get_all_data():
    return {"data" : list(data.values())}


  

@app.post("/user")
def post_user():
    user_data = request.get_json()
    user_id = uuid.uuid4().hex 
    new_user = {**user_data , "user_id" : user_id }
    users[user_id] = new_user
    
    return new_user,201

@app.post("/data")
def create_data():
    user_data = request.get_json()
    if user_data["user_id"] not in users:
        return abort(404 , message="Data not found")
    
    
    id = uuid.uuid4().hex
    new_data = {**user_data , "id" : id}
    data[id]=new_data 
    
    return new_data , 201
    
@app.put("/data/<string:id>")
def update_data(id):
    user_data = request.get_json()
    try:
        t_data = data[id]
        t_data |= user_data
        return t_data
    except KeyError:
        abort(404 , message = "data not found. ")
            
            
        
@app.delete("/user/<string:user_id>")
def delete_user(user_id):
    try:
        del users[user_id]
        return {"msg": "User deleted. "}
    except KeyError:
        abort(404, message = "User not found. ")
        
        
@app.delete("/data/<string:id>")
def delete_user_data(id):
    try:
        del data[id]
        return {"msg": "User Data deleted. "} 
    except KeyError:
        abort(404 , "User Data not found. ")       

              
           