# SmartCity IoT Environmental Monitoring System
Group5_CloudComputing_capstone
Business Context: The "Green City" initiative needs to monitor urban air quality (CO2, NO2, Temperature). They have thousands of simulated sensors across the city. They need a centralized "Command Center" where city officials can see live heatmaps and receive alerts if pollution levels in a specific district become dangerous.

Core Technical Objectives:
- Ingest real-time IoT data streams.
- Process and aggregate data (e.g., calculating hourly averages).
- Host a public-facing visualization dashboard on EC2.

Architectural Components:
- Sensors: A Python script running on a local machine (or another EC2) simulating HTTP traffic to API Gateway.
- Processing: AWS Lambda processes the raw sensor data and stores it in Amazon DynamoDB.
- EC2 Dashboard: An EC2 instance running a web server (e.g., Flask/Django) that hosts an interactive map (Leaflet.js) showing the sensor locations and live readings.
- Alerting: Amazon SNS to send "Dangerous Level" alerts to city officials' emails.

Advanced Challenge: Use S3 Static Website Hosting for a secondary "Citizen's View" page that fetches data from the same DynamoDB via an API, demonstrating a multi-channel visualization strategy.


Architecture

Sensor Simulator
      ↓
API Gateway
      ↓
Lambda
      ↓
DynamoDB
      ↓
Dashboard
      ↓
S3 Citizen Portal

Features
- Serverless Processing
- Event-driven Architecture
- Real-time Dashboard
- Public Citizen View
- SNS Alert
- Data Aggregation

AWS Services
- VPC
- EC2
- API Gateway
- Lambda
- DynamoDB
- SNS
- CloudWatch
- S3

Future Enhance
-  ALB+ASG for Dashboard
-  
To improve scalability, fault tolerance, and high availability, allowing the platform to handle sudden increases in user traffic more efficiently.

-   End-to-End HTTPS Communication
-   
Replace direct HTTP communication with HTTPS endpoints to improve transmission security and eliminate mixed-content issues.

-  Elastic IP or API Gateway for Stable Access
-  
Use an Elastic IP or expose backend services through API Gateway to avoid service interruptions caused by EC2 public IP changes.

-  Data Lifecycle Management
-  
Archive historical sensor data to Amazon S3 for long-term storage and analytics, reducing the load on DynamoDB.
