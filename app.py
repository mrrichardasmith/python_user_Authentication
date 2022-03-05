from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

#Boiler Plate - Create an Instance of the Flask object called app 
app = Flask(__name__)

#Boiler Plate - Create an instance of the SQLAlchemy object and pass it app
db = SQLAlchemy(app)

# Prevent technical overhead by setting this to False
app.config['SQLALCHEMY_TRACK_MODIFICIATIONS'] = False

# Configure the database URI and name the database file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_database.db'

# This is the secret key used to protect forms
app.secret_key = 'secretkeyhardcoded'

# Boiler Plate - Create an instance of the LoginManager and pass it app
login = LoginManager(app)

# Boiler Plate - Create a loop back to login when there is a problem
login.login_view = 'login'

# User loader is a requirement of LoginManager and an error is thrown until this is created
@login.user_loader 
def load_user(id): 
  return User.query.get(int(id))

import routes, models