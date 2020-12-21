from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def createApp(obj):
    app = Flask(__name__)
    app.config.from_object(obj)
    db.init_app(app)
    migrate.init_app(app, db)
    from oasystem.user.views import userbp
    app.register_blueprint(userbp)
    return app
