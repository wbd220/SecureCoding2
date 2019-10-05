from flask import Flask, render_template, request, url_for, redirect, flash
from flask_wtf import FlaskForm, form
from wtforms import Form, StringField, TextAreaField, validators, StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
import os

app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = 'bd0c7d441f27d441f27567d441f2b6176a'


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'


class LoginForm(FlaskForm):
    username = StringField('uname', validators=[DataRequired()])
    password = PasswordField('Pword', validators=[DataRequired()])
    two_fa_field = StringField('2FA', validators=[DataRequired()])
    submit = SubmitField('Sign In')


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    bad_typist_try = 0
    login_form = LoginForm()
    if login_form.validate_on_submit():
        flash("Login requested for user {}, two_fa_field={}".format(
            login_form.username.data, login_form.two_fa_field.data))
        return redirect(url_for('spell_check'))
    return render_template('login.html', bad_typist_try=bad_typist_try, form=login_form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')


@app.route('/spell_check', methods=['GET', 'POST'])
def spell_check():
    return render_template('spell_check.html')


@app.errorhandler(404)
def not_found(e):
    bad_typist_try = 1
    return render_template('login.html', bad_typist_try=bad_typist_try)


if __name__ == '__main__':
    app.run()
