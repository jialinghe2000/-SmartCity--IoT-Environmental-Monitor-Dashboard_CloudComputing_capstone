# API Lambda
This folder is reserved for future serverless API integration.
In the current implementation, the Citizen View retrieves data from the Flask Dashboard API:
EC2 Flask API
    /api/sensors

Future enhancement:
S3 Citizen View
        ↓
API Gateway
        ↓
Lambda
        ↓
DynamoDB
