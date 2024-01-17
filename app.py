from flask import Flask, jsonify
from consumer import MyKafkaConsumer
from producer import MyKafkaProducer
import time
import threading
import json

app = Flask(__name__)

# List to hold the data for our dashbpard
dashboard_data = []

topic = 'realtime-analytics'
public_ip = '127.0.0.1'
kafka_server_port = '9092'

myConsumer = MyKafkaConsumer('realtime-analytics','127.0.0.1', '9092') 
# myConsumer = MyKafkaConsumer('realtime-analytics','54.226.89.103', '9092') 
myProducer = MyKafkaProducer('realtime-analytics','127.0.0.1', '9092') 
# myProducer = MyKafkaProducer('realtime-analytics','54.226.89.103', '9092') 

def kafka_produce():
    myProducer.produce()

def kafka_consumer():
    global dashboard_data
    for message in myConsumer.getConsumer():
        dashboard_data.append(message.value)
        if len(dashboard_data) > 10: # Keeping the last 10 data points
            dashboard_data.pop(0)

threading.Thread(target = kafka_produce).start()
threading.Thread(target = kafka_consumer).start()


@app.route('/data', methods=['GET'])
def get_data():
    return jsonify(dashboard_data)

@app.route('/')
def index():
    return "Real-time Analytics Dashboard"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) # This will make the Flask app accessiblee via the EC2's public IP