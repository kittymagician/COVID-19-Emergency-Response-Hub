# COVID-19 Emergency Response Hub

The COVID-19 Response Hub was designed for the community after realising that Parish Councils do not have a case mangement/ticket submission system. This application aims to provide software that is open, free and able to support the community at this difficult time

The application supports requests for food, medicine and emotional support via the web interface, sms and telephone (sms and telephone services use the Twilio platform).

- SMS: a simple chatbot that accepts requests and relays them via sms and the report center.

- Phone: text to speech and speech to text bot that processes requests and relays them to the report center

- Web: Web forms that relay the data to the report center.

Once the customer has requested the food/medicine/emotional support via the supported channels registered volunteers can login and view the customer's phone number and request as well as assign cases and once completed close them. The Dashboard is a one stop place to view live metrics of cases being processed, assigned and closed.
# Dependencies 

Flask, Flask-WTF, flask-sqlalchemy, flask-user, flask-talisman, flask-login and [twilio](https://www.twilio.com/) to name a [few!](https://github.com/kittymagician/COVID-19-Emergency-Response-Hub/blob/master/requirements.txt)

web pages call out to the stackpath CDN for Bootstrap, Cloudflare CDN for fontawesome icons, JQuery and DataTables and Google CDN for font and jsdelivr for [Cookie Consent](https://github.com/osano/cookieconsent)

# Installation

See the installation guide on the [Wiki](https://github.com/kittymagician/COVID-19-Emergency-Response-Hub/wiki/Installation)

# Screenshots
![Home Screen](https://github.com/kittymagician/COVID-19-Emergency-Response-Hub/blob/master/screenshots/releasev1/home.png)
![Dashboard](https://github.com/kittymagician/COVID-19-Emergency-Response-Hub/blob/master/screenshots/releasev1/dashboard.png)
![Full Report](https://github.com/kittymagician/COVID-19-Emergency-Response-Hub/blob/master/screenshots/fullreport.png)
![Food](https://github.com/kittymagician/COVID-19-Emergency-Response-Hub/blob/master/screenshots/releasev1/food.png)
![Medicine](https://github.com/kittymagician/COVID-19-Emergency-Response-Hub/blob/master/screenshots/releasev1/medicine.png)
![Emotional Support](https://github.com/kittymagician/COVID-19-Emergency-Response-Hub/blob/master/screenshots/releasev1/emotionalsupport.png)

# Licence
See `LICENSE` for further information.


# Contributing

1. Fork it ( https://github.com/kittymagician/COVID-19-Emergency-Response-Hub/fork )
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create a new Pull Request

# With Thanks

Joel Graham - [joelagraham.co.uk](http://joelagraham.co.uk) - front end redesign

KittyMagician - [kittymagician.com](https://kittymagician.com) - Backend and original front end design. 

Armin Ronacher - For founding [flask](https://flask.palletsprojects.com/en/1.1.x/) (the micro web framework this web app uses.)

Matthew Holt - For founding [Caddy](https://caddyserver.com) (a super simple web server with https by default.)

Benoit Chesneau - For founding [gunicorn](https://gunicorn.org) (for building a WSGI that can interface with Caddy.)

Ling Thio - For founding [flask-user](https://github.com/lingthio/Flask-User) (for creating a package that provides a simple way to intergrate Flask-Login and Flask-Security into a project)

Osano - For developing [cookie consent](https://github.com/osano/cookieconsent) (a open source cookie consent banner)

Thank you to the millions of developers around the world working on open source projects.
