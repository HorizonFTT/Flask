from flask import Flask
from bluelog.settings import config
from bluelog.extensions import bootstrap, db, moment, ckeditor, mail

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('bluelog')
    app.config.from_object(config[config_name])

    register_extensions(app)
    register_blueprints(app)


    return app


def register_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    ckeditor.init_app(app)
    mail.init_app(app)
    moment.init_app(app)



def register_blueprints(app):
    app.register_blueprint(blog)
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(auth, url_prefix='/auth')
