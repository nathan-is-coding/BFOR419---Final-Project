#!/usr/bin/env python3

from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
import threading
import subprocess
import time

clients = 0

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)

def send_update():
    global clients
    if clients > 0:
        #('Update', broadcast=True)
        with app.app_context():
            emit('Update', broadcast=True, namespace="/")
            print("Update sent")

def readStatistics():
    global cpuUsage, ramUsage, ramTotal, storageUsage, storageAvailable, storageTotal, sshStatus, sshRuntime, apacheStatus, apacheRuntime
    with open('stats.txt', "r") as file:
        cpuUsage = file.readline()
        ramUsage = file.readline()
        ramTotal = file.readline()
        storageUsage = file.readline()
        storageAvailable = file.readline()
        storageTotal = file.readline()
        sshStatus = file.readline()
        sshRuntime = file.readline()
        apacheStatus = file.readline()
        apacheRuntime = file.readline()

def GetStatistics():
    while True:
        subprocess.run(["./ServerStats.bash"])
        print("Stats retrieved")
        send_update()
        time.sleep(10)

@app.route("/")
def home():
    readStatistics()
    return render_template(
        'home.html',
        cpuUsage=cpuUsage,
        ramUsage=ramUsage,
        ramTotal=ramTotal,
        storageUsage=storageUsage,
        storageAvailable=storageAvailable,
        storageTotal=storageTotal,
        sshStatus=sshStatus,
        sshRuntime=sshRuntime,
        apacheStatus=apacheStatus,
        apacheRuntime=apacheRuntime
        )

@socketio.on('connect')
def client_connection(auth=None):
    global clients
    clients += 1
    print("Clients: ", clients)

@socketio.on('disconnect')
def client_disconnection():
    global clients
    clients -= 1
    print("Clients: ", clients)

thread = threading.Thread(target=GetStatistics)
thread.start()

print("Exited thread")
socketio.run(app, '127.0.0.1', 8080)