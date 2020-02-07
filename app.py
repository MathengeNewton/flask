from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, length
# from flask_sqlalchemy import SQLAlchemy

# from datetime import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = "secretkey"
Bootstrap(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql + psycopg2://postgres:mathenge,./1998@localhost/mytest'
# db = SQLAlchemy(app)


# class firstTable(db.Model):
#     id = db.Column(db.Integer, nullable=False, primary_key=True)
#     title = db.Column(db.String(100), nullable=False, unique=True)
#     content = db.Column(db.Text, nullable=False)
#     authur = db.Column(db.String(20), nullable=False, default='n/a')
#     date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

#     def __init__(self, title, content, authur, date):
#         self.title = title
#         self.content = content
#         self.authur = authur
#         self.date = date

#     def __repr__(self):
#         return 'Blog Post' + str(self.id)


class LoginForm(FlaskForm):
    email = StringField('email', validators=[
                        InputRequired(), length(min=4, max=15)])
    password = PasswordField('password', validators=[
                             InputRequired(), length(min=8, max=80)])
    remember = BooleanField('remember me')


class Registration(FlaskForm):
    name = StringField('name', validators=[
                       InputRequired(), length(min=6, max=20)])
    email = StringField('email', validators=[
                        InputRequired(), length(min=4, max=15)])
    password = PasswordField('password', validators=[
                             InputRequired(), length(min=8, max=80)])


@app.route('/')
def index():

    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return '<h1>' + form.email.data + '' + form.password.data + '</h1>'
    return render_template('entry/login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = Registration()
    if form.validate_on_submit():
        return '<h1>' + form.name.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'
    return render_template('entry/register.html', form=form)


@app.route('/dashboard')
def dashboard():
    return render_template('body/dashboard.html')


if __name__ == "__main__":
    app.run(debug=True)
