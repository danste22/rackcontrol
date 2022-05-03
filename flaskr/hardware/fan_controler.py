from . import pi_driver
import time
import datetime
from flaskr.model import PWM, Fan, FanTempDuty, Location, Sensor, FanMetrics, db


class FanController:
    pi = None
    _fan_status = {}

    def __init__(self):
        self.pi = pi_driver.PiDriver()

    def cal_seq(self, pwm_pin, tacho_pin):
        last_measurement = 0
        # Zero counter
        self.pi.get_input_counter(tacho_pin)

        # Check fan
        for i in range(20, 101, 10):
            self.pi.set_duty(pwm_pin, i)
            time.sleep(4)
            curr_measurement = self.pi.get_input_counter(tacho_pin)

            if last_measurement >= curr_measurement:
                print("Fan init Error: No Fan speed change, for fan tacho: " + str(tacho_pin))

    def init_fans(self):
        for i in PWM.query.order_by(PWM.id.asc()).all():
            self.pi.init_pwm(i.pin)

            for j in Fan.query.filter_by(location=i.location).all():
                self.pi.init_input(j.tacho_pin)
                self.pi.init_input_callback(j.tacho_pin)
                self.cal_seq(i.pin, j.tacho_pin)

    def switch_off(self, location):
        pwm = PWM.query.filter_by(location=location).first()
        self.pi.set_duty(pwm.pin, 0)

    def set_temp_duty(self):
        for i in PWM.query.order_by(PWM.id.asc()).all():
            sensor = Sensor.query.filter_by(location=i.location).first()
            ftd = FanTempDuty.query \
                .filter(FanTempDuty.temperature <= int(round(self.pi.get_w1_temp(sensor.bus_id) / 1000))) \
                .filter(FanTempDuty.location == i.location) \
                .order_by(FanTempDuty.temperature.desc()) \
                .first()
            self.pi.set_duty(i.pin, ftd.duty)

    def record_speed(self):
        timestamp = datetime.datetime.utcnow()

        for i in Fan.query.order_by(Fan.id.asc()).all():
            counter = int(round(self.pi.get_input_counter(i.tacho_pin) / 2, 2))

            if counter <= 1:
                self._fan_status[i.id] = False
            else:
                self._fan_status[i.id] = True

            db.session.add(FanMetrics(timestamp, i.id, counter))
            db.session.commit()

    @staticmethod
    def get_metrics():
        metrics_dates = []
        metrics_label = []
        metrics_data = {}

        fan_metrics = FanMetrics.query \
            .join(Fan, FanMetrics.fan_id == Fan.id) \
            .join(Location, Fan.location == Location.id) \
            .add_columns(Fan.id, Location.name, FanMetrics.date, FanMetrics.value) \
            .order_by(FanMetrics.date.asc(), FanMetrics.id.asc()) \
            .all()

        for i in fan_metrics:
            label = i.name + str(i.id)
            date = i.date.strftime("%H:%M:%S")

            if date not in metrics_dates:
                metrics_dates.append(date)

            if label not in metrics_label:
                metrics_label.append(label)

        # fix that values are not applied if N/A for timecode
        for i in fan_metrics:
            label = i.name + str(i.id)

            if label in metrics_data:
                temp = metrics_data[label]
                temp.append(int(i.value))
                metrics_data[label] = temp
            else:
                metrics_data[label] = [int(i.value)]

        return dict(dates=metrics_dates, data=metrics_data)

    def get_fan_status_summary(self):
        active_cnt = 0

        for i in self._fan_status:
            if self._fan_status[i]:
                active_cnt += 1

        return dict(total=len(self._fan_status), active=active_cnt)
