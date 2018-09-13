from app import app
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    return '''
<html>
    <head>
        <title>Home Page - Sensor Site Senior Design</title>
    </head>
    <body>
        <h1>Hello!</h1>
    </body>
</html>'''


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}'.format(
            form.username.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)