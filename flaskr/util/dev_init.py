from flaskr import db
from flaskr.model import Location, PWM, Fan, FanTempDuty, Sensor

for i in ['TOP', 'PSU', 'EXT']:
    db.session.add(Location(name=i))
db.session.commit()

db.session.add(PWM(channel=0, location=Location.query.filter_by(name="TOP").first().id, pin=18))
db.session.add(PWM(channel=1, location=Location.query.filter_by(name="PSU").first().id, pin=13))
db.session.commit()

db.session.add(Fan(location=Location.query.filter_by(name="TOP").first().id, tacho_pin=17))
db.session.add(Fan(location=Location.query.filter_by(name="TOP").first().id, tacho_pin=22))
db.session.add(Fan(location=Location.query.filter_by(name="PSU").first().id, tacho_pin=27))
db.session.commit()

db.session.add(FanTempDuty(location=Location.query.filter_by(name="TOP").first().id, temperature=20, duty=20))
db.session.add(FanTempDuty(location=Location.query.filter_by(name="TOP").first().id, temperature=25, duty=40))
db.session.add(FanTempDuty(location=Location.query.filter_by(name="TOP").first().id, temperature=30, duty=60))
db.session.add(FanTempDuty(location=Location.query.filter_by(name="TOP").first().id, temperature=35, duty=80))
db.session.add(FanTempDuty(location=Location.query.filter_by(name="TOP").first().id, temperature=40, duty=100))
db.session.add(FanTempDuty(location=Location.query.filter_by(name="PSU").first().id, temperature=20, duty=20))
db.session.add(FanTempDuty(location=Location.query.filter_by(name="PSU").first().id, temperature=25, duty=40))
db.session.add(FanTempDuty(location=Location.query.filter_by(name="PSU").first().id, temperature=30, duty=60))
db.session.add(FanTempDuty(location=Location.query.filter_by(name="PSU").first().id, temperature=35, duty=80))
db.session.add(FanTempDuty(location=Location.query.filter_by(name="PSU").first().id, temperature=40, duty=100))
db.session.commit()

db.session.add(
    Sensor(location=Location.query.filter_by(name="TOP").first().id, bus_id="10-000802e772de", type="1W"))
db.session.add(
    Sensor(location=Location.query.filter_by(name="PSU").first().id, bus_id="10-000802e80140", type="1W"))
db.session.add(
    Sensor(location=Location.query.filter_by(name="EXT").first().id, bus_id="10-000802e73dd2", type="1W"))
db.session.commit()
