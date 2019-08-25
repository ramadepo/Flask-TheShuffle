from flask import Flask, render_template, request, redirect, url_for, flash
from util.exts import db
from util.models import *
from util.hasher import Hasher
import config


app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


@app.route('/')
def index():
    return redirect(url_for('home_page'))


@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/subject')
def subject_page():
    return render_template('subject.html')


@app.route('/subject/<number>')
def subject_profile(number):
    return render_template('subject_profile.html')


@app.route('/history')
def history_page():
    return render_template('history.html')


@app.route('/log')
def log_page():
    return render_template('log.html')


@app.route('/user')
def user_page():
    return render_template('user.html')


@app.route('/user/<username>')
def user_profile(username):
    return render_template('user_profile.html')


@app.route('/user/signup', methods=['POST'])
def signup():
    # data = {'signup_email': <String>, 'signup_username': <String>, 'signup_password': <String>}
    data = request.form
    account_email = Account.query.filter(
        Account.email == data['signup_email']).first()
    account_username = Account.query.filter(
        Account.username == data['signup_username']).first()

    if not (data['signup_email'] and data['signup_username'] and data['signup_password']):
        flash('Input must not be empty.', 'danger')
    elif account_email or account_username:
        flash('Email or Username has been used.', 'danger')
    else:
        while True:
            id = Hasher.hash(6)
            account_id = Account.query.filter(Account.id == id).first()
            if not account_id:
                break
        email = data['signup_email']
        username = data['signup_username']
        password = Hasher.sha256(data['signup_password'])
        permission = -1
        new_account = Account(
            id=id, email=email, username=username, password=password, permission=permission)
        
        db.session.add(new_account)
        db.session.commit()

    return redirect(url_for('user_page'))


@app.route('/user/signin', methods=['POST'])
def signin():
    # data = {'signin_username': <String>, 'signin_password': <String>}
    data = request.form

    return redirect(url_for('user_page'))


@app.route('/certificate/<account_id>/<certification>')
def certificate(account_id, certification):
    check = Hasher.generate_certification(account_id)
    if certification == check:
        return 'Yes'
    else:
        return 'No'


if __name__ == '__main__':
    app.run()
