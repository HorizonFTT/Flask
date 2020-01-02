import click
from flask import Flask
app = Flask(__name__)


@app.cli.command()
def hello():
    click.echo('Hello, Human!')


@app.route('/greet', defaults={'name': 'Programmer'})
@app.route('/greet/<name>')
def greet(name):
    return '<h1>Hello, %s!</h1>' % name
