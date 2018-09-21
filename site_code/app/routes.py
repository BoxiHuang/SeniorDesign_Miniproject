from app import app
from flask import render_template, flash, redirect, url_for,session, request
import datetime, time
from app.forms import LoginForm
from app.forms import RegistrationForm
from app.forms import SensorSubmitForm
from app.forms import SelectSensorForm
from app.forms import DataEntry
from app import db
from app.models import User, Data, Sensor
from flask_login import current_user, login_user
from flask_login import logout_user
from flask_login import login_required
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
import boto3
import json
import webbrowser
from urllib.request import urlopen
client = boto3.client('lambda',region_name='us-east-1',aws_access_key_id='AKIAIXH6VKQF4EJMORFA',
    aws_secret_access_key='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')
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    st = ""
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    form = SensorSubmitForm()
    user_id = session["user_id"]
    user = User.query.filter_by(id=user_id).first()
    this_sensor = Sensor.query.filter_by(user_id=user_id).first()
    thisForm = SelectSensorForm(form_name='SelectSensorForm')
    thisForm.sensor_select.choices = [(row.id, row.name) for row in Sensor.query.filter_by(user_id=user_id).all()]
    if form.validate_on_submit():
        sensor = Sensor(name=form.sensor_name.data,user_id=user_id)
        db.session.add(sensor)
        db.session.commit()
        return redirect(url_for('index'))
    sensor_list = Sensor.query.filter_by(user_id=user_id).all()
    my_sensor = thisForm.sensor_select.data
    data = Data.query.filter_by(sensor_id=my_sensor).all()
    thisurl = plotGraph(data)
    if thisurl != 'none':
        print(thisurl)
        newstr = thisurl[:0] + thisurl[1:]
        st = newstr[:-1]
        print(st)
        return render_template('index.html',user=user,sensor_display=this_sensor,form=form,thisForm = thisForm,sensor_list = sensor_list,inurl = st)
    return render_template('index.html',user=user,sensor_display=this_sensor,form=form,thisForm = thisForm,sensor_list = sensor_list,inurl = st)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/registration',methods=['GET','POST'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None:
            return render_template('reg.html',title='Register',form=form)
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('reg.html', title='Register', form=form)

@app.route('/enter-data',methods=['GET','POST'])
def dataEntry():
    form = DataEntry()
    if form.validate_on_submit():
        sensor = Sensor.query.filter_by(name=form.sensorName.data).first()
        data = Data(temp=form.temperature.data, humidity=form.humidity.data,sensor_id=sensor.id)
        db.session.add(data)
        db.session.commit()
        return redirect(url_for('dataEntry'))
    return render_template('enter-data.html',form=form)




def plotGraph(data):
   # response = client.invoke(
     #   ClientContext='MyApp',
    #    FunctionName='MyFunction',
     #   InvocationType='Event',
     #   LogType='Tail',
      #  Payload='fileb://file-path/input.json',
      #  Qualifier='1',
   # )
    try:
        gotdata = data
    except IndexError:
        gotdata = 'null'
    if gotdata != 'null':
        humidity = [None] *len(data)
        temp = [None] * len(data)
        t_ime = [None] * len(data)
        i = 0
        for row in data:
            humidity[i] = row.humidity
            temp[i] = row.temp
            t_ime[i]=time.mktime(row.time.timetuple())
            i = i+1
            print(t_ime)    
        humidity1 = ''.join(str(x) for x in humidity)
        time1 = ''.join(str(x) for x in temp)
        temp1 = ''.join(str(x) for x in t_ime)
        response = client.get_account_settings()
        print(response)
        data = {'temp':temp,'humidity':humidity,'time':t_ime}
        print(data)
        data_json = json.dumps(data)
        response = client.invoke(
            FunctionName='bobocandoit',
            InvocationType='RequestResponse',
            Payload=data_json,
        )

        thisresponse = response['Payload'].read()
        print(thisresponse)
        return(thisresponse)
    else:
        return('none')
