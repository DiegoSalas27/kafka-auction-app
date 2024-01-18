from flask import Flask, render_template, request, redirect, url_for, jsonify
from wtforms import Form, StringField, FloatField, SubmitField
from wtforms.validators import InputRequired
from consumer import MyKafkaConsumer
from producer import MyKafkaProducer
import time
import threading
import json

app = Flask(__name__)

# List to hold the data for our dashbpard
highest_bidders = []

topic = 'realtime-analytics'
public_ip = '127.0.0.1'
kafka_server_port = '9092'

myConsumer = MyKafkaConsumer(topic,'127.0.0.1', kafka_server_port) 
# myConsumer = MyKafkaConsumer(topic,'54.226.89.103', kafka_server_port) 
myProducer = MyKafkaProducer(topic,'127.0.0.1', kafka_server_port) 
# myProducer = MyKafkaProducer(topic,'54.226.89.103', kafka_server_port) 

class AuctionSubmissionForm(Form):
    email = StringField("Enter your email", validators=[InputRequired("Please enter your email.")])
    quantity = FloatField("Enter quantity", validators=[InputRequired("Please enter quantity.")])
    submit = SubmitField('Submit')
    
def kafka_consumer():
    global highest_bidders
    for message in myConsumer.getConsumer():
        highest_bidders.append(message.value)
        highest_bidders.sort(key=lambda x: x['amount'], reverse=True)
        print('GOOD JOB', highest_bidders)
        if len(highest_bidders) > 5: # Keeping the last 5 data points
            highest_bidders.pop(0)

threading.Thread(target = kafka_consumer).start()

@app.route('/', methods=['GET','POST'])
def index():
    form = AuctionSubmissionForm(request.form)
    if request.method == 'POST' and form.validate():
        myProducer.produce(form.email.data, form.quantity.data)
        # put_user(form.email.data, form.quantity.data) #put the data into DynamoDB
        return redirect(url_for('thankyou'))

    return render_template('index.html', form=form)

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html', highest_bidders=highest_bidders)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) # This will make the Flask app accessible via the EC2's public IP