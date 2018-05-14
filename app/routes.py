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
    elif form.errors:
        flash(form.errors)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/admin_panel', methods=['GET', 'POST'])
@login_required
def admin_panel():
    '''
    The admin panel is only available to a user who is logged in. 
    The panel allows administrators to view the list of sessions and create new sessions.
    '''
    form = WorkshopCreationForm(request.form)
    
    # Responing to a POST request
    if form.validate_on_submit(): 
        # Form submitted correctly.
        flash("Session created!")

        # Creating session and committing to DB. 
        workshop = WorkshopActivity(
            name=form.name.data, 
            date=form.date.data, 
            question=form.question.data, 
            unit_is_year=True if form.unit_is_year.data == "year" else False, 
            unique_str=form.unique_str.data,
            admin_owner=current_user.id)
        db.session.add(workshop)
        db.session.commit()
    elif form.errors: 
        # Form submitted incorrectly, displaying errors.
        flash(form.errors)

    # Return to the admin panel after any operations occur.
    return render_template("admin_panel.html", form=form, sessions=WorkshopActivity.query.all())


@app.route('/session/<session_str>', methods=['GET', 'POST'])
def session_id_participate(session_str):
    
    '''
    The session participation page allows a workshop participant to submit post-its to a timeline.
    The participant must go to the appropriate link defined at /session/id to participate.
    '''

    # Retrieve session that the user is participating in
    workshop = WorkshopActivity.query.filter_by(unique_str=session_str).first()
    form = ContributeToTimelineYearlong(request.form) if workshop.unit_is_year else ContributeToTimelineLifelong(request.form)
    
    # Responding to a POST request
    if form.validate_on_submit():
        # Form submitted correctly
        flash('Submitted!')

        # Retrieving post-its from the form and committing to DB.
        for postit in form.submissions.entries:
            if not postit.body.data:
                continue
            p = PostIt(
                body=postit.body.data,
                on_sex=True if postit.on_sex.data == "sex" else False,
                session_id=workshop.id,
                session=workshop)
            if workshop.unit_is_year:
                p.mdy_timestamp = postit.timestamp.data
            else: 
                p.year_timestamp = postit.timestamp.data
            db.session.add(p)
        db.session.commit()
        return redirect(url_for('session_id_participate', session_str=session_str))
    elif form.errors: 
        flash(form.errors)
    return render_template("session_participate.html", session=workshop, form=form)


@app.route('/session/<session_str>/view')
def session_id_view(session_str):
    # Retrieve session that the user is participating in
    workshop = WorkshopActivity.query.filter_by(unique_str=session_str).first()
    if workshop.unit_is_year:
        postits = workshop.postits.orderby(PostIt.mdy_timestamp).all()
    else:
        postits = workshop.postits.orderby(PostIt.year_timestamp).all()
    return render_template('timeline-view.html', posts=postits)


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
