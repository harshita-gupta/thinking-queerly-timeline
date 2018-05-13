from flask import render_template, redirect, flash, url_for
from app import app, db
from app.forms import AdminLoginForm, AdminRegistration
from flask_login import current_user, login_user, logout_user, login_required
from app.models import Admin


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    # add code here
    return render_template('index.html', title='Home', user=user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_panel'))
    form = AdminLoginForm()
    if form.validate_on_submit():
        user = Admin.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('admin_panel'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/admin_panel')
@login_required
def admin_panel():
    return "you made it to admin panel!"


@app.route('/session/<session_id>')
def session_id_participate(session_id):
    return ""


@app.route('/session/<session_id>/view')
def session_id_view(session_id):
    return ""


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('admin_panel'))
    form = AdminRegistration()
    if form.validate_on_submit():
        user = Admin(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered admin!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
