from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICIATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_database.db'

app.secret_key = 'secretkeyhardcoded'


login = LoginManager(app)
login.login_view = 'login'

@login.user_loader 
def load_user(id): 
  return User.query.get(int(id))

import routes, models