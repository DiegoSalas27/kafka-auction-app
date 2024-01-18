# Steps to download kafka and set it up in MAC (installation is almost the same in Windows and Linux)s
1. Download apache kafka: https://kafka.apache.org/downloads
2. Unzip the package and place in in your user folder. eg: /Users/diegosalas/kafka_2.13-3.1.0
3. Create a kafka_logs/zookeeper and a kafka_logs/server_logs folder in the same folder where kafka was installed. eg: eg /Users/diegosalas/kafka_logs
4. Update zookeeper.properties:
`dataDir=/Users/diegosalas/kafka_logs/zookeeper`
5. Update server.properties:
- Uncomment line 31: `listeners=PLAINTEXT://:9092`
- Update line 60: `log.dirs=YOUR_PATH_TO_SERVER_LOGS`. eg: `log.dirs=/Users/diegosalas/kafka_logs/server_logs`

# Starting a kafka cluster
1. Make sure you are in the root of kafka folder. eg: /Users/diegosalas/kafka_2.13-3.1.0
2. Start Zookeeper: ./bin/zookeeper-server-start.sh config/zookeeper.properties
3. Start Kafka Server: ./bin/kafka-server-start.sh config/server.properties

# Create a topic
1. Make sure you are in the root of kafka folder. eg: /Users/diegosalas/kafka_2.13-3.1.0
2. Enter the following command: ./bin/kafka-topics.sh --create --topic realtime-analytics --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1

# Setup python application
1. run the following command: `pip3 install -r requirements.txt`
the previous command will install kafka-python (a kafka client for python) and flask (a minimalistic web framework to create rest APIs and web applications).

# Run the python application
python3 app.py

