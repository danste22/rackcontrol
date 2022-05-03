from flaskr import db
import datetime


class Node(db.Model):
    __tablename__ = "node"

    id = db.Column(db.Integer, primary_key=True)
    hostname = db.Column(db.String(20), unique=True, nullable=True)
    tty = db.Column(db.String(20), unique=True, nullable=True)
    ip = db.Column(db.String(20), unique=True, nullable=True)

    def __init__(self, hostname, tty, ip):
        self.hostname = hostname
        self.tty = tty
        self.ip = ip

    def to_string(self):
        return dict(id=self.id, hostname=self.hostname, tty=self.tty, ip=self.ip)


class Location(db.Model):
    __tablename__ = "location"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=True)
    pwms = db.relationship("PWM", backref=db.backref("pwm"))
    fans = db.relationship("Fan", backref=db.backref("fan"))
    ftds = db.relationship("FanTempDuty", backref=db.backref("fan_temp_duty"))
    sensors = db.relationship("Sensor", backref=db.backref("sensor"))

    def __init__(self, name):
        self.name = name

    def to_string(self):
        return dict(id=self.id, name=self.name, pwms=self.pwms, fans=self.fans, ftds=self.ftds, sensors=self.sensors)


class PWM(db.Model):
    __tablename__ = "pwm"

    id = db.Column(db.Integer, primary_key=True)
    channel = db.Column(db.Integer, unique=True, nullable=False)
    location = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    pin = db.Column(db.Integer, unique=True, nullable=True)

    def __init__(self, channel, location, pin):
        self.channel = channel
        self.location = location
        self.pin = pin

    def to_string(self):
        return dict(id=self.id, channel=self.channel, location=self.location, pin=self.pin)


class Fan(db.Model):
    __tablename__ = "fan"

    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    tacho_pin = db.Column(db.Integer, unique=True, nullable=True)
    metrics = db.relationship("FanMetrics", backref=db.backref("fan_metrics"))

    def __init__(self, location, tacho_pin):
        self.location = location
        self.tacho_pin = tacho_pin

    def to_string(self):
        return dict(id=self.id, location=self.location, tacho_pin=self.tacho_pin)


class FanTempDuty(db.Model):
    __tablename__ = "fan_temp_duty"

    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    temperature = db.Column(db.Integer, nullable=True)
    duty = db.Column(db.Integer, nullable=True)

    def __init__(self, location, temperature, duty):
        self.location = location
        self.temperature = temperature
        self.duty = duty

    def to_string(self):
        return dict(id=self.id, location=self.location, temperature=self.temperature, duty=self.duty)


class Sensor(db.Model):
    __tablename__ = "sensor"

    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    bus_id = db.Column(db.String(20), nullable=True)
    type = db.Column(db.String(10), nullable=True)
    metrics = db.relationship("SensorMetrics", backref=db.backref("sensor_metrics"))

    def __init__(self, location, bus_id, type):
        self.location = location
        self.bus_id = bus_id
        self.type = type

    def to_string(self):
        return dict(id=self.id, location=self.location, bus_id=self.bus_id, type=self.type)


class SensorMetrics(db.Model):
    __tablename__ = "sensor_metrics"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.TIMESTAMP, default=datetime.datetime.utcnow())
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensor.id'), nullable=False)
    value = db.Column(db.Float, nullable=False)

    def __init__(self, date, sensor_id, value):
        self.date = date
        self.sensor_id = sensor_id
        self.value = value

    def to_string(self):
        return dict(id=self.id, date=self.date, sensorId=self.sensor_id, value=self.value)


class FanMetrics(db.Model):
    __tablename__ = "fan_metrics"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.TIMESTAMP, default=datetime.datetime.utcnow())
    fan_id = db.Column(db.Integer, db.ForeignKey('fan.id'), nullable=False)
    value = db.Column(db.Float, nullable=False)

    def __init__(self, date, fan_id, value):
        self.date = date
        self.fan_id = fan_id
        self.value = value

    def to_string(self):
        return dict(id=self.id, date=self.date, fanId=self.fan_id, value=self.value)
