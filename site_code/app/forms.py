from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')

class SensorSubmitForm(FlaskForm):
    sensor_name = StringField('Sensor Name', validators=[DataRequired()])
    submit = SubmitField('Enter New Sensor')

class SelectSensorForm(FlaskForm):
    sensor_select = SelectField('Sensor:', default='',validators=[DataRequired()])
    submit = SubmitField('Select Sensor')

class DataEntry(FlaskForm):
    sensorName = StringField('Sensor Name')
    username = StringField('Username')
    humidity = IntegerField('Humidity')
    temperature = IntegerField('Temp')
    submit = SubmitField('Enter Data')
