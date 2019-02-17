import mysql.connector
from mysql.connector.cursor import MySQLCursorPrepared
from datetime import datetime
import re
#pip install mysql-connector-python-rf
#https://pynative.com/python-mysql-execute-parameterized-query-using-prepared-statement/ 
#https://github.com/mysql/mysql-connector-python/blob/master/examples/prepared_statements.py - prepared и обычные запросы
#https://pynative.com/python-mysql-select-query-to-fetch-data/ - select


def getConnection():
	#192.168.64.2
    config = {'host': 'localhost','port': 3306,'database': 'paid_treatment','user': 'root','password': '','charset': 'utf8','use_unicode': True,'get_warnings': True}
    connection=mysql.connector.Connect(**config)
    return connection

def regusers(login,password):
	connection=getConnection()
	cursor = connection.cursor(cursor_class=MySQLCursorPrepared)
	checkuser = False
	query = "SELECT users_id FROM users WHERE login = %s"
	cursor.execute(query,(login,))
	records = cursor.fetchall()
	if (len(records)==0):		
		query = "INSERT INTO users (login, password, priv) VALUES (%s, %s, %s)"
		cursor.execute(query, (login,password,0))
		connection.commit()
		checkuser = True
	return checkuser

def auth(login,password):
	connection=getConnection()
	cursor = connection.cursor(cursor_class=MySQLCursorPrepared)
	prepstmt = "SELECT * FROM users WHERE login = %s and password = %s"
	cursor.execute(prepstmt, (login,password))
	records = cursor.fetchall()		
	connection.close()
	return records

def getUserByLogin(login):
	connection=getConnection()
	cursor = connection.cursor()
	prepstmt = "SELECT users_Id FROM users WHERE login = %s"
	cursor.execute(prepstmt, (login,))
	records = cursor.fetchall()
	connection.close()
	return reslist

def insertDoctor(name, info):
	checkres = True
	try:
		connection=getConnection()
		curprep = connection.cursor(cursor_class=MySQLCursorPrepared)
		prepstmt = "INSERT INTO doctor (doctors_name, info) VALUES (%s, %s)"
		curprep.execute(prepstmt, (name,info))
		connection.commit()
	except Exception as e:
		checkres=False
		print(e)
		return checkres
	else:
		return checkres

def insertPatient(name, birthday_date):
	checkres = True
	try:
		connection=getConnection()
		curprep = connection.cursor(cursor_class=MySQLCursorPrepared)
		prepstmt = "INSERT INTO patient (patients_name, birthday_date) VALUES (%s,%s)"
		bdate=datetime.strptime(birthday_date, '%d.%m.%Y').strftime('%Y-%m-%d')
		curprep.execute(prepstmt, (name,bdate))
		connection.commit()
	except Exception as e: 
		checkres=False
		print(e)
		return checkres
	else:
		return checkres	

def InsertService(name, price):
	checkres = True
	try:
		connection=getConnection()
		curprep = connection.cursor(cursor_class=MySQLCursorPrepared)
		prepstmt = "INSERT INTO service (services_name, price) VALUES (%s,%s)"
		curprep.execute(prepstmt, (name,price))
		connection.commit()
	except Exception as e:
		checkres=False
		print(e)
		return checkres
	else:
		return checkres

def InsertRecords(recorddate,idpat,iddoc,idser,price):
	checkres = True
	try:
		connection=getConnection()
		curprep = connection.cursor(cursor_class=MySQLCursorPrepared)	
		prepstmt = "INSERT INTO rendering_service (service_date,services_code,price,patient_code,doctors_code)\
		VALUES (%s,%s,%s,%s,%s)"
		#bdate=datetime.strptime(recorddate, '%d.%m.%Y').strftime('%Y-%m-%d')
		curprep.execute(prepstmt, (recorddate,idser,price,idpat,iddoc))
		connection.commit()
	except Exception as e:
		checkres=False
		print(e)
		return checkres
	else:
		return checkres





def SelectPatients(patients_code, date):
	if date == "":
		date = "%"

	connection = getConnection()
	cursor=connection.cursor(cursor_class=MySQLCursorPrepared)
	prepstmt = "SELECT patients_code,patients_name,birthday_date FROM patient\
	WHERE patients_code like %s and birthday_date like %s"
	cursor.execute(prepstmt,(patients_code,date))		
	records = cursor.fetchall()	
	connection.close()	
	return records

def SelectDoctors(doctors_code,info):
	if info == "":
		info = "%"

	connection = getConnection()
	cursor=connection.cursor(cursor_class=MySQLCursorPrepared)
	prepstmt = "SELECT doctors_code,doctors_name,info FROM doctor WHERE doctors_code like %s and info like %s"
	cursor.execute(prepstmt,(doctors_code,info))		
	records = cursor.fetchall()		
	connection.close()	
	return records

def SelectServices(services_code,price):

	if price == "":
		price = "%"

	connection = getConnection()
	cursor=connection.cursor(cursor_class=MySQLCursorPrepared)
	prepstmt = "SELECT services_code,services_name,price FROM service WHERE services_code like %s and price like %s"
	cursor.execute(prepstmt,(services_code,price))		
	records = cursor.fetchall()		
	connection.close()
	return records

def SelectRecords(act_num, service_date,services_code,patients_code,doctors_code,price ):
	if service_date == "":
		service_date = "%"

	if price == "":
		price="%"

	connection = getConnection()
	cursor=connection.cursor(cursor_class=MySQLCursorPrepared)
	prepstmt = "SELECT act_num, service_date, rs.services_code, services_name, rs.patient_code, patients_name, rs.doctors_code, doctors_name, rs.price\
	FROM rendering_service rs JOIN doctor d JOIN patient p JOIN service s\
	 WHERE act_num like %s and service_date like %s and rs.services_code like %s \
	 and rs.patient_code like %s and rs.doctors_code like %s and rs.price like %s\
	 and rs.services_code = s.services_code and rs.doctors_code = d.doctors_code and rs.patient_code = p.patients_code"	
	cursor.execute(prepstmt,(act_num,service_date,services_code,patients_code,doctors_code,price))
	records = cursor.fetchall()
	connection.close()
	return records

def RemoveDoctors(doctors_code):
	connection = getConnection()
	cursor=connection.cursor(cursor_class=MySQLCursorPrepared)
	prepstmt = "DELETE FROM doctor WHERE doctors_code = %s"
	cursor.execute(prepstmt,(doctors_code,))
	connection.commit()


def RemovePatients(patients_code):
	connection = getConnection()
	cursor=connection.cursor(cursor_class=MySQLCursorPrepared)
	prepstmt = "DELETE FROM patient WHERE patients_code = %s"
	cursor.execute(prepstmt,(patients_code,))
	connection.commit()
	
def RemoveRecords(act_num):
	connection = getConnection()
	cursor=connection.cursor(cursor_class=MySQLCursorPrepared)
	prepstmt = "DELETE FROM rendering_service  WHERE act_num = %s"
	cursor.execute(prepstmt,(act_num,))
	connection.commit()
	

def RemoveServices(services_code):
	connection = getConnection()
	cursor=connection.cursor(cursor_class=MySQLCursorPrepared)
	prepstmt = "DELETE FROM service WHERE services_code = %s"
	cursor.execute(prepstmt,(services_code,))
	connection.commit()





def SelectIdDoctor():
	connection = getConnection()
	cursor=connection.cursor()
	query = "SELECT doctors_code,doctors_name FROM doctor"
	cursor.execute(query,)
	records = cursor.fetchall()
	connection.close()
	return records


def SelectIdPatient():
	connection = getConnection()
	cursor=connection.cursor()
	query = "SELECT patients_code,patients_name FROM patient"
	cursor.execute(query,)
	records = cursor.fetchall()
	connection.close()
	return records

def SelectIdServices():
	connection = getConnection()
	cursor=connection.cursor()
	query = "SELECT services_code,services_name,price FROM service"
	cursor.execute(query,)
	records = cursor.fetchall()
	connection.close()
	return records

def SelectIdRecord():
	connection = getConnection()
	cursor=connection.cursor()
	query = "SELECT act_num FROM rendering_service"
	cursor.execute(query,)
	records = cursor.fetchall()
	connection.close()
	return records


#проверка на правильность вводимой строки
def RegularCheck(query):
	regul = False
	pattern= "^[A-Za-z_-]*$"
	if re.match(pattern,query):
		regul = True
	print(re.match(pattern,query))
	return regul

	
def stats1():
	connection = getConnection()
	cursor=connection.cursor()
	query = "SELECT count(*) FROM doctor"
	cursor.execute(query,)
	records = cursor.fetchall()
	connection.close()
	return records

def stats2():
	connection = getConnection()
	cursor=connection.cursor()
	query = "SELECT count(*) FROM rendering_service"
	cursor.execute(query,)
	records = cursor.fetchall()
	connection.close()
	return records

def stats3():
	connection = getConnection()
	cursor=connection.cursor()
	query = "SELECT count(*) FROM service"
	cursor.execute(query,)
	records = cursor.fetchall()
	connection.close()
	return records

def findPrice(services_code):
	connection = getConnection()
	cursor=connection.cursor()
	query = "SELECT price FROM service where services_code = %s"
	cursor.execute(query,(services_code,))
	records = cursor.fetchall()
	connection.close()
	return records

	



#<p><img src = "image/folded-paper.png"></p>
