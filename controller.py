try:
    from app import app
    import dao
    from flask import request,jsonify,Response,json, session
    import os
    from datetime import datetime
    import uuid
    from google.cloud import storage
    import pymysql
    from dbconfig import mysql
    import re
    from os import environ

except Exception as e:
    
    print('some of the modules are not imported.')

#Createing Client  as well as storing the data to the db

def createClient():    
    try:        
        client_details = request.get_json()     
        first_name = client_details["first_name"]
        last_name = client_details["last_name"]
        phone_number = client_details["phone_number"]
        email_id = client_details["email_id"]
        country = client_details["country"]
        city = client_details["city"]
        status = client_details["status"]
        password = client_details["password"]
        if first_name and last_name and phone_number and email_id and country and city and status and password:
            
            user_exist = dao.user_exist(email_id)
            if user_exist is True:
                status_code = Response(status=409)
                return json.dumps({'Status':False,'message':'You are already registerd, Please Login'}), 409, {'ContentType':'application/json'}
            else:
                
                dao.register(first_name, last_name, phone_number,email_id, country, city, status, password)
                id = dao.get_id_by_name(email_id)
                status_code = Response(status=200)
                return json.dumps({"Status":True,"message":"You have successfully registered"}), 200, {'ContentType':'application/json'}
        else:
            status_code = Response(status=400)
            return json.dumps({"message":"Bad parameters"}), 400, {'ContentType':'application/json'}
    except Exception as e:
        
        return json.dumps({'message':'client creation failed'})


def login():
    try:
        login_details = request.get_json()
        email_id = login_details["email_id"]
        password = login_details["password"]
        user_exist = dao.user_exist(email_id)
        if email_id and password:
            if user_exist is True:
                user = dao.user_login(email_id, password)
                if user is True:
                    status_code = Response(status=200)
                    return json.dumps({"Status":True,"message":"you have successfully Loggedin"}), 200, {'ContentType':'application/json'}
            else:
                status_code = Response(status=400)
                return json.dumps({"Status":False,"message":"Please Register"}), 400, {'ContentType':'application/json'}

        status_code = Response(status=400)
        return json.dumps({"Status":False,"message":"Bad parameters - invalid credentials"}), 400, {'ContentType':'application/json'}
    except Exception as e:
        print(e)
        return json.dumps({'message':'Some errors are there'})


def update():    
    try:
        client_details = request.get_json()     
        first_name = client_details["first_name"]
        last_name = client_details["last_name"]
        phone_number = client_details["phone_number"]
        country = client_details["country"]
        city = client_details["city"]
        email_id = client_details["email_id"] 
        if first_name and last_name and phone_number and country and city and email_id:
            user_exist = dao.user_exist(email_id)
            if user_exist is True:
                dao.update_user(first_name, last_name, phone_number, country, city, email_id)
                status_code = Response(status=200)
                return json.dumps({"Status":True,"message":"Updated!!"}), 200, {'ContentType':'application/json'}
            else:
                status_code = Response(status=400)
                return json.dumps({"Status":False,"message":"Please Register"}), 400, {'ContentType':'application/json'}
        else:
            status_code = Response(status=400)
            return json.dumps({"Status":False,"message":"Null values are not allowed"}), 400, {'ContentType':'application/json'}
    except Exception as e:
        print(e)
        return json.dumps({'message':'Some errors are there'})
    
    
def passwordUpdate():
    try:
        password_details = request.get_json()
        email_id = password_details["email_id"]
        old_password = password_details["old_password"]
        new_password = password_details["new_password"]
        user_exist = dao.user_exist(email_id)
        if email_id and old_password and new_password:
            if user_exist is True:
                user = dao.user_login(email_id, old_password)
                if user is True:
                    dao.update_password(email_id, new_password)
                    status_code = Response(status=200)
                    return json.dumps({"Status":True,"message":"Password is updated"}), 200, {'ContentType':'application/json'}
            else:
                status_code = Response(status=400)
                return json.dumps({"Status":False,"message":"Please Register"}), 400, {'ContentType':'application/json'}
        status_code = Response(status=400)
        return json.dumps({"Status":False,"message":"Bad parameters - invalid credentials"}), 400, {'ContentType':'application/json'}
    except Exception as e:
        print(e)
        return json.dumps({'message':'Some errors are there'})
    
def forgotPassword():
    try:
        password_details = request.get_json()
        email_id = password_details["email_id"]
        new_password = password_details["new_password"]
        user_exist = dao.user_exist(email_id)
        if email_id and new_password:
            if user_exist is True:
                dao.update_password(email_id, new_password)
                status_code = Response(status=200)
                return json.dumps({"Status":True,"message":"Password is updated"}), 200, {'ContentType':'application/json'}
            else:
                status_code = Response(status=400)
                return json.dumps({"Status":False,"message":"Please Register"}), 400, {'ContentType':'application/json'}
        status_code = Response(status=400)
        return json.dumps({"Status":False,"message":"Bad parameters - invalid credentials"}), 400, {'ContentType':'application/json'}
    except Exception as e:
        print(e)
        return json.dumps({'message':'Some errors are there'})
        
    
    
	
        
		
            
            
            
	
    
    


