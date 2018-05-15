import csv
from flask import render_template, redirect, flash, url_for, request, send_file
from app import app, db
from io import BytesIO, StringIO
from app.forms import AdminLoginForm, AdminRegistration, ContributeToTimelineYearlong, ContributeToTimelineLifelong, WorkshopCreationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import Admin, WorkshopActivity, PostIt

'''
This file is responsible for routing various relative URLs to pages and interfaces of the website.
'''

''' HOMEPAGE '''
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

''' 
ADMIN PANEL PAGES
'''

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


@app.route('/download_data/<session_str>', methods=['GET'])
@login_required
def download_data(session_str):
    '''
    This link will allow an administrator to download a CSV of session data. 
    The page would not change, but a download would begin.
    '''
    workshop = WorkshopActivity.query.filter_by(unique_str=session_str).first()
    postits = workshop.postits.order_by(
        PostIt.mdy_timestamp if workshop.unit_is_year else PostIt.year_timestamp).all()
    
    # The below code uses flask's provided send_file function to send a file to 
    # the client requesting it. 
    # Since csv.writer cannot write bytes in python3, 
    # but flask's send_file method requires bytes in pyhton3, 
    # we must initialize two I/O streams for our operation.

    f = BytesIO()  # the stream that will be sent as a file to the user
    s = StringIO()  # the string stream that the CSV will first be written to 
    
    # Writing the CSV to the string stream
    writer = csv.writer(s)
    writer.writerow(['id', 'body', 'year_stamp', 'mdy_timestamp', 'on_sex', 'session_id'])
    [writer.writerow([p.id, p.body, p.year_timestamp, p.mdy_timestamp, p.on_sex, p.session_id]) for p in postits]

    # Encoding the string CSV into bytes
    s.seek(0)
    f.write(s.getvalue().encode())
    f.seek(0)

    # Sending the byte file to the client
    return send_file(f,
                     mimetype='text/csv',
                     attachment_filename='%s.csv' % session_str,
                     as_attachment=True)
    

@app.route('/delete_session/<session_str>', methods=['GET'])
@login_required
def delete_session(session_str):
    # Currently, since this a demo application, deleting sessions does not do anything. 
    # Eventually, it will delete the WorkshopActivity row that corresponds to session_str, 
    # and will also delete any associated post-its. 
    # The intention of this feature is to stay within the constraints of 
    # Heroku's free tier.
    return redirect(url_for('admin_panel'))

'''
TIMELINE CONTRIBUTION AND VIEWING FUNCTIONS
'''

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
            
            # Setting appropriate row field based on type of timeline
            if workshop.unit_is_year:
                p.mdy_timestamp = postit.timestamp.data
            else: 
                p.year_timestamp = postit.timestamp.data
            # Add this one post-it
            db.session.add(p)

        # Commit all added post-its to database
        db.session.commit()
        return redirect(url_for('session_id_participate', session_str=session_str))
    elif form.errors:
        flash(form.errors)
    return render_template("session_participate.html", session=workshop, form=form)


@app.route('/session/<session_str>/view')
def session_id_view(session_str):
    '''
    Displays a timeline of all post-its for a given session. Viewable to public.
    '''

    # Retrieve session and corresponding post-its
    workshop = WorkshopActivity.query.filter_by(unique_str=session_str).first()
    postits = workshop.postits.order_by(
        PostIt.mdy_timestamp if workshop.unit_is_year else PostIt.year_timestamp).all()
    return render_template('timeline-view.html', posts=postits, session=workshop)


'''
USER MANAGEMENT PAGES
'''

@app.route('/login', methods=['GET', 'POST'])
def login():
    '''
    This view allows existing administrators to log in in order to access the admin panel.
    '''
    # If user is logged in, redirect to admin panel
    if current_user.is_authenticated:
        return redirect(url_for('admin_panel'))

    form = AdminLoginForm(request.form)

    if form.validate_on_submit():
        # If user successfully submits login information
        user = Admin.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            # If credentials fail
            flash('Invalid username or password')
            return redirect(url_for('login'))
        # In this case, credentials pass
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('admin_panel'))
    elif form.errors:
        # Display errors
        flash(form.errors)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    '''
    This 'view' provides a link via which an administrator can log out. 
    It always redirects back to the home page.
    '''
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    '''
    This link allows any site visitors not currently logged in as administrators 
    to create administrator accounts.
    '''
    # If user is logged in, redirect to admin panel
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
    elif form.errors: 
        flash(form.errors)
    return render_template('register.html', title='Register', form=form)


