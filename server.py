from flask import Flask
from datetime import date
import os


app = Flask(__name__)


@app.route('/')
def index():
    return 'please visit my blog at http://kingname.info'

@app.route("/alarm_clock")
def alarm_clock():
    if os.path.exists('alarmclock.txt'):
        with open('alarmclock.txt') as f:
            date_in_txt = f.read()
            today = str(date.today())
            if date_in_txt == today:
                return 'yes'
    return 'no'


@app.route('/set_alarm')
def set_alarm():
    with open('alarmclock.txt', 'w') as f:
        f.write(str(date.today()))
    return 'OK'


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=745)