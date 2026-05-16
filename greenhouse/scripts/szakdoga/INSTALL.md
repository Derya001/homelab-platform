# Üvegház rendszer — telepítési jegyzetek
# Raspberry Pi 4, Raspberry Pi OS Bookworm (Debian 12), Python 3.11, Node-RED v4

---

## 1. I2C engedélyezése

```bash
sudo raspi-config nonint do_i2c 0
# ellenőrzés:
ls /dev/i2c*
# kell hogy legyen: /dev/i2c-1
```

---

## 2. apt csomagok

```bash
sudo apt install -y mosquitto mosquitto-clients
sudo systemctl enable --now mosquitto
```

---

## 3. Python könyvtárak (rootként kell, mert a service root alatt fut)

```bash
pip install \
    adafruit-blinka \
    adafruit-circuitpython-tca9548a \
    adafruit-circuitpython-bh1750 \
    adafruit-circuitpython-sht31d \
    adafruit-circuitpython-ads1x15 \
    paho-mqtt \
    --break-system-packages
```

Ellenőrzés:
```bash
python3 -c "import adafruit_tca9548a, adafruit_bh1750, adafruit_sht31d, adafruit_ads1x15.ads1115, paho.mqtt.client; print('OK')"
```

---

## 4. Node-RED dashboard

```bash
cd ~/.node-red
npm install node-red-dashboard
sudo systemctl restart nodered
```

---

## 5. systemd service telepítése

```bash
sudo cp /home/pi/szakdoga/i2c-sensors.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now i2c-sensors
systemctl status i2c-sensors
```

---

## 6. sudoers — a Node-RED exec node-ok miatt kell (pump, lámpa scriptek)

```bash
sudo visudo
```

Add hozzá a végére:
```
pi ALL=(ALL) NOPASSWD: /usr/bin/python3
```

---

## 7. Node-RED flow importálása

1. Nyisd meg: `http://raspberrypi.local:1880`
2. Jobb felső sarok → Import
3. Másold be a `flows_greenhouse_complete.json` tartalmát
4. Import → Deploy

Dashboard elérhető: `http://raspberrypi.local:1880/ui`

---

## Fájlok helye a Pi-n

```
/home/pi/szakdoga/
├── I2C_sensors.py          # fő szenzorolvasó service
├── lamp_on.py              # GPIO17 HIGH
├── lamp_off.py             # GPIO17 LOW
├── pump_on_for.py          # GPIO27 HIGH, paraméter: másodperc
├── flows_greenhouse_complete.json
├── i2c-sensors.service     # -> /etc/systemd/system/ alá kell másolni
└── INSTALL.md              # ez a fájl

/etc/systemd/system/
└── i2c-sensors.service
```

---

## Gyors újraindítás után ellenőrzés

```bash
systemctl status i2c-sensors
systemctl status mosquitto
# MQTT live monitor:
mosquitto_sub -t "sensors/#" -v
```
