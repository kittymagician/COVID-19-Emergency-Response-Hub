# COVID-19 Emergency Response Hub

The Community Response Hub was designed after realising that Parish Councils do not have a case mangement/ticket submission system.

The application supports requests for food, medicine and emotional support via the web interface, sms and telephone (sms and telephone services use the Twilio platform).

- SMS: a simple chatbot that accepts requests and relays them via sms and the report center.

- Phone: text to speech and speech to text bot that processes requests and relays them to the report center

- Web: Web forms that relay the data to the report center.

Once the customer has requested the food via the supported channels registered volunteers can login and view the customer's phone number and request as well as assign cases and once completed close them. The Dashboard is a one stop place to view live metrics of cases being processed, assigned and closed.
# Dependencies 

Flask, Flask-WTF, flask-sqlalchemy, flask-user, [twilio](https://www.twilio.com/)

web pages call out to the stackpath CDN for Bootstrap, Cloudflare CDN for fontawesome icons, JQuery and DataTables and Google CDN for font.

# Installation

See the installation guide on the [Wiki](https://github.com/kittymagician/COVID-19-Emergency-Response-Hub/wiki/Installation)

# Screenshots
![Home Screen](https://github.com/kittymagician/COVID-19-Emergency-Response-Hub/blob/master/screenshots/home.png)
![Dashboard](https://github.com/kittymagician/COVID-19-Emergency-Response-Hub/blob/master/screenshots/dashboard.png)
![Full Report](https://github.com/kittymagician/COVID-19-Emergency-Response-Hub/blob/master/screenshots/fullreport.png)
# With Thanks

Joel Graham - [joelagraham.co.uk](http://joelagraham.co.uk) - front end redesign

KittyMagician - [kittymagician.com](https://kittymagician.com) - Backend and original front end design. 

Armin Ronacher - For founding [flask](https://flask.palletsprojects.com/en/1.1.x/) (the micro web framework this web app uses.)

Matthew Holt - For founding [Caddy](https://caddyserver.com) (a super simple web server with https by default.)

Benoit Chesneau - For founding [gunicorn](https://gunicorn.org) (for building a WSGI that can interface with Caddy.)

Thank you to the millions of developers around the world working on open source projects.
