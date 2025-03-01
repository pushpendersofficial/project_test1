import datetime
import os

from flask import Flask, render_template, redirect, url_for
from forms import SignupForm

from models import Signups
from database import db_session,init_db

app = Flask(__name__)
app.secret_key = os.environ['APP_SECRET_KEY']

@app.route("/", methods=('GET', 'POST'))
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        signup = Signups(name=form.name.data, email=form.email.data, date_signed_up=datetime.datetime.now())
        db_session.add(signup)
        db_session.commit()
        return redirect(url_for('success'))
    return render_template('signup.html', form=form)

@app.route("/success")
def success():
    return render_template('success.html')

if __name__ == '__main__':
    init_db()

    prod_or_test=os.environ.get('build_env') 
    if prod_or_test =='production': 
        app.run(host='0.0.0.0', port=5090, debug=True) 
      
    if prod_or_test =='testing': 
        app.run(host='0.0.0.0', port=5091, debug=True)
