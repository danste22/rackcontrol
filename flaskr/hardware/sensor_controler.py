from . import pi_driver
import datetime
from flaskr.model import Location, Sensor, SensorMetrics, db


class SensorController:
    pi = None
    _sensor_status = {}

    def __init__(self):
        self.pi = pi_driver.PiDriver()

    def record_temp(self):
        timestamp = datetime.datetime.utcnow()

        for i in Sensor.query.order_by(Sensor.id.asc()).all():
            if self.pi.get_w1_temp(i.bus_id) is None:
                self._sensor_status[i.id] = False
            else:
                self._sensor_status[i.id] = True

            db.session.add(SensorMetrics(timestamp, i.id, self.pi.get_w1_temp(i.bus_id)))
            db.session.commit()

    @staticmethod
    def get_metrics():
        metrics_label = []
        metrics_dates = []
        metrics_data = {}

        for i in Location.query.order_by(Location.id.asc()).all():
            metrics_label.append(i.name)

        sensor_metrics = SensorMetrics.query\
            .join(Sensor, Sensor.id == SensorMetrics.sensor_id)\
            .join(Location, Location.id == Sensor.location)\
            .add_columns(SensorMetrics.date, Location.name, SensorMetrics.value)\
            .order_by(SensorMetrics.date.asc(), SensorMetrics.sensor_id.asc())\
            .all()

        for i in sensor_metrics:
            sens_value = round(i.value/1000, 1)
            date = i.date.strftime("%H:%M:%S")

            if date not in metrics_dates:
                metrics_dates.append(date)

            if i.name in metrics_data:
                temp = metrics_data[i.name]
                temp.append(sens_value)
                metrics_data[i.name] = temp
            else:
                metrics_data[i.name] = [sens_value]

        return dict(dates=metrics_dates, data=metrics_data)

    def get_sensor_status_summary(self):
        active_cnt = 0

        for i in self._sensor_status:
            if self._sensor_status[i]:
                active_cnt += 1

        return dict(total=len(self._sensor_status), active=active_cnt)
