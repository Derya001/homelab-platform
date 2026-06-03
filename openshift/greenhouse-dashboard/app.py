from flask import Flask, render_template, jsonify
import subprocess
import re

app = Flask(__name__)

def get_sensor_data():
    try:
        result = subprocess.run(
            ["timeout", "12", "python3", "/home/pi/szakdoga/i2c_sensors.py"],
            capture_output=True, text=True, timeout=15
        )
        output = result.stdout
        light = re.search(r'Light=([\d.]+)', output)
        soil = re.search(r'Soil\(raw\)=(\d+)', output)
        temp = re.search(r'Temp=([\d.]+)', output)
        hum = re.search(r'Hum=([\d.]+)', output)
        return {
            "light": float(light.group(1)) if light else None,
            "soil": int(soil.group(1)) if soil else None,
            "temperature": float(temp.group(1)) if temp else None,
            "humidity": float(hum.group(1)) if hum else None
        }
    except Exception as e:
        return {"error": str(e)}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/sensors')
def sensors():
    return jsonify(get_sensor_data())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
