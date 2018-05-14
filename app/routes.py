from flask import render_template, redirect, flash, url_for, request
from app import app, db
from app.forms import AdminLoginForm, AdminRegistration, ContributeToTimelineYearlong, ContributeToTimelineLifelong, WorkshopCreationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import Admin, WorkshopActivity, PostIt


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
    form = AdminLoginForm(request.form)
    if form.validate_on_submit():
        user = Admin.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('admin_panel'))
    else: 
        flash(form.errors)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/admin_panel', methods=['GET', 'POST'])
@login_required
def admin_panel():
    form = WorkshopCreationForm(request.form)
    sessions = WorkshopActivity.query.all()
    if form.validate_on_submit(): 
        print("that shit submitted")
        flash("Session created!")
    else: 
        flash(form.errors)
    return render_template("admin_panel.html", form=form, session_list=sessions)


@app.route('/session/<session_id>', methods=['GET', 'POST'])
def session_id_participate(session_id):
    workshop = WorkshopActivity.query.get(int(session_id))
    workshop = WorkshopActivity(question="q is here", name="ws name is here", date="date is here", unit_is_year=False)
    form = ContributeToTimelineYearlong(request.form) if workshop.unit_is_year else ContributeToTimelineLifelong(request.form)
    if form.validate_on_submit():
        print("validated")
        flash('Submitted!')
        return redirect(url_for('session_id_participate', session_id=session_id))
    # else: 
    #     flash(form.errors)
    return render_template("session_participate.html", session=workshop, form=form)


@app.route('/session/<session_id>/view')
def session_id_view(session_id):
    return ""


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('admin_panel'))
    form = AdminRegistration(request.form)
    if form.validate_on_submit():
        user = Admin(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered admin!')
        return redirect(url_for('login'))
    else: 
        flash(form.errors)
    return render_template('register.html', title='Register', form=form)
