# Steps to download kafka and set it up in MAC (installation is almost the same in Windows and Linux)
1. Download apache kafka: https://kafka.apache.org/downloads
2. Unzip the package and place in in your user folder. eg: /Users/diegosalas/kafka_2.13-3.1.0
3. Create a kafka_logs/zookeeper and a kafka_logs/server_logs folder in the same folder where kafka was installed. eg: eg /Users/diegosalas/kafka_logs
4. Update zookeeper.properties:
`dataDir=/Users/diegosalas/kafka_logs/zookeeper`
5. Update server.properties:
- Uncomment line 31: `listeners=PLAINTEXT://:9092`
- Update line 60: `log.dirs=YOUR_PATH_TO_SERVER_LOGS`. eg: `log.dirs=/Users/diegosalas/kafka_logs/server_logs`

# Installing in Linux
1. Install java: sudo apt-get install default-jre
2. Install kafka: wget https://archive.apache.org/dist/kafka/3.1.0/kafka_2.13-3.1.0.tgz
3. Extract: tar -xzf kafka_2.13-3.1.0.tgz

# Starting a kafka cluster
1. Make sure you are in the root of kafka folder. eg: /Users/diegosalas/kafka_2.13-3.1.0
2. Start Zookeeper: ./bin/zookeeper-server-start.sh config/zookeeper.properties
3. Start Kafka Server: ./bin/kafka-server-start.sh config/server.properties

# Create a topic
1. Make sure you are in the root of kafka folder. eg: /Users/diegosalas/kafka_2.13-3.1.0
2. Enter the following command: ./bin/kafka-topics.sh --create --topic realtime-analytics --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1

# Installing kafka server EC2
1. download source code: wget https://medium-4-eb.s3.amazonaws.com/kafka-server.zip
2. Install unzip: sudo apt install unzip
3. unzip kafka-server.zip
4. cd kafka-server/
5. Install pip3: sudo apt install python3-pip
6. Install dependencies: pip3 install -r requirements.txt

# Configure websockets in nginx
1. Access the deployed application folder by sshing into your EC2 instance: /var/app/current 
2. Create the following directory: mkdir .ebextensions
3. Cd into the .ebextensions folder: cd .ebextensions/
4. Enter the following configuration: `container_commands:
  enable_websockets:
    command: |
      sed -i '/\s*proxy_set_header\s*Connection/c \
              proxy_set_header Upgrade $http_upgrade;\
              proxy_set_header Connection "upgrade";\
              '
/tmp/deployment/config/#etc#nginx#conf.d#00_elastic_beanstalk_proxy.conf`

# Setup python application (Beanstalk)
1. run the following command: `pip3 install -r requirements.txt`
the previous command will install kafka-python (a kafka client for python) and flask (a minimalistic web framework to create rest APIs and web applications).

# Run the python application
python3 app.py

