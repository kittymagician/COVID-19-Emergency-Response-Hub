# COVID-19 Emergency Response Hub

The Community Response Hub was designed after realising that Parish Councils do not have a case mangement/ticket submission system.

# Dependencies 

Flask, Flask-WTF, flask-sqlalchemy, flask-user, twilio, web pages call out to a CDN for Bootstrap.

# Installation

Register for a Twilio account and register a phone that is able to support SMS.

1. Install packages using PIP.

2. Edit the app.py with the Twilio API, Twilio number and your mobile number.

3. Edit app.py and set USER_ENABLE_REGISTER = False to USER_ENABLE_REGISTER = True

4. Setup the database by running python3 createreportsdb.py.

5. Run python3 app.py and go to the web app. Register your username and password by going to /user/register

6. Edit app.py and set USER_ENABLE_REGISTER = False

7. Run python3 app.py

8. Configure your proxy to accept the Flask connection from localhost:5000. Feel free to use Gunicorn. 
