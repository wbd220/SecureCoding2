from flask import Flask, render_template, request, url_for, redirect, flash, session
from flask_wtf import FlaskForm, form
from wtforms import Form, StringField, TextAreaField, validators, StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo
from flask_bootstrap import Bootstrap
# from flask_login import LoginManager, logout_user  #this is for flask-login
# from app import login   # this is for flask-login
from werkzeug.security import generate_password_hash, check_password_hash
import os
import subprocess

app = Flask(__name__)
Bootstrap(app)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'bd0c7d441f27d441f27567d441f2b6176a'


# login = LoginManager(app)    # this is for flask-login


class LoginForm(FlaskForm):
    username = StringField('uname', validators=[DataRequired()])
    password = PasswordField('pword', validators=[DataRequired()])
    two_fa_field = StringField('2FA', validators=[DataRequired()])
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('uname', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('pword', validators=[DataRequired()])
    confirm_password = PasswordField('confirm pword', validators=[DataRequired(), EqualTo('password')])
    two_fa_field = StringField('2FA', validators=[DataRequired()])
    submit = SubmitField('Register me')


class SpellCheckForm(FlaskForm):
    text2test = TextAreaField('inputtext', render_kw={"rows": 15, "cols": 45})
    # misspelled_stuff = TextAreaField('misspelled')
    submit = SubmitField("Check Spelling")


userdict = {'tester': {'password': 'testpass', '2fa': '5555555555'}}
result = ''

@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    global userdict
    if login_form.validate_on_submit():
        if login_form.username.data in userdict:
            if (userdict[login_form.username.data]['password'] == login_form.password.data and
                    userdict[login_form.username.data]['2fa'] == login_form.two_fa_field.data):
                flash("Login successful for user {}".format(login_form.username.data), 'success')
                session['username'] = login_form.username.data  # create session cookie
                return render_template('login.html', form=login_form, result='success')
            else:
                flash("Login unsuccessful")
                return render_template('login.html', form=login_form, result='failure')
        else:
            flash("You are not registered user, please register")
            return render_template('login.html', form=login_form, result='failure')
    return render_template('login.html', form=login_form, result='')


@app.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegistrationForm()
    if register_form.validate_on_submit():
        userdict[register_form.username.data] = {'password': register_form.password.data,
                                                 '2fa': register_form.two_fa_field.data}
        flash(f"Registration successful for user {register_form.username.data} Please login")
        return redirect(url_for('login'))
    return render_template('register.html', form=register_form)


@app.route('/spell_check', methods=['GET', 'POST'])
def spell_check():
    if 'username' in session:
        spell_check_form = SpellCheckForm()
        if spell_check_form.validate_on_submit():
            input_text = spell_check_form.text2test.data  # put text from form into a field
            input_file = open("input_file.txt", 'w')  # open file
            input_file.write(str(input_text))  # put text into file
            input_file.close()  # close the file
            # call subprocess
            misspelled = subprocess.run(['./a.out', './input_file.txt', './wordlist.txt'],
                                              stdout=subprocess.PIPE).stdout.decode('utf-8').replace("\n", ", ").rstrip(
                ", ")
            # spell_check_form.misspelled_stuff.data = misspelled_words
            return render_template('spell_check.html', form=spell_check_form, misspelled=misspelled)
        return render_template('spell_check.html', form=spell_check_form)
    else:
        flash("You are not logged in, Please log in")
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('username', None)
    return redirect(url_for('login'))


# @app.route('/logout')   #  for flask-login
# def logout():
#     logout_user()
#     return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
