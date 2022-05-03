from flask import (
    Blueprint, render_template
)
from flaskr.hardware import fan_controler, sensor_controler

bp = Blueprint('home', __name__)


@bp.route('/')
def index():
    fc = fan_controler.FanController()
    sc = sensor_controler.SensorController()

    return render_template(
        'home.html',
        fan_status=fc.get_fan_status_summary(),
        fan_metrics=fc.get_metrics(),
        sensor_status=sc.get_sensor_status_summary(),
        sensor_metrics=sc.get_metrics()
    )
