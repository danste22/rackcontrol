import os

from flask import Flask
from flask_apscheduler import APScheduler
from flask_minify import Minify
from flask_sqlalchemy import SQLAlchemy

from flaskr.hardware import pi_driver

scheduler = APScheduler()
db = SQLAlchemy()
pi = pi_driver.PiDriver()


def create_app(config=None):
    app = Flask(__name__, instance_relative_config=True)

    # Minify view responses
    Minify(app=app, html=True, js=True, cssless=True)

    # Use only if no external config set
    if config is None:
        app.config.from_pyfile("rackcontrol.cfg")
    else:
        app.config.update(config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # database
    db.init_app(app)
    db.app = app

    from flaskr.model import Location, PWM, Fan, FanTempDuty, Sensor, SensorMetrics, FanMetrics
    if app.config["FLASK_ENV"] == "development":
        db.drop_all()
        db.create_all()
        db.session.commit()
        from flaskr.util import dev_init
    else:
        db.create_all()
        db.session.commit()

    # apply the blueprints to the app
    from flaskr import home, console, settings
    app.register_blueprint(home.bp)
    app.register_blueprint(console.bp)
    app.register_blueprint(settings.bp)
    app.add_url_rule("/", endpoint="index")

    # Init driver
    pi.init_app(app)
    pi.app = app

    # Init fan controller
    from .hardware import fan_controler
    fc = fan_controler.FanController()
    fc.init_fans()

    # sheduler
    scheduler.init_app(app)
    scheduler.app = app

    from flaskr import tasks
    scheduler.start()

    return app
