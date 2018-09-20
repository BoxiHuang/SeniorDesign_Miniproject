from __future__ import print_function
import json
#from app import app
#from flask import render_template, flash, redirect, url_for,session
#from app.forms import LoginForm
#from app.forms import RegistrationForm
#from app.forms import SensorSubmitForm
#from app import db
#from app.models import User, Data, Sensor
#from flask_login import current_user, login_user
#from flask_login import logout_user
#from flask_login import login_required
#from flask_wtf import FlaskForm
#from wtforms import StringField, PasswordField, BooleanField, SubmitField
#from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

print('Loading function')

def lambda_handler(event, context):

	#if form == LoginForm():
		#if form.validate_on_submit():
		print("Hello, User "  + event.data('key1'))					#Need to update "event.data()" to fit project database
		print("Sensor Name is " +  event.data('key2'))
		print("temperature record = " + event.data('key3'))
		print("humidity record = " + event.data('key4'))

	#elif form == SensorSubmitForm():
		#if form.validate_on_submit():
		print('Congrats, You have successfully created sensor!')

	#elif form == RegistrationForm():
		#if form.validate_on_submit():
		print('Congrats, You are now a registered user!')


#A local test call function to see output, need comment out in the end
if __name__ == "__main__":
	class Event:
		def data(self, key):
			j = {
					'key1': 'Jon',
					'key2': 'Jon-sensor',
					'key3': '80F',
					'key4': '30%'
				}
			return j[key]
	context = 'context'
	event = Event()
	print(lambda_handler(event, context))
