from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import datetime
from random import randint
from threading import Thread, Event
import eventlet
import time
import adafruit_dht
from board import *
import time
import json




app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app, async_mode='eventlet')
eventlet.monkey_patch()

SENSOR_PIN = D26
dht22 = adafruit_dht.DHT22(SENSOR_PIN, use_pulseio=False)



# button = 20
# led_red = 13
# led_yellow = 19
# led_green = 26

# buttonStatus = GPIO.LOW
# led_red_status = GPIO.LOW
# led_yellow_status = GPIO.LOW
# led_green_status = GPIO.LOW

# GPIO.setup(button, GPIO.IN)
# GPIO.setup(led_red, GPIO.OUT)
# GPIO.setup(led_yellow, GPIO.OUT)
# GPIO.setup(led_green, GPIO.OUT)

# GPIO.output(led_red, GPIO.LOW)
# GPIO.output(led_yellow, GPIO.LOW)
# GPIO.output(led_green, GPIO.LOW)


@app.route("/")
def hello():
    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M")
    templateData = {
        'title': 'HELLO!',
        'time': timeString
    }
    return render_template('index.html', **templateData)


# @app.route('/led/')
# def led():
#     buttonStatus = GPIO.input(button)
#     led_red_status = GPIO.input(led_red)
#     led_yellow_status = GPIO.input(led_yellow)
#     led_green_status = GPIO.input(led_green)

#     templateData = {
#         'title': "Led and Button",
#         'button': buttonStatus,
#         'led_red_status': led_red_status,
#         'led_yellow_status': led_yellow_status,
#         'led_green_status': led_green_status
#     }
#     return render_template('led.html', **templateData)



# @socketio.on('led_event', namespace='/led')
# def led_event(json, methods=['GET', 'POST']):
#     print('received my event: ' + str(json))
#     led_name = json['led']
#     if led_name == 'red':
#         led = 13
#     elif led_name == 'yellow':
#         led = 19
#     elif led_name == 'green':
#         led = 26
#     action = json['action']
#     if action == 'on':
#         GPIO.output(led, GPIO.HIGH)
#     elif action == 'off':
#         GPIO.output(led, GPIO.LOW)



def dht_read():
    while True:
        try:
            temperature = dht22.temperature
            humidity = dht22.humidity
            # print(f"Humidity= {humidity:.2f}")
            # print(f"Temperature= {temperature:.2f}°C")
            cur_date_time = datetime.datetime.now()
            date_time = json.dumps(time.mktime(cur_date_time.timetuple())*1000)
            socketio.emit('newnumber', {'humidity': round(humidity, 2), 'temperature': round(temperature, 2), 'datetime' : date_time},namespace='/dht')
        except:
            print("Reading failed")
        time.sleep(10)

@app.route('/sensor/')
def sensor():
    return render_template('sensor.html')


@socketio.on('connect', namespace='/dht')
def test_connect():
    print('Client DHT connected')
    before_values = []


# def btn_read():
#     while True:
#         button_status = GPIO.input(button)
#         #print('Button: ' + str(button_status))
#         socketio.emit('btn_status', {'btn_status': button_status},namespace='/btn')
#         time.sleep(1)

@socketio.on('connect', namespace='/btn')
def test_connect():
    print('Client BTN connected')


thread_dht = None
# thread_btn = None
if __name__ == "__main__":
    if thread_dht is None:
        thread_dht = Thread(target=dht_read)
        thread_dht.daemon = True
        thread_dht.start()
    # if thread_btn is None:
    #     thread_btn =Thread(target=btn_read)
    #     thread_btn.daemon = True
    #     thread_btn.start()
    socketio.run(app, host='192.168.0.114', port='5050', debug=True)



