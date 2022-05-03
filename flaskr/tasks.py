from flaskr import scheduler
from flaskr.hardware import pi_driver, fan_controler, sensor_controler

fc = fan_controler.FanController()
sc = sensor_controler.SensorController()
pi = pi_driver.PiDriver()


# Add tasks to clean-up metrics after 24h


@scheduler.task(
    "interval",
    id="job_sync",
    seconds=10,
    max_instances=1
)
def task1():
    # print("All ports: " + str(pi.get_ports()))

    fc.set_temp_duty()


@scheduler.task(
    "interval",
    id="job_sync",
    seconds=60,
    max_instances=1
)
def task2():
    fc.record_speed()
    sc.record_temp()
