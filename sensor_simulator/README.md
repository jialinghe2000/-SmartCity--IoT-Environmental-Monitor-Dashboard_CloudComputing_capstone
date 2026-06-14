In a real SmartCity environment, physical sensors deployed across different districts continuously send environmental data to the cloud. In our project, we simulate this process using a Python program running on an EC2 instance.

The simulator generates one set of sensor data every five seconds, following a predefined JSON data structure that contains the sensor ID, district, temperature, CO2 level, NO2 level, and timestamp.
