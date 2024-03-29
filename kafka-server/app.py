from flask import Flask
from flask_cors import CORS
from consumer import MyKafkaConsumer
from producer import MyKafkaProducer
from constants import HIGHEST_BIDDERS, BID, TIMER
import time
import threading
import boto3

app = Flask(__name__)

CORS(app)

dynamodb = boto3.resource('dynamodb',region_name='us-east-1')
kafka_server_port = '9092'
highest_bidders = []

highestBidderConsumer = MyKafkaConsumer(BID,'127.0.0.1', kafka_server_port) 

highestBidderProducer= MyKafkaProducer(HIGHEST_BIDDERS,'127.0.0.1', kafka_server_port)
timerProducer = MyKafkaProducer(TIMER,'127.0.0.1', kafka_server_port) 
    
def kafka_highest_bidder_consumer():
    global highest_bidders
    for message in highestBidderConsumer.getConsumer():
        highest_bidders.append(message.value)
        put_user(message.value)
        highest_bidders.sort(key=lambda x: (len (x['amount']), x['amount']), reverse=True)
        if len(highest_bidders) > 5: # Keeping the last 5 data points
            highest_bidders.pop()
        highestBidderProducer.produce(highest_bidders)

def syncTime(duration):
    timer = duration
    while timer > 0:
        timerProducer.produce(timer)
        timer -= 1
        time.sleep(1)

def put_user(user):
    table = dynamodb.Table('users')

    print('user', user)

    response = table.put_item(
       Item={
            'email': user['email'],
            'amount': user['amount'],
            'client_ip': user['client_ip']
        }
    )

threading.Thread(target = kafka_highest_bidder_consumer).start()
threading.Thread(target = syncTime, args=(60,)).start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) # This will make the Flask app accessible via the EC2's public IP