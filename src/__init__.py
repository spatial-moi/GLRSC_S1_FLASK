import flask
import os
from flask import Flask
from src.config import config
from src.models import db
from flask_migrate import Migrate
from src.routes import account_bp, request_bp, meeting_bp
from datetime import timedelta
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt


app = Flask(__name__)
bcrypt = Bcrypt(app)
migrate = Migrate()
app = flask.Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("PRODUCTION_DATABASE_URI")
app.config["DATABASE_URL"] = os.getenv("PRODUCTION_DATABASE_URI")
app.config["DATABASE_URI"] = os.getenv("PRODUCTION_DATABASE_URI")
app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies", "json", "query_string"]
app.config['JWT_SECRET_KEY'] = 'moairoutingclass27981231'
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)
app.config['SQLALCHEMY_POOL_SIZE'] = 30
app.config['SQLALCHEMY_MAX_OVERFLOW'] = 30
app.config['SQLALCHEMY_POOL_TIMEOUT'] = 60
app.config['SQLALCHEMY_POOL_RECYCLE'] = 10

cors_origin = [
    'https://spatial-moi.github.io',
    'http://localhost:3000'
]

cors = CORS(app, resources={r'/*': {"origins": cors_origin}})
jwt = JWTManager(app)


def create_app(config_mode):
    app.config.from_object(config[config_mode])

    # register routes
    app.register_blueprint(account_bp)
    app.register_blueprint(request_bp)
    app.register_blueprint(meeting_bp)

    db.init_app(app)
    migrate.init_app(app, db)

    from src.models import Account, MeetingRequest, AccountRequest, ActiveMeeting
    with app.app_context():
        db.drop_all()

    return app
