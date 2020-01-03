import click
import os
import sys
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
from flask_sqlalchemy import SQLAlchemy

WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'secret string')

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URI', prefix + os.path.join(app.root_path, 'data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Note(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    body=db.Column(db.Text)

@app.cli.command()
def initDB():
    db.create_all()
    click.echo('Initialized database.')
