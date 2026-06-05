from flask import Flask, render_template, jsonify
import requests
import re
import os

app = Flask(__name__)

AWX_URL = "http://100.115.15.106:32668"
AWX_TOKEN = os.environ.get("AWX_TOKEN")
JOB_TEMPLATE_ID = 15

def get_latest_sensor_data():
    try:
        headers = {
            "Authorization": f"Bearer {AWX_TOKEN}",
            "Content-Type": "application/json"
        }
        response = requests.get(
            f"{AWX_URL}/api/v2/job_templates/{JOB_TEMPLATE_ID}/jobs/?order_by=-finished&page_size=1",
            headers=headers,
            timeout=10
        )
        response.raise_for_status()
        jobs = response.json()

        if not jobs["results"]:
            return {"error": "No jobs found"}

        job_id = jobs["results"][0]["id"]

        stdout_response = requests.get(
            f"{AWX_URL}/api/v2/jobs/{job_id}/stdout/?format=txt",
            headers=headers,
            timeout=10
        )
        stdout_response.raise_for_status()
        output = stdout_response.text

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
    return jsonify(get_latest_sensor_data())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
