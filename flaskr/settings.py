from flask import (
    Blueprint, render_template, request, redirect
)

from flaskr.model import Location, PWM, Fan, FanTempDuty, Sensor, db
from flaskr.util import http
from flaskr.hardware import pi_driver

bp = Blueprint('settings', __name__, url_prefix='/settings')


def delete_record(val_dict, model):
    ids = []
    for i in val_dict:
        if val_dict[i]['id'] != "-1":
            ids.append(val_dict[i]['id'])

    for row in model.query.filter(~model.id.in_(ids)):
        db.session.delete(row)
        db.session.commit()


@bp.route('/')
def index():
    location = Location.query.order_by(Location.name.asc()).all()
    pwm = PWM.query.order_by(PWM.id.asc()).all()
    fan = Fan.query.order_by(Fan.id.asc()).all()
    fan_temp_duty = FanTempDuty.query.order_by(FanTempDuty.id.asc()).all()
    sensor = Sensor.query.order_by(Sensor.id.asc()).all()
    pi = pi_driver.PiDriver()
    av_sensors = []

    for i in pi.list_w1_sensors():
        if Sensor.query.filter_by(bus_id=i['id']).first() is None:
            av_sensors.append(i['id'])

    return render_template(
        'settings.html',
        locations=location,
        pwms=pwm,
        fans=fan,
        fanTempDuties=fan_temp_duty,
        sensors=sensor,
        av_sensors=av_sensors,
        pwm_pins=pi.get_pwm_channel_pins(),
        ports=pi.get_ports()
    )


@bp.route('/update/fan', methods=["POST"])
def update_fan():
    val_dict = http.parse_multi_form(request.form)['fan']

    delete_record(val_dict, Fan)

    for i in val_dict:
        if val_dict[i]['id'] != "-1":
            fan = Fan.query.filter_by(id=val_dict[i]['id']).first()
            changed = False

            if fan.location != val_dict[i]['location']:
                fan.location = val_dict[i]['location']
                changed = True
            if fan.tacho_pin != val_dict[i]['tacho_pin']:
                fan.tacho_pin = val_dict[i]['tacho_pin']
                changed = True
            if changed:
                db.session.commit()
        else:
            fan = Fan(val_dict[i]['location'], val_dict[i]['tacho_pin'])
            db.session.add(fan)
            db.session.commit()

    return redirect("/settings/", code=302)


@bp.route('/update/fantempduty', methods=["POST"])
def update_fantempduty():
    val_dict = http.parse_multi_form(request.form)['ftd']

    delete_record(val_dict, FanTempDuty)

    for i in val_dict:
        if val_dict[i]['id'] != "-1":
            fan_temp_duty = FanTempDuty.query.filter_by(id=val_dict[i]['id']).first()
            changed = False

            if fan_temp_duty.location != val_dict[i]['location']:
                fan_temp_duty.location = val_dict[i]['location']
                changed = True
            if fan_temp_duty.temperature != val_dict[i]['temp']:
                fan_temp_duty.temperature = val_dict[i]['temp']
                changed = True
            if fan_temp_duty.duty != val_dict[i]['duty']:
                fan_temp_duty.duty = val_dict[i]['duty']
                changed = True
            if changed:
                db.session.commit()
        else:
            fan_temp_duty = FanTempDuty(val_dict[i]['location'], val_dict[i]['temp'], val_dict[i]['duty'])
            db.session.add(fan_temp_duty)
            db.session.commit()

    return redirect("/settings/", code=302)


@bp.route('/update/location', methods=["POST"])
def update_location():
    val_dict = http.parse_multi_form(request.form)['location']

    delete_record(val_dict, Location)

    for i in val_dict:
        if val_dict[i]['id'] != "-1":
            location = Location.query.filter_by(id=val_dict[i]['id']).first()

            if location.name != val_dict[i]['name']:
                location.name = val_dict[i]['name']
                db.session.commit()
        else:
            location = Location(val_dict[i]['name'])
            db.session.add(location)
            db.session.commit()

    return redirect("/settings/", code=302)


@bp.route('/update/pwm', methods=["POST"])
def update_pwm():
    val_dict = http.parse_multi_form(request.form)['pwm']

    delete_record(val_dict, PWM)

    for i in val_dict:
        if val_dict[i]['id'] != "-1":
            pwm = PWM.query.filter_by(id=val_dict[i]['id']).first()
            changed = False

            if pwm.channel != val_dict[i]['channel']:
                pwm.channel = val_dict[i]['channel']
                changed = True
            if pwm.location != val_dict[i]['location']:
                pwm.location = val_dict[i]['location']
                changed = True
            if pwm.pin != val_dict[i]['pin']:
                pwm.pin = val_dict[i]['pin']
                changed = True
            if changed:
                db.session.commit()
        else:
            pwm = PWM(val_dict[i]['channel'], val_dict[i]['location'], val_dict[i]['pin'])
            db.session.add(pwm)
            db.session.commit()

    return redirect("/settings/", code=302)


@bp.route('/update/sensor', methods=["POST"])
def update_sensor():
    val_dict = http.parse_multi_form(request.form)['sensor']

    delete_record(val_dict, Sensor)

    for i in val_dict:
        if val_dict[i]['id'] != "-1":
            sensor = Sensor.query.filter_by(id=val_dict[i]['id']).first()
            changed = False

            if sensor.location != val_dict[i]['location']:
                sensor.location = val_dict[i]['location']
                changed = True
            if sensor.bus_id != val_dict[i]['bus_id']:
                sensor.bus_id = val_dict[i]['bus_id']
                changed = True
            if sensor.type != val_dict[i]['type']:
                sensor.type = val_dict[i]['type']
                changed = True
            if changed:
                db.session.commit()
        else:
            sensor = Sensor(val_dict[i]['location'], val_dict[i]['bus_id'], val_dict[i]['type'])
            db.session.add(sensor)
            db.session.commit()

    return redirect("/settings/", code=302)
