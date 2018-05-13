from flask import render_template
from app import app
from app.forms import AdminLoginForm


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    return render_template('index.html', title='Home', user=user)


@app.route('/login')
def login():
    form = AdminLoginForm()
    return render_template('login.html', title='Sign In', form=form)
