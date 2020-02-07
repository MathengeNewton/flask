from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, length
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user


app = Flask(__name__)
app.config['SECRET_KEY'] = "secretkey"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:mathenge,./1998@localhost/myflaskapp'
Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class userinfo(UserMixin, db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    name = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return userinfo.query.get(int(user_id))


class LoginForm(FlaskForm):
    email = StringField('email', validators=[
                        InputRequired(), length(min=10, max=20)])
    password = PasswordField('password', validators=[
                             InputRequired(), length(min=8, max=80)])
    remember = BooleanField('remember me')


class Registration(FlaskForm):
    name = StringField('name', validators=[
                       InputRequired(), length(min=6, max=20)])
    email = StringField('email', validators=[
                        InputRequired(), length(min=10, max=20)])
    password = PasswordField('password', validators=[
                             InputRequired(), length(min=8, max=80)])


@app.route('/')
def index():

    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        account = userinfo.query.filter_by(email=form.email.data).first()
        if account:
            if check_password_hash(account.password, form.password.data):
                return redirect(url_for('dashboard'))
        return '<h1>Invalid user or password</h1>'
    return render_template('entry/login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = Registration()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(
            form.password.data, method='sha256')
        new_user = userinfo(name=form.name.data,
                            email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return render_template('entry/login.html')

    return render_template('entry/register.html', form=form)


@app.route('/dashboard')
def dashboard():

    return render_template('body/dashboard.html')


if __name__ == "__main__":
    app.run(debug=True)
