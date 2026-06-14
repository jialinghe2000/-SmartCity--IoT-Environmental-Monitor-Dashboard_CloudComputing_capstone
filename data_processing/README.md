# Data Processing Module

Workflow

Sensor
    ↓
API Gateway
    ↓
ProcessSensorData Lambda
    ↓
DynamoDB
    ↓
SNS Alert

Background Processing

DynamoDB
    ↓
data_aggregator Lambda
    ↓
SmartCityAggregates


Cloud Features

- Serverless Computing
- Event-driven Architecture
- Managed Storage
- Automatic Scaling
