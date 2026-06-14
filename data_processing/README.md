# AWS Lambda Functions

## ProcessSensorData

Responsibilities:

- Validate incoming sensor data
- Classify pollution levels
- Store records into DynamoDB
- Trigger SNS alerts
- Support serverless processing

## data_aggregator

Responsibilities:

- Scan raw sensor records
- Group by district
- Calculate average values
- Store aggregated data
