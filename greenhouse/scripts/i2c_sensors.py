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

# --- Logging configuration ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
log = logging.getLogger("i2c_sensors")

# --- MQTT broker configuration ---
BROKER   = "localhost"
PORT     = 1883
TOP_LIGHT = "sensors/light"
TOP_SOIL  = "sensors/soil"
TOP_TEMP  = "sensors/temp"
TOP_HUM   = "sensors/hum"

mqttc = mqtt.Client(protocol=mqtt.MQTTv311)
mqttc.connect(BROKER, PORT, keepalive=60)

# --- I2C initialization with multiplexer ---
# Raspberry Pi I2C bus → TCA9548A multiplexer
# Channel mapping:
#   CH0 → BH1750 light sensor
#   CH1 → ADS1115 (soil moisture via analog input)
#   CH2 → SHT31 temperature & humidity sensor
i2c = busio.I2C(board.SCL, board.SDA)
tca = TCA9548A(i2c)

bh1750 = adafruit_bh1750.BH1750(tca[0])
ads    = ADS.ADS1115(tca[1])
chan   = AnalogIn(ads, ADS.P0)  # SMH13-M analog soil moisture sensor connected to A0
sht    = adafruit_sht31d.SHT31D(tca[2])

log.info("Sensors initialised (BH1750@CH0, ADS1115@CH1, SHT31@CH2)")

def safe_publish(topic, payload):
    """
    Publish MQTT message with retain flag enabled.
    Retain ensures the last value is always available to new subscribers.
    """
    mqttc.publish(topic, payload, retain=True)
    log.debug("Published → %s : %s", topic, payload)

while True:
    try:
        # --- Light sensor (BH1750) ---
        try:
            lux = bh1750.lux or 0.0
        except Exception as e:
            log.warning("BH1750 read failed: %s", e)
            lux = 0.0

        # --- Soil moisture sensor (via ADS1115 ADC) ---
        try:
            soil_raw = chan.value  # 16-bit ADC value (0–65535)
        except Exception as e:
            log.warning("ADS1115 read failed: %s", e)
            soil_raw = -1

        # --- Temperature & Humidity sensor (SHT31) ---
        try:
            temp_c = float(f"{sht.temperature:.2f}")
            hum    = float(f"{sht.relative_humidity:.2f}")
        except Exception as e:
            log.warning("SHT31 read failed: %s", e)
            temp_c = -99.0
            hum    = -1.0

        # --- MQTT publish ---
        safe_publish(TOP_LIGHT, f"{lux:.2f}")
        safe_publish(TOP_SOIL,  str(soil_raw))
        safe_publish(TOP_TEMP,  f"{temp_c:.2f}")
        safe_publish(TOP_HUM,   f"{hum:.2f}")

        # Log summary for monitoring
        log.info("Light=%.2f lux | Soil(raw)=%s | Temp=%.2f °C | Hum=%.2f %%",
                 lux, soil_raw, temp_c, hum)

        time.sleep(5)

    except Exception as e:
        # Ensure the loop never stops due to unexpected errors
        log.error("Main loop error: %s", e)
        time.sleep(5)

