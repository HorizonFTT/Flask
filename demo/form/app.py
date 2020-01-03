import click
import os
from flask import (
    Flask,
    redirect,
    url_for,
    jsonify,
    make_response,
    session,
    request,
    render_template,
    Markup,
    flash,
)
from form import LoginForm

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'secret string')


@app.route('/basic', methods=['GET', 'POST'])
def basic():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        flash('Welcome home, %s!' % username)
        return redirect(url_for('basic'))
    return render_template('basic.html', form=form)
