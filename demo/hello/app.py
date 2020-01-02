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
)
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'secret string')

colors = ['blue', 'white', 'red']


@app.cli.command()
def say_hello():
    click.echo('Hello, Human!')


@app.route('/greet', defaults={'name': 'Programmer'})
@app.route('/greet/<name>')
def greet(name):
    return '<h1>Hello, %s!</h1>' % name


@app.route('/hello')
def hello():
    name = request.args.get('name', 'Flask')
    if name is None:
        name = request.cookies.get('name', 'Human')
    response = f'<h1>Hello, {name}!</h1>'
    if 'logged_in' in session:
        response += '[Authenticated]'
    else:
        response += '[Not Authenticated]'
    return response


@app.route('/goBack/<int:year>')
def go_back(year):
    return f'<p>Welcome to {(2020 - year)}!</p>'


@app.route(f'/colors/<any({str(colors)[1:-1]}):color>')
def three_colors(color):
    return '<p>Love is patient and kind. Love is not jealous or boastful or proud or rude.</p>'


@app.route('/fuck')
def fuck():
    return redirect(url_for('hello'))


@app.route('/foo')
def foo():
    return jsonify(name='Grey Li', gender='male')


@app.route('/set/<name>')
def set_cookie(name):
    response = make_response(redirect(url_for('hello')))
    response.set_cookie('name', name)
    return response


@app.route('/login')
def login():
    session['logged_in'] = True
    return redirect(url_for('hello'))


@app.route('/logout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in')
        return redirect(url_for('hello'))
