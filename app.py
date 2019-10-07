from flask import Flask, render_template, request, url_for, redirect, flash
from flask_wtf import FlaskForm, form
from wtforms import Form, StringField, TextAreaField, validators, StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo
from flask_bootstrap import Bootstrap
import os

app = Flask(__name__)
Bootstrap(app)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'bd0c7d441f27d441f27567d441f2b6176a'


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


userdict = {'tester': {'password': 'testpass', '2fa': '5555555555'}}


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    global userdict
    if login_form.validate_on_submit():
        if (userdict[login_form.username.data]['password'] == login_form.password.data and
                userdict[login_form.username.data]['2fa'] == login_form.two_fa_field.data):
            flash("Login successful for user {}".format(login_form.username.data), 'success')
            return redirect(url_for('spell_check'))
        else:
            flash("Login unsuccessful")
    return render_template('login.html', form=login_form)


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
    return render_template('spell_check.html')


if __name__ == '__main__':
    app.run(debug=True)
