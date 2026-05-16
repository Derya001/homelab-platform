#!/usr/bin/env python3
import time
import sys
import logging

import paho.mqtt.client as mqtt
import board
import busio
from adafruit_tca9548a import TCA9548A
import adafruit_bh1750
import adafruit_sht31d
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
log = logging.getLogger("I2C_sensors")

BROKER    = "localhost"
PORT      = 1883
TOP_LIGHT = "sensors/light"
TOP_SOIL  = "sensors/soil"
TOP_TEMP  = "sensors/temp"
TOP_HUM   = "sensors/hum"

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
mqttc.connect(BROKER, PORT, keepalive=60)

# CH0 -> BH1750  (fény)
# CH1 -> ADS1115 (talajnedvesség)
# CH2 -> SHT31   (hőmérséklet + páratartalom)
I2C = busio.I2C(board.SCL, board.SDA)
tca = TCA9548A(I2C)

bh1750 = adafruit_bh1750.BH1750(tca[0])
ads    = ADS.ADS1115(tca[1])
chan   = AnalogIn(ads, 0)        # 0 = A0 csatorna
sht    = adafruit_sht31d.SHT31D(tca[2])

log.info("Sensors initialised (BH1750@CH0, ADS1115@CH1, SHT31@CH2)")

def safe_publish(topic, payload):
    mqttc.publish(topic, payload, retain=True)
    log.debug("Published -> %s : %s", topic, payload)

while True:
    try:
        try:
            lux = bh1750.lux or 0.0
        except Exception as e:
            log.warning("BH1750 read failed: %s", e)
            lux = 0.0

        try:
            soil_raw = chan.value
        except Exception as e:
            log.warning("ADS1115 read failed: %s", e)
            soil_raw = -1

        try:
            temp_c = round(sht.temperature, 2)
            hum    = round(sht.relative_humidity, 2)
        except Exception as e:
            log.warning("SHT31 read failed: %s", e)
            temp_c = -99.0
            hum    = -1.0

        safe_publish(TOP_LIGHT, f"{lux:.2f}")
        safe_publish(TOP_SOIL,  str(soil_raw))
        safe_publish(TOP_TEMP,  f"{temp_c:.2f}")
        safe_publish(TOP_HUM,   f"{hum:.2f}")

        log.info("Light=%.2f lux | Soil(raw)=%s | Temp=%.2f C | Hum=%.2f %%",
                 lux, soil_raw, temp_c, hum)

        time.sleep(5)

    except Exception as e:
        log.error("Main loop error: %s", e)
        time.sleep(5)
