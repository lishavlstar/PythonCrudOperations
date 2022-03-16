import pymysql
from dbconfig import mysql
from passlib.hash import sha256_crypt
import datetime

# checking if the client name is already in use or not
def user_exist(email_id):
	conn = None;
	cursor = None;
	
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		
		sql = "SELECT client_id FROM Client WHERE email_id=%s"
		sql_where = (email_id,)
		
		cursor.execute(sql, sql_where)
		row = cursor.fetchone()
		
		if row:
			return True
		return False

	except Exception as e:
		print(e)

	finally:
		if cursor and conn:
			cursor.close()
			conn.close()

#Storing client details to DB
def register(first_name, last_name, phone_number,email_id, country, city, status, password):
	conn = None;
	cursor = None;
	
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		sql = "INSERT INTO Client(first_name, last_name, phone_number, email_id, country, city, status) VALUES(%s,%s,%s,%s,%s,%s,%s)"
		data = (first_name, last_name, phone_number, email_id, country, city, status,)
		cursor.execute(sql, data)
		conn.commit()

		sql = "SELECT client_id FROM Client WHERE email_id=%s"
		sql_where = (email_id)
		
		cursor.execute(sql, sql_where)
		row = cursor.fetchone()
		client_id = row[0]
		

		sql = "INSERT INTO Client_User_Login(client_id, email_id, password) VALUES(%s,%s,%s)"
		data = (client_id, email_id, sha256_crypt.encrypt(password))
		cursor.execute(sql, data)
		conn.commit()

	except Exception as e:
		print(e)

	finally:
		if cursor and conn:
			cursor.close()
			conn.close()

#Selecting client_id from DB to create folder with client id
def get_id_by_name(email_id):
	conn = None;
	cursor = None;
	
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		
		sql = "SELECT client_id FROM Client WHERE email_id=%s"
		sql_where = (email_id)
		
		cursor.execute(sql, sql_where)
		row = cursor.fetchone()
		data = row[0]
		if data:
			return data
			
		return False

	except Exception as e:
		print(e)

	finally:
		if cursor and conn:
			cursor.close()
			conn.close()

def user_login(email_id, password):
	conn = None;
	cursor = None;
	
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		
		sql = "SELECT email_id, password FROM Client_User_Login WHERE email_id=%s"
		sql_where = (email_id,)
		
		cursor.execute(sql, sql_where)
		row = cursor.fetchone()
		
		if row:
			if sha256_crypt.verify(password, row[1]):
				return True
				
		return None

	except Exception as e:
		print(e)

	finally:
		if cursor and conn:
			cursor.close()
			conn.close()

def update_user(first_name, last_name, phone_number, country, city, email_id):
	conn = None;
	cursor = None;
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		sql = "UPDATE Client SET first_name=%s, last_name=%s, phone_number=%s, country=%s, city=%s WHERE email_id=%s"
		data = (first_name, last_name, phone_number, country, city, email_id)
		cursor.execute(sql, data)
		conn.commit()

	except Exception as e:
		print(e)
	finally:
		if cursor and conn:
			cursor.close()
			conn.close()

def update_password(email_id, password):
	conn = None;
	cursor = None;
	
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		sql = "UPDATE Client_User_Login SET password=%s WHERE email_id=%s"
		data = ( sha256_crypt.encrypt(password), email_id)
		cursor.execute(sql, data)
		conn.commit()

	except Exception as e:
		print(e)

	finally:
		if cursor and conn:
			cursor.close()
			conn.close()

