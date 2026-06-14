there are 2 functions in lambda:
1\ SmartCityProcessSensorData
responsibilities:
1.validate sensor data from sensor(/sensor simulator) through API Gateway
2.define pollution status
3.store row data to DynamoDB
4.trigger SNS Alert
5.return API Gateway comstible response

2\Aggregator
responsiblity
1.scan raw data from DynamoDB table
2.Group and calculate sums by district
3.Calculate averages and write to DynamoDB table - Aggregates

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
