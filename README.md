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


# System Design

Architecture

Sensor Simulator
      ↓
API Gateway
      ↓
Lambda
      ↓ 
DynamoDB & SNS
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
  
To improve scalability, fault tolerance, and high availability, allowing the platform to handle sudden increases in user traffic more efficiently.

-   End-to-End HTTPS Communication
   
Replace direct HTTP communication with HTTPS endpoints to improve transmission security and eliminate mixed-content issues.

-  Elastic IP or API Gateway for Stable Access
  
Use an Elastic IP or expose backend services through API Gateway to avoid service interruptions caused by EC2 public IP changes.

-  Data Lifecycle Management
  
Archive historical sensor data to Amazon S3 for long-term storage and analytics, reducing the load on DynamoDB.


# Technical Deep Dive: Security, Storage, and Scalability

## Security Design

Security is implemented at multiple layers of the SmartCity system, including network security, identity security, application security, and operational monitoring.

### 1. Network Security: VPC and Security Groups

The system is deployed inside a custom AWS Virtual Private Cloud (VPC), providing network isolation and secure communication between resources.

The VPC consists of:

- Two Public Subnets
- Two Private Subnets
- Internet Gateway (IGW)
- Security Groups

Public subnets host Internet-facing resources such as:

- EC2 Sensor Simulator
- EC2 Flask Dashboard

Private subnets are reserved for future backend services and internal resources that should not be directly exposed to the Internet.

Security Groups function as virtual firewalls.

For the Dashboard EC2 instance:

| Port | Purpose |
|--------|----------|
| HTTP (80) | Public dashboard access |
| SSH (22) | Administrator management and deployment |

Only necessary ports are opened, minimizing the attack surface and improving network security.

### 2. Identity Security: IAM Roles

AWS Identity and Access Management (IAM) Roles are used to securely grant permissions between AWS services.

Instead of storing AWS credentials in application code, services obtain temporary credentials through IAM Roles.

Examples:

- Lambda → DynamoDB access
- Lambda → SNS publish permission
- EC2 Dashboard → DynamoDB read permission

This follows the Principle of Least Privilege, ensuring that each service only receives the permissions required to perform its tasks.

### 3. Application Security: API Gateway and Validation

API Gateway acts as the controlled entry point of the platform.

Sensor devices submit data through:

```http
POST /sensor
```

This prevents direct access to backend services such as DynamoDB.

The ProcessSensorData Lambda function validates incoming JSON payloads before processing.

Validated fields include:

- sensor_id
- district
- temperature
- co2
- no2
- timestamp

This helps prevent invalid or malformed data from being stored.

### 4. Data Access Security

DynamoDB is never directly exposed to public users.

Database access is restricted to authorized AWS services through IAM permissions.

Users access information through:

- Dashboard API
- S3 Citizen Portal
- API Gateway

This creates a secure separation between public interfaces and backend storage.

### 5. Monitoring and Operational Security

Amazon CloudWatch is used to monitor system activity.

CloudWatch provides:

- Lambda execution logs
- Error detection
- Troubleshooting support
- Processing pipeline verification

Amazon SNS enhances operational security by sending immediate email alerts when dangerous pollution conditions are detected.

---

## Storage Design

The system uses Amazon DynamoDB as its primary storage solution.

DynamoDB was selected because IoT environments generate large amounts of high-frequency, time-series sensor data.

Advantages include:

- Flexible schema
- Low latency
- Fully managed service
- High write scalability
- Serverless operation

### 1. SmartCitySensorData Table

This table stores raw sensor readings.

#### Purpose

Store individual processed sensor records received from Lambda.

#### Key Design

| Key Type | Attribute |
|-----------|------------|
| Partition Key | sensor_id |
| Sort Key | timestamp |

#### Attributes

- sensor_id
- timestamp
- district
- temperature
- co2
- no2
- status

#### Example Record

```json
{
  "sensor_id": "S001",
  "timestamp": "2026-06-15T12:00:00Z",
  "district": "Downtown",
  "temperature": 36,
  "co2": 850,
  "no2": 70,
  "status": "WARNING"
}
```

This structure supports time-series storage because multiple readings from the same sensor can be ordered by timestamp.

### 2. SmartCityAggregates Table

This table stores aggregated environmental statistics.

#### Purpose

Store district-level summary information generated by the Aggregator Lambda function.

#### Key Design

| Key Type | Attribute |
|-----------|------------|
| Partition Key | district |
| Sort Key | aggregate_hour |

#### Attributes

- district
- aggregate_hour
- avg_temperature
- avg_co2
- avg_no2
- total_records_processed

#### Example Record

```json
{
  "district": "Downtown",
  "aggregate_hour": "2026-06-15T12:00:00Z",
  "avg_temperature": 34,
  "avg_co2": 790,
  "avg_no2": 58,
  "total_records_processed": 125
}
```

### 3. Two-Table Storage Strategy

The system separates operational data from analytical data.

#### SmartCitySensorData

Stores:

- Raw sensor readings
- Real-time operational records

#### SmartCityAggregates

Stores:

- District-level summaries
- Analytics-ready data

Benefits:

- Faster dashboard queries
- Better scalability
- Reduced read overhead
- Improved data organization

---

## Scalability Design

Scalability refers to the ability of a system to handle increasing workloads without significant performance degradation.

The SmartCity architecture achieves scalability through managed services, serverless computing, event-driven processing, and future infrastructure enhancements.

### 1. API Gateway Scalability

API Gateway serves as the ingestion layer for sensor data.

In real-world deployments, thousands of sensors may transmit data simultaneously.

API Gateway can automatically handle concurrent requests without requiring manual server management.

Benefits:

- Managed service
- Automatic scaling
- High availability
- Reduced operational overhead

### 2. Lambda Scalability

AWS Lambda provides serverless event-driven processing.

Every sensor event automatically triggers a Lambda execution.

When workload increases:

- Lambda automatically launches additional execution environments
- Multiple requests are processed in parallel

Benefits:

- No server provisioning
- Event-driven architecture
- Automatic scaling
- Pay-as-you-go pricing

### 3. DynamoDB Scalability

DynamoDB is designed for high-frequency data ingestion.

IoT platforms continuously generate sensor records.

DynamoDB provides:

- High write throughput
- Low-latency reads
- Automatic scaling
- Managed database infrastructure

This makes it suitable for large-scale SmartCity deployments.

### 4. Aggregation-Based Scalability

The Aggregator Lambda improves analytical scalability.

Instead of querying all raw sensor records, dashboards can retrieve summarized information from the SmartCityAggregates table.

Benefits:

- Reduced database reads
- Faster dashboard response
- Better performance under heavy workloads

### 5. Future Dashboard Scaling

The current dashboard uses:

```text
User
    ↓
EC2 Flask Dashboard
```

For future production deployment, the architecture can be enhanced using:

- Application Load Balancer (ALB)
- Auto Scaling Group (ASG)

Future architecture:

```text
Users
    ↓
Application Load Balancer
    ↓
Auto Scaling Group
    ↓
Multiple EC2 Dashboard Instances
```

#### Application Load Balancer (ALB)

Responsibilities:

- Distribute incoming traffic
- Improve availability
- Prevent overload on a single instance

#### Auto Scaling Group (ASG)

Responsibilities:

- Automatically launch EC2 instances
- Automatically terminate unused instances
- Adjust capacity according to demand

Benefits:

- High availability
- Fault tolerance
- Elastic scaling
- Improved user experience

---

## Cloud Computing Characteristics

The SmartCity platform demonstrates several key cloud computing characteristics.

### Resource Pooling

Cloud resources are shared and managed by AWS.

Examples:

- VPC
- EC2
- Lambda
- DynamoDB

Users consume resources without managing physical hardware.

### On-Demand Self-Service

Resources can be provisioned whenever needed.

Examples:

- Launching EC2 instances
- Creating Lambda functions
- Creating DynamoDB tables
- Deploying API Gateway endpoints

### Rapid Elasticity

Resources can scale automatically according to workload.

Examples:

- Lambda automatic scaling
- API Gateway request scaling
- DynamoDB throughput scaling
- Future ASG dashboard scaling

### Measured Service

AWS follows a pay-as-you-go model.

Organizations only pay for the resources consumed.

Examples:

- Lambda invocation-based pricing
- DynamoDB usage-based pricing
- EC2 hourly billing

### Broad Network Access

System resources can be accessed through standard network protocols.

Examples:

- Sensor devices sending HTTP requests
- Dashboard access through web browsers
- S3 Citizen Portal access
- SNS email notifications

---

## Summary

The SmartCity platform combines:

- Secure networking through VPC and Security Groups
- Identity security through IAM Roles
- Serverless event-driven processing with Lambda
- Scalable NoSQL storage with DynamoDB
- Real-time alerting through SNS
- Real-time visualization through EC2 Dashboard and S3 Citizen Portal

The architecture demonstrates key cloud computing principles while providing a scalable, secure, and extensible IoT monitoring solution.
