import os
import datetime
import sqlite3
from flask import Flask, render_template_string, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_user import login_required, UserManager, UserMixin
from twilio.twiml.voice_response import Gather, VoiceResponse, Say
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_talisman import Talisman

account_sid = "Twilio SID goes here" #Twilio SID 
auth_token  = "Twilio Auth Token goes here" #Twilio Auth Token
client = Client(account_sid, auth_token)
responder_number = "Volenteer Phone Number goes here." # The number you want requests to forward to.
twilio_number = "Twilio Registered Number goes here." # The twilio SMS number you registered previously.
default_resp = "I have forwarded on your request to the community support team"
fallback_resp = "Welcome to the Emergency Response SMS bot. What do you need support with? Say Food Shopping for Food Shopping, Mediciation for Medication, emotional support call for emotional support phone call."
now = datetime.datetime.now()
locale = "en-GB" # Text to speech and speech to text language for Twilio.

class MyForm(FlaskForm):
    telephonenumber = StringField('telephone number', validators=[DataRequired(), Length(max=40)])
    food = StringField('What food do you require?', validators=[DataRequired(), Length(max=100)])
    submit = SubmitField('Submit')

class MedForm(FlaskForm):
    telephonenumber = StringField('telephone number', validators=[DataRequired(), Length(max=40)])
    medication = StringField('How many items + Pharmacy Name + Paid or Free perscription', validators=[DataRequired(), Length(max=1000)])
    submit = SubmitField('Submit')

class EmotionalForm(FlaskForm):
    telephonenumber = StringField('telephone number', validators=[DataRequired(), Length(max=40)])
    emotional = StringField('When would be an ideal time to call you back?', validators=[DataRequired(), Length(max=1000)])
    submit = SubmitField('Submit')
    
# Class-based application configuration
class ConfigClass(object):
    """ Flask application config """
    # Flask settings
    SECRET_KEY = str(os.urandom(255))
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE='Lax'
    SESSION_COOKIE_NAME = "__secure"

    # Flask-SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = 'sqlite:///hubapp.sqlite'    # File-based SQL database
    SQLALCHEMY_TRACK_MODIFICATIONS = False    # Avoids SQLAlchemy warning

    # Flask-User settings
    USER_COPYRIGHT_YEAR = now.year
    USER_APP_NAME = "Emergency Response Hub"      # Shown in and email templates and page footers
    USER_ENABLE_EMAIL = False      # Disable email authentication
    USER_ENABLE_USERNAME = True    # Enable username authentication
    USER_REQUIRE_RETYPE_PASSWORD = True    # Simplify register form
    USER_ENABLE_REGISTER = False #set to True to register your username but set this to False afterwards!
    USER_CORPORATION_NAME = "COVID-19 Emergency Response Hub" # change to your own brand name.
    
def create_app():
    """ Flask application factory """
    
    # Create Flask app load app.config
    app = Flask(__name__)
    app.config.from_object(__name__+'.ConfigClass')
    # Security Headers
    csp = {
        'default-src': '\'self\'',
        'style-src':  '\'unsafe-inline\' \'self\' bootstrapcdn.com *.bootstrapcdn.com cloudflare.com *.cloudflare.com googleapis.com *.googleapis.com jsdelivr.net *.jsdelivr.net',
        'script-src': '\'unsafe-eval\' \'self\' bootstrapcdn.com *.bootstrapcdn.com cloudflare.com *.cloudflare.com googleapis.com *.googleapis.com jquery.com *.jquery.com jsdelivr.net *.jsdelivr.net',
        'font-src': 'cloudflare.com *.cloudflare.com gstatic.com *.gstatic.com bootstrapcdn.com *.bootstrapcdn.com',
        'img-src': '\'self\' data:'
    }
    feature_policy = {
        'geolocation': '\'none\'',
        'accelerometer': '\'none\'',
        'camera': '\'none\'',
        'geolocation': '\'none\'',
        'gyroscope': '\'none\'',
        'magnetometer': '\'none\'',
        'microphone': '\'none\'',
        'payment': '\'none\'',
        'usb': '\'none\''
    }
    Talisman(app, content_security_policy=csp, feature_policy=feature_policy, content_security_policy_nonce_in=['script-src'])
    # Initialize Flask-SQLAlchemy
    db = SQLAlchemy(app)

    # Define the User data-model.
    # NB: Make sure to add flask_user UserMixin !!!
    class User(db.Model, UserMixin):
        __tablename__ = 'users'
        id = db.Column(db.Integer, primary_key=True)
        active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')

        # User authentication information. The collation='NOCASE' is required
        # to search case insensitively when USER_IFIND_MODE is 'nocase_collation'.
        username = db.Column(db.String(100, collation='NOCASE'), nullable=False, unique=True)
        password = db.Column(db.String(255), nullable=False, server_default='')
        email_confirmed_at = db.Column(db.DateTime())

        # User information
        first_name = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')
        last_name = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')

    # Create all database tables
    db.create_all()

    # Setup Flask-User and specify the User data-model
    user_manager = UserManager(app, db, User)

    # The Home page is accessible to anyone
    @app.route('/')
    def home_page():
      return redirect(url_for('hub'))

    # The Members page is only accessible to authenticated users via the @login_required decorator
    
    @app.route('/member_page')
    @login_required    # User must be authenticated
    def member_page():
        # String-based templates
        return render_template_string("""
            {% extends "flask_user_layout.html" %}
            {% block content %}
                <h2>Volunteer Hub</h2>
                <p><a href={{ url_for('food') }}>Food Form</a>
                <p><a href={{ url_for('medication') }}>Medication Form</a>
                <p><a href={{ url_for('emotionalsupport') }}>Emotional Support Form</a>
                <p><a href={{ url_for('fullreport') }}>Full Report</a></p>
                <p><a href={{ url_for('openreport') }}>All Open Cases</a></p>
                <p><a href={{ url_for('assignedreport') }}>All Assigned Cases</a></p>
                <p><a href={{ url_for('dashboard') }}>Dashboard</a></p>
                <p><a href={{ url_for('user.logout') }}>Sign out</a></p>
            {% endblock %}
            """)
    @app.route("/reportcenter")
    @login_required
    def reportcenter():
      return redirect(url_for('member_page'))
    @app.route("/reportcenter/dashboard")
    @login_required
    def dashboard():
      conn = sqlite3.connect('hubapp.sqlite')
      c = conn.cursor()
      c.execute('SELECT count(*) AS \"status\" FROM webreport WHERE status = \"open\"')
      webreport = c.fetchone()
      web = webreport[0]
      c.execute('SELECT count(*) AS \"webstatus\" FROM smsreport WHERE status = \"open\"')
      smsreport = c.fetchone()
      sms = smsreport[0]
      c.execute('SELECT count(*) AS \"phonestatus\" FROM phonereport WHERE status = \"open\"')
      phonereport = c.fetchone()
      phone = phonereport[0]
      c.execute('select count(*) AS \"webstatusclosed\" FROM webreport WHERE status = \"close\"')
      closedweb = c.fetchone()
      cweb = closedweb[0]
      c.execute('select count(*) AS \"smsstatusclosed\" FROM smsreport WHERE status = \"close\"')
      closedsms = c.fetchone()
      csms = closedsms[0]
      c.execute('select count(*) AS \"phonestatusclosed\" FROM phonereport WHERE status = \"close\"')
      closedphone = c.fetchone()
      cphone = closedsms[0]
      closed = cweb + csms + cphone
      c.execute('select count(*) AS \"webstatusassigned\" FROM webreport WHERE status = \"assigned\"')
      assignedweb = c.fetchone()
      aweb = assignedweb[0]
      c.execute('select count(*) AS \"smsstatusassigned\" FROM smsreport WHERE status = \"assigned\"')
      assignedsms = c.fetchone()
      asms = assignedsms[0]
      c.execute('select count(*) AS \"phonestatusassigned\" FROM phonereport WHERE status = \"assigned\"')
      assignedphone = c.fetchone()
      aphone = assignedphone[0]
      assigned = aweb + asms + aphone
      conn.close()
      return render_template('dashboard.html', web = web, sms = sms, phone = phone, closed = closed, assigned=assigned)
    @app.route("/reportcenter/full")
    @login_required
    def fullreport():
      conn = sqlite3.connect('hubapp.sqlite')
      c = conn.cursor()
      c.execute("SELECT * FROM webreport")
      items = c.fetchall()
      c.execute("SELECT * FROM smsreport")
      smsitems = c.fetchall()
      c.execute("SELECT * FROM phonereport")
      phoneitems = c.fetchall()
      return render_template('fullreport.html', items=items, smsitems=smsitems, phoneitems=phoneitems)
    @app.route("/reportcenter/open")
    @login_required
    def openreport():
      conn = sqlite3.connect('hubapp.sqlite')
      c = conn.cursor()
      c.execute('SELECT ID, telephone number, category, message, status FROM webreport WHERE status = \"open\"')
      web = c.fetchall()
      c.execute('SELECT ID, telephone number, category, message, status FROM smsreport WHERE status = \"open\"')
      sms = c.fetchall()
      c.execute('SELECT ID, telephone number, category, message, status FROM phonereport WHERE status = \"open\"')
      phone = c.fetchall()
      conn.close()
      return render_template('openreport.html', sms=sms, web=web, phone=phone)
    @app.route("/reportcenter/assigned")
    @login_required
    def assignedreport():
      conn = sqlite3.connect('hubapp.sqlite')
      c = conn.cursor()
      c.execute('SELECT ID, telephone number, category, message, status FROM webreport WHERE status = \"assigned\"')
      web = c.fetchall()
      c.execute('SELECT ID, telephone number, category, message, status FROM smsreport WHERE status = \"assigned\"')
      sms = c.fetchall()
      c.execute('SELECT ID, telephone number, category, message, status FROM phonereport WHERE status = \"assigned\"')
      phone = c.fetchall()
      conn.close()
      return render_template('assignedreport.html', sms=sms, web=web, phone=phone)
    @app.route("/reportcenter/web/close/<int:id>")
    @login_required
    def closereport(id):
      conn = sqlite3.connect('hubapp.sqlite')
      c = conn.cursor()
      try:
        c.execute("UPDATE webreport SET status = ? WHERE ID = ?", ('close', id))
        conn.commit()
        conn.close()
        return redirect(url_for('openreport'))
      except:
        return 'This case has already been closed.'
    @app.route("/reportcenter/web/assign/<int:id>")
    @login_required
    def assignreport(id):
      conn = sqlite3.connect('hubapp.sqlite')
      c = conn.cursor()
      try:
        print('hi')
        c.execute("UPDATE webreport SET status = ? WHERE ID = ?", ('assigned', id))
        conn.commit()
        conn.close()
        return redirect(url_for('assignedreport'))
      except:
        return 'This case has already been assigned.'
    @app.route("/reportcenter/sms/close/<int:id>")
    @login_required
    def smsclosereport(id):
      conn = sqlite3.connect('hubapp.sqlite')
      c = conn.cursor()
      try:
        c.execute("UPDATE smsreport SET status = ? WHERE ID = ?", ('close', id))
        conn.commit()
        conn.close()
        return redirect(url_for('openreport'))
      except:
        return 'This case has already been closed.'
    @app.route("/reportcenter/sms/assign/<int:id>")
    @login_required
    def smsassignreport(id):
      conn = sqlite3.connect('hubapp.sqlite')
      c = conn.cursor()
      try:
        c.execute("UPDATE smsreport SET status = ? WHERE ID = ?", ('assigned', id))
        conn.commit()
        conn.close()
        return redirect(url_for('assignedreport'))
      except:
        return 'This case has already been assigned.'
    @app.route("/reportcenter/phone/close/<int:id>")
    @login_required
    def phoneclosereport(id):
      conn = sqlite3.connect('hubapp.sqlite')
      c = conn.cursor()
      try:
        c.execute("UPDATE phonereport SET status = ? WHERE ID = ?", ('close', id))
        conn.commit()
        conn.close()
        return redirect(url_for('openreport'))
      except:
        return 'This case has already been closed.'
    @app.route("/reportcenter/phone/assign/<int:id>")
    @login_required
    def phoneassignreport(id):
      conn = sqlite3.connect('hubapp.sqlite')
      c = conn.cursor()
      try:
        c.execute("UPDATE phonereport SET status = ? WHERE ID = ?", ('assigned', id))
        conn.commit()
        conn.close()
        return redirect(url_for('assignedreport'))
      except:
        return 'This case has already been assigned.'
    @app.route("/gdpr")
    def gdpr():
      return render_template('gdpr.html')
    @app.route("/hub", methods=['GET'])
    def hub():
      return render_template('default.html')
    @app.route("/hub/food", methods=['GET', 'POST'])
    def food():
      form = MyForm()
      if form.validate_on_submit():
        conn = sqlite3.connect('hubapp.sqlite')
        c = conn.cursor()
        number = form.telephonenumber.data
        food = form.food.data
        c.execute("insert into webreport values (?, ?, ?, ?, ?)", (None, number, 'food', food, 'open'))
        conn.commit()
        conn.close()
        return redirect(url_for('success'))
      return render_template('food.html', form=form)
    @app.route("/hub/medicine", methods=['GET', 'POST'])
    def medication():
      form = MedForm()
      if form.validate_on_submit():
        conn = sqlite3.connect('hubapp.sqlite')
        c = conn.cursor()
        number = form.telephonenumber.data
        medication = form.medication.data
        c.execute("insert into webreport values (?, ?, ?, ?, ?)", (None, number, 'medication', medication, 'open'))
        conn.commit()
        conn.close()
        return redirect(url_for('success'))
      return render_template('medicine.html', form=form)
    @app.route("/hub/emotionalsupport", methods=['GET', 'POST'])
    def emotionalsupport():
      form = EmotionalForm()
      if form.validate_on_submit():
        conn = sqlite3.connect('hubapp.sqlite')
        c = conn.cursor()
        number = form.telephonenumber.data
        food = form.emotional.data
        c.execute("insert into webreport values (?, ?, ?, ?, ?)", (None, number, 'Emotional Support', food, 'open'))
        conn.commit()
        conn.close()
        return redirect(url_for('success'))
      return render_template('emotionalsupport.html', form=form)
    @app.route("/hub/success")
    def success():
      return render_template('success.html')
    @app.route("/sms", methods =['POST'])
    def sms():
        conn = sqlite3.connect('hubapp.sqlite')
        c = conn.cursor()
        number = request.form['From']
        message_body = request.form['Body'].lower()
        resp = MessagingResponse()
        if message_body == 'hi':
          response_message = fallback_resp
        if 'food shopping' in message_body:
          response_message = 'Great! What food do you require? Say I need food followed by the items. For example \'I need 1 tinned beans\''
        elif 'i need' in message_body:
          helper_resp = message_body.replace('i need ', '')
          helper_message = 'a new food request has come in from the following number: ' + number + ' for the following items: ' + helper_resp
          message = client.messages.create(
              to=responder_number, 
              from_=twilio_number,
              body=helper_message)
          c.execute("insert into smsreport values (?, ?, ?, ?, ?)", (None, responder_number, 'food', helper_resp, 'open'))
          response_message = default_resp
        elif 'medication' in message_body:
          response_message = 'Great! Where do we need to pick your medications up from and is the perscription paid/free? Say for example \'pick up from spires pharmacy free prescription in the name of John Doe\''
        elif 'pick up' in message_body:
          helper_resp = message_body.replace('pick up from ', '')
          helper_message = 'a new medication request has come in from the following number: ' + number + ' for the following: ' + helper_resp
          message = client.messages.create(
              to=responder_number, 
              from_=twilio_number,
              body=helper_message)
          response_message = default_resp
          c.execute("insert into smsreport values (?, ?, ?, ?, ?)", (None, responder_number, 'edication', helper_resp, 'open'))
        elif 'emotional support call' in message_body:
          helper_message = 'a new emotional support phone call request has come in from the following number: ' + number
          message = client.messages.create(
              to=responder_number, 
              from_=twilio_number,
              body=helper_message)
          response_message = default_resp
          c.execute("insert into smsreport values (?, ?, ?, ?, ?)", (None, responder_number, 'emotional support', helper_resp, 'open'))
        else:
          response_message = fallback_resp
        resp.message(response_message)
        conn.commit()
        conn.close()
        return str(resp)
    @app.route("/voice", methods=['GET', 'POST'])
    def voiceresponse():
      response = VoiceResponse()
      gather = Gather(input='speech', action='/voice/selection', language=locale)
      gather.say('Welcome to the Emergency Response Hub, Please say out loud one of the following three options. food. medication. and finally. emotional support. if you need your prescriptions picked up say medication. If you need food say food. if you need an emotional support chat say emotional support.', voice='alice', language=locale)
      response.append(gather)
      return str(response)
    @app.route("/voice/selection", methods=['GET', 'POST'])
    def selection():
      speech = request.values.get('SpeechResult')
      caller = request.values.get('Caller')
      response = VoiceResponse()
      if speech == 'food':
        gather = Gather(input='speech', action='/voice/food', language=locale)
        gather.say("Please say what food you require. For example baked beans.", voice='alice', language=locale)
        response.append(gather)
      elif speech == 'medication':
        gather = Gather(input='speech', action='/voice/medication', language=locale)
        gather.say("Please say the medication you require.", voice='alice', language=locale)
        response.append(gather)
      elif speech == 'emotional support':
        if caller != None:
          conn = sqlite3.connect('hubapp.sqlite')
          c = conn.cursor()
          response.say('You said you need emotional support. One of our volunteers will be in touch soon. In the meantime if you want to talk to someone immediately please contact Samaritans at 1. 1. 6.  1. 2. 3. The Lines are open 24 hours a day 7 days a week.', voice='alice', language=locale)
          response.say('Thank you for calling. Goodbye.', voice='alice', language=locale)
          speech = "requires emotional support callback."
          c.execute("insert into phonereport values (?, ?, ?, ?, ?)", (None, caller, 'emotional support', speech, 'open'))
          conn.commit()
          conn.close()
          response.hangup()
        else:
          response.say('Unfortauntely your caller ID has been witheald. We are unable to process your emotional support request unless we are able to get your caller ID. However you can call Samaritans for free at 1. 1. 6.  1. 2. 3.')
      else:
        response.say('I\'m sorry, I was unable to identify what you said. Please call back or alternatively text this number your request. Goodbye!', voice='alice', language=locale)
        response.hangup()
      return str(response)
    @app.route("/voice/medication", methods=['GET', 'POST'])
    def phonemedication():
      speech = request.values.get('SpeechResult')
      caller = request.values.get('Caller')
      response = VoiceResponse()
      if caller != None:
        conn = sqlite3.connect('hubapp.sqlite')
        c = conn.cursor()
        c.execute("insert into phonereport values (?, ?, ?, ?, ?)", (None, caller, 'medication', speech, 'open'))
        response.say('I have notified the team that you require the following medication: ' + speech, voice='alice', language=locale)
        response.say('They will be in contact soon. Thank you for calling. Goodbye!', voice='alice', language=locale)
        conn.commit()
        conn.close()
      else:
        response.say('Unfortunately I am unable to process your call as you are witholding your caller id. You can either disable your caller ID or use our online service. Thank You, Goodbye.')
      return str(response)
    @app.route("/voice/food", methods=['GET', 'POST'])
    def phonefood():
      speech = request.values.get('SpeechResult')
      caller = request.values.get('Caller')
      response = VoiceResponse()
      if caller != None:
        conn = sqlite3.connect('hubapp.sqlite')
        c = conn.cursor()
        c.execute("insert into phonereport values (?, ?, ?, ?, ?)", (None, caller, 'food', speech, 'open'))
        response.say('I have notified the team that you require the following: ' + speech, voice='alice', language=locale)
        response.say('they will be in contact soon. Thank you for calling. Goodbye!', voice='alice', language=locale)
        conn.commit()
        conn.close()
      else:
        response.say('Unfortunately I am unable to process your call as you are witholding your caller id. You can either disable your caller ID or use our online service. Thank You, Goodbye.')
      return str(response)
    return app
app = create_app()

# Start development web server
if __name__=='__main__':
    app.run(host='0.0.0.0', port=3000, debug=False)
