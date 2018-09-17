from app import app
from flask import render_template, flash, redirect, url_for,session
from app.forms import LoginForm
from app.forms import RegistrationForm
from app.forms import SensorSubmitForm
from app import db
from app.models import User, Data, Sensor
from flask_login import current_user, login_user
from flask_login import logout_user
from flask_login import login_required
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    form = SensorSubmitForm()
    user_id = session["user_id"]
    user = User.query.filter_by(id=user_id).first()
    this_sensor = Sensor.query.filter_by(user_id=user_id).first()
    if form.validate_on_submit():
        sensor = Sensor(name=form.sensor_name.data,user_id=user_id)
        db.session.add(sensor)
        db.session.commit()
    return render_template('index.html',user=user,sensor_display=this_sensor,form=form)


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

