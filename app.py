from flask import Flask, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required, login_user, logout_user, LoginManager, UserMixin, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, EqualTo
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = 'secretkeyhardcoded'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///voter.db'


db = SQLAlchemy(app)

# create login_manager here:
login_manager = LoginManager()
# initialize login_manager here:
login_manager.init_app(app)
# redirect not logged in users to the page hosting the login form
login_manager.login_view = 'index'

@app.route('/', methods=['GET', 'POST'])
def index():
  login = LoginForm()
  if request.method == 'GET':
    return render_template("login.html", login = login )
  if request.method == 'POST':
    user = User.query.filter_by(username=login.username.data).first()
    if user is None:
      print(user)
      flash('Invalid username or password')
      return redirect(url_for('index'))
    else:
      if check_password_hash(user.password, login.password.data):
        print('matched')
        login_user(user)
    #which it shoud be as you just loaded it above
    if current_user.is_authenticated:
      print(current_user.username)
      print(current_user.password)
    return render_template('vote.html', current_user=user )


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        #having trouble calling the methods directly from the User object
        user.password = generate_password_hash(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('index'))
    return render_template('register.html', title='Register', registration_form=form)


@app.route('/vote')
@login_required
def vote():
    return 'This is a voter page only accessible through authentication'

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@login_manager.unauthorized_handler
def unauthorized():
  # do stuff
  return render_template('noauth.html')

@login_manager.user_loader
def load_user(id):
  return User.query.get(int(id))

#A form for logging on users
class LoginForm(FlaskForm):
  username = StringField(label = "User Name:", validators=[DataRequired()])
  email = StringField(label = "email:", validators=[DataRequired()])
  password = StringField(label = "password:", validators=[DataRequired()])
  submit = SubmitField("Login")


class RegistrationForm(FlaskForm):
    username = StringField(label = 'Username', validators=[DataRequired()])
    email = StringField(label='email', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    password2 = PasswordField(
        label='Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))
    def set_password(self, password):
      self.password_hash = generate_password_hash(password)
    def check_password_hash(self, password):
      return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Vote(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  name = db.Column(db.String(50), index = True, unique = False)
  attending = db.Column(db.String(5), index = True, unique = False)

  def __repr__(self):
    return f"{self.name} by {self.attending}"


