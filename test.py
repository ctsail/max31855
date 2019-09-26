#!/usr/bin/python
from max31855 import MAX31855, MAX31855Error
import time, datetime

cs_pins = [25]
clock_pin = 23
data_pin = 22
units = "f"
thermocouples = []
for cs_pin in cs_pins:
    thermocouples.append(MAX31855(cs_pin, clock_pin, data_pin, units))

date=datetime.datetime.now()
file="/home/pi/Projects/max31855_logger/logs/{0}.csv".format(date.strftime("%Y%m%d%H%M%S"))

running = True
with open(file,"a") as log:
    while(running):
        try:
            for thermocouple in thermocouples:
                rj = thermocouple.get_rj()
                try:
                    tc = thermocouple.get()
                except MAX31855Error as e:
                    tc = "Error: "+ e.value
                    running = False
                log.write("{0}\n".format(tc))
                print("tc: {} and rj: {}".format(tc, rj))
            time.sleep(0.1)
        except KeyboardInterrupt:
            running = False

for thermocouple in thermocouples:
    thermocouple.cleanup()
