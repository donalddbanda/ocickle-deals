from flask import Flask
from .extensions import db, migrate, cors, login_manager
from app.routes import admin_bp, waiting_list_bp
from app import config


def create_app():
    app = Flask(__name__)
    app.config.from_object(config.Config())


    db.init_app(app)
    cors.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_view = "/admin/login"

    app.register_blueprint(admin_bp)
    app.register_blueprint(waiting_list_bp)

    return app
