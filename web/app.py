from flask import Flask, render_template, request, redirect, url_for, jsonify
from wtforms import Form, StringField, FloatField, SubmitField
from wtforms.validators import InputRequired
from flask_socketio import SocketIO
from consumer import MyKafkaConsumer
from producer import MyKafkaProducer
import socket
import time
from threading import Thread
import json
from constants import REALTIME_ANALYTICS, HIGHEST_BIDDERS, TIMER

app = Flask(__name__)
socketio = SocketIO(app)

public_ip = '127.0.0.1'
kafka_server_port = '9092'

highest_bidders = []
timer_thread = None

# Getting server IP address
host_name = socket.gethostname()
server_ip = socket.gethostbyname(host_name)

timerConsumer = MyKafkaConsumer(TIMER, public_ip, kafka_server_port) 
highestBidderConsumer = MyKafkaConsumer(HIGHEST_BIDDERS, public_ip, kafka_server_port)
# myConsumer = MyKafkaConsumer(topic,'54.226.89.103', kafka_server_port) 
myProducer = MyKafkaProducer(REALTIME_ANALYTICS, public_ip, kafka_server_port) 
# myProducer = MyKafkaProducer(topic,'54.226.89.103', kafka_server_port) 

class AuctionSubmissionForm(Form):
    email = StringField("Enter your email", validators=[InputRequired("Please enter your email.")])
    quantity = FloatField("Enter quantity", validators=[InputRequired("Please enter quantity.")])
    submit = SubmitField('Submit')
    
def kafka_highest_bidder_consumer():
    global highest_bidders
    for message in highestBidderConsumer.getConsumer():
        highest_bidders = message.value
        socketio.emit('update_highest_bidders', highest_bidders)

def kafka_timer_consumer():
    for message in timerConsumer.getConsumer():
        socketio.emit('update_timer', message.value)

def refresh_highest_bidders():
    global highest_bidders
    time.sleep(0.5)
    socketio.emit('update_highest_bidders', highest_bidders)

Thread(target = kafka_highest_bidder_consumer).start()
Thread(target = kafka_timer_consumer).start()

# WebSocket event handler for client connections
@socketio.on('connect')
def handle_connect():
    print('Client connected')

@app.route('/', methods=['GET','POST'])
def index():
    form = AuctionSubmissionForm(request.form)
    if request.method == 'POST' and form.validate():
        client_ip = request.remote_addr
        myProducer.produce(form.email.data, form.quantity.data, client_ip)
        return redirect(url_for('thankyou'))

    return render_template('index.html', form=form, server_ip=server_ip)

@app.route('/thankyou')
def thankyou():
    Thread(target = refresh_highest_bidders).start()
    return render_template('thankyou.html')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8080) # This will make the Flask app accessible via the EC2's public IP