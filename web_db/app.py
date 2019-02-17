from flask import Flask, request, json, jsonify, make_response, abort, session, render_template, redirect, url_for
import dbmanager

app = Flask(__name__)

@app.route('/authcheck', methods=['POST'])
def authcheck():
    login=request.form['login']
    passw = request.form['password']
    us=dbmanager.auth(login,passw)
    if(len(us)>0):
        session['login'] = us[0][1].decode("utf-8")
        session['priv']=us[0][3]
        return redirect(url_for('dash'))
    else:
    	text2 = "Неверный логин/пароль"
    	text3 = "Проверьте правильность заполнения полей!"
    	title = "Ошибка!"
    	return render_template('action.html',text3 = text3, text2 = text2, title = title)

@app.route('/dashboard')
def dash():
	if 'login' not in session:
		return redirect(url_for('auth'))
	if(session.get('priv')==1):
		return render_template('index.html')
	else:
		return render_template('index.html', user=1)
	

@app.route('/')
def auth():
    if 'login' not in session:
    	return render_template("auth.html")
    return redirect(url_for('dash'))
    

@app.route('/reg')
def reg():
    if 'login' in session:
        return redirect(url_for('dash'))
    return render_template("signin.html")

@app.route('/logout')
def logout():
    session.pop('login', None)
    session.pop('priv', None)
    session.pop('user_id', None)  
    return redirect(url_for('auth'))

@app.route('/regcheck', methods = ['POST'])
def regcheck():
	login=request.form['login']
	passw = request.form['password']
	reg = dbmanager.regusers(login,passw)
	if reg == True:
		text3 = "Пользователь успешно зарегестрирован!"
		return render_template('action.html',text3 = text3)
	else:
		text3 = "Такой пользователь уже существует."
		return render_template('action.html',text3 = text3)





#start pages

@app.route('/services',)
def services():
	if 'login' not in session:
		return redirect(url_for('auth'))
	if(session.get('priv')==1):
		return render_template('services.html')
	else:
		return render_template('services.html', user=1)

@app.route('/doctors',)
def doctors():
	if 'login' not in session:
		return redirect(url_for('auth'))
	if(session.get('priv')==1):
		return render_template('doctors.html')
	else:
		return render_template('doctors.html', user=1)

@app.route('/patients',)
def patients():
	if 'login' not in session:
		return redirect(url_for('auth'))
	if(session.get('priv')==1):
		return render_template('patients.html')
	return redirect(url_for('dash'))

@app.route('/records',)
def records():
	if 'login' not in session:
		return redirect(url_for('auth'))
	if(session.get('priv')==1):
		return render_template('records.html')
	return redirect(url_for('dash'))

@app.route('/stats')
def stats():
	if 'login' not in session:
		return redirect(url_for('auth'))
	reslist1 = dbmanager.stats1()
	reslist2 = dbmanager.stats2()
	reslist3 = dbmanager.stats3()
	return render_template('stats.html',reslist1=reslist1,reslist2 = reslist2, reslist3 = reslist3)



#Add pages
@app.route('/addpatients', methods = ['POST', 'GET'])
def addpatients():
	if 'login' not in session:
		return redirect(url_for('auth'))
	if(session.get('priv')==0):
		return redirect(url_for('dash'))
	if request.method == 'POST':
		checkres = dbmanager.insertPatient(request.form['patientname'], request.form['patientdate'])
		if checkres == True:
			title = "Успешно!"
			text3 = "Вы успешно добавили пациента!"
			return render_template('action.html', text3 = text3, title = title)
		else:
			title = "Неудачно!"
			text2 = "Во время добавления произошла ошибка."
			text3 = "Проверьте правильность заполнения полей!"
			return render_template('action.html', text2 = text2,text3 = text3, title = title)
	else:
		return render_template('addpatients.html')

@app.route('/adddoctors', methods=['POST', 'GET'])
def adddoctors():
	if 'login' not in session:
		return redirect(url_for('auth'))
	if(session.get('priv')==0):
		return redirect(url_for('dash'))
	if request.method == 'POST':
		checkres = dbmanager.insertDoctor(request.form['doctorname'], request.form['doctorinfo'])
		if checkres == True:
			title = "Успешно!"
			text3 = "Вы успешно добавили доктора!"
			return render_template('action.html', text3 = text3, title = title)
		else:
			title = "Неудачно!"
			text2 = "Во время добавления произошла ошибка."
			text3 = "Проверьте правильность заполнения полей!"
			return render_template('action.html', text2 = text2,text3 = text3, title = title)
	else:
		return render_template('adddoctors.html')

@app.route('/addservices', methods = ['POST','GET'])
def addservices():
	if 'login' not in session:
		return redirect(url_for('auth'))
	if(session.get('priv')==0):
		return redirect(url_for('dash'))
	if request.method == 'POST':
		checkres = dbmanager.InsertService(request.form['servicename'], request.form['serviceprice'])
		if checkres == True:
			title = "Успешно!"
			text3 = "Вы успешно добавили услугу!"
			return render_template('action.html', text3 = text3, title = title)
		else:
			title = "Неудачно!"
			text2 = "Во время добавления произошла ошибка."
			text3 = "Проверьте правильность заполнения полей!"
			return render_template('action.html', text2 = text2,text3 = text3, title = title)
	else:
		return render_template('addservices.html')

@app.route('/addrecords', methods=['POST','GET'])
def addrecords():
	if 'login' not in session:
		return redirect(url_for('auth'))
	if(session.get('priv')==0):
		return redirect(url_for('dash'))
	if request.method == 'POST':
		checkres = dbmanager.InsertRecords(request.form['recorddate'], request.form['patients_code'],request.form['doctors_code'],request.form['services_code'],request.form['price'])
		if request.form['patients_code'] == "Выберите имя пациента" or \
		request.form['doctors_code'] == "Выберите имя доктора" or \
		request.form['services_code'] == "Выберите название услуги":
			title = "Неудачно!"
			text2 = "Во время добавления произошла ошибка."
			text3 = "Необходимо выбрать доктора/пациента/запись!"
			return render_template('action.html', text2 = text2,text3 = text3, title = title)
		if checkres == True:
			title = "Успешно!"
			text3 = "Вы успешно добавили запись!"
			return render_template('action.html', text3 = text3, title = title)
		else:
			title = "Неудачно!"
			text2 = "Во время добавления произошла ошибка."
			text3 = "Проверьте правильность заполнения полей!"
			return render_template('action.html', text2 = text2,text3 = text3, title = title)
	else:
		reslist = dbmanager.SelectIdServices()
		reslist2 = dbmanager.SelectIdPatient()
		reslist3= dbmanager.SelectIdDoctor()
		return render_template('addrecords.html',reslist = reslist,reslist2 =reslist2,reslist3 = reslist3)






#Select pages
@app.route('/slpatients', methods=['POST','GET'])
def slpatients():
	if 'login' not in session:
		return redirect(url_for('auth'))
	if(session.get('priv')==0):
		return redirect(url_for('dash'))
	if request.method == 'POST':		
		reslist = dbmanager.SelectPatients(request.form['patients_code'],request.form['date'])
		if len(reslist)==0:
			title = "Неудачо!"
			text3 = "Такого пациента не существует!"
			return render_template('action.html',title = title,text3 = text3)
		else:
			return render_template('checkpatients.html',reslist = reslist)
	else:
		reslist = dbmanager.SelectIdPatient()
		return render_template('slpatients.html',reslist = reslist)

@app.route('/patient/<idd>',methods=['GET'])
def patient(idd):
	if 'login' not in session:
		return redirect(url_for('auth'))
	if(session.get('priv')==0):
		return redirect(url_for('dash'))
	reslist = dbmanager.SelectPatients(idd,'')
	if len(reslist)==0:
		title = "Неудачо!"
		text3 = "Такого доктора не существует!"
		return render_template('action.html',title = title,text3 = text3)
	else:
		return render_template('checkpatients.html',reslist = reslist)

@app.route('/slrecords',methods=['POST','GET'])
def slrecords():
	if 'login' not in session:
		return redirect(url_for('auth'))
	if(session.get('priv')==0):
		return redirect(url_for('dash'))
	if request.method == 'POST':
			reslist = dbmanager.SelectRecords(request.form['act_num'],request.form['service_date'],\
				request.form['services_code'],request.form['patients_code'],request.form['doctors_code'],request.form['price'])
			if len(reslist)==0:
				title = "Неудачно!"
				text2 = "Запись не найдена."
				text3 = "Проверьте правильность заполнения полей!"
				return render_template('action.html',title = title,text3 = text3, text2 = text2)
			else:
				return render_template('checkrecords.html',reslist = reslist)
	else:
		reslist = dbmanager.SelectIdRecord()
		reslist1 = dbmanager.SelectIdServices()
		reslist2 = dbmanager.SelectIdPatient()
		reslist3 = dbmanager.SelectIdDoctor()
		return render_template('slrecords.html',reslist = reslist, reslist1 = reslist1, reslist2 = reslist2, reslist3 = reslist3)




@app.route('/sldoctors',methods=['POST','GET'])
def sldoctors():
	if 'login' not in session:
		return redirect(url_for('auth'))
	if request.method == 'POST':
			reslist = dbmanager.SelectDoctors(request.form['doctors_code'],request.form['info'])
			if len(reslist)==0:
				title = "Неудачо!"
				text3 = "Такого доктора не существует!"
				return render_template('action.html',title = title,text3 = text3)
			else:
				if(session.get('priv')==0):
					return render_template('checkdoctors.html',reslist = reslist, user=1)
				return render_template('checkdoctors.html',reslist = reslist)
	else:
		reslist = dbmanager.SelectIdDoctor()
		return render_template('sldoctors.html',reslist = reslist)

@app.route('/doctor/<idd>',methods=['GET'])
def doctor(idd):
	if 'login' not in session:
		return redirect(url_for('auth'))
	reslist = dbmanager.SelectDoctors(idd,'')
	if len(reslist)==0:
		title = "Неудачо!"
		text3 = "Такого доктора не существует!"
		return render_template('action.html',title = title,text3 = text3)
	else:
		if(session.get('priv')==0):
			return render_template('checkdoctors.html',reslist = reslist, user=1)
		return render_template('checkdoctors.html',reslist = reslist)

@app.route('/slservices',methods=['POST','GET'])
def slservices():
	if 'login' not in session:
		return redirect(url_for('auth'))
	if request.method == 'POST':	
			reslist = dbmanager.SelectServices(request.form['services_code'],request.form['price'])
			if len(reslist)==0:
				title = "Неудачо!"
				text3 = "Такой услуги не существует!"
				return render_template('action.html',title = title,text3 = text3)
			else:
				if(session.get('priv')==0):
					return render_template('checkservices.html',reslist = reslist, user=1)
				return render_template('checkservices.html',reslist = reslist)
	else:	
		reslist = dbmanager.SelectIdServices()
		return render_template('slservices.html',reslist = reslist)

@app.route('/service/<idd>',methods=['GET'])
def service(idd):
	if 'login' not in session:
		return redirect(url_for('auth'))
	reslist = dbmanager.SelectServices(idd,'')
	if len(reslist)==0:
		title = "Неудачо!"
		text3 = "Такой услуги не существует!"
		return render_template('action.html',title = title,text3 = text3)
	else:
		if(session.get('priv')==0):
			return render_template('checkservices.html',reslist = reslist, user=1)
		return render_template('checkservices.html',reslist = reslist)




#Delete pages
@app.route('/rmpatients',methods = ['POST'])
def rmpatients():
	if 'login' not in session:
		return redirect(url_for('auth'))
	if(session.get('priv')==0):
		return redirect(url_for('dash'))
	dbmanager.RemovePatients(request.form['patients_code'])
	title = "Успешно!"
	text3 = "Вы успешно удалили пациента!"
	return render_template('action.html', text3 = text3, title = title)
	

@app.route('/rmdoctors',methods = ['POST'])
def rmdoctors():
	if 'login' not in session:
		return redirect(url_for('auth'))
	if(session.get('priv')==0):
		return redirect(url_for('dash'))	
	dbmanager.RemoveDoctors(request.form['doctors_code'])	
	title = "Успешно!"
	text3 = "Вы успешно удалили доктора!"
	return render_template('action.html', text3 = text3, title = title)	

@app.route('/rmservices', methods = ['POST'])
def rmservices():
	if 'login' not in session:
		return redirect(url_for('auth'))
	if(session.get('priv')==0):
		return redirect(url_for('dash'))	
	dbmanager.RemoveServices(request.form['services_code'])
	title = "Успешно!"
	text3 = "Вы успешно удалили услугу!"
	return render_template('action.html', text3 = text3, title = title)
	

@app.route('/rmrecords', methods = ['POST'])
def rmrecords():
	if 'login' not in session:
		return redirect(url_for('auth'))
	if(session.get('priv')==0):
		return redirect(url_for('dash'))
	dbmanager.RemoveRecords(request.form['act_num'])
	title = "Успешно!"
	text3 = "Вы успешно удалили запись!"
	return render_template('action.html', text3 = text3, title = title)
	
	
app.secret_key = 'A0Zr97j/3yX R~XHY!jmN]LWX/,?RT'


if __name__ == '__main__':
    app.run(debug=True)


