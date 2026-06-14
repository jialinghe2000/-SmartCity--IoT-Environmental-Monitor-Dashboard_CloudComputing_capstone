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
  
To improve scalability, fault tolerance, and high availability, allowing the platform to handle sudden increases in user traffic more efficiently.

-   End-to-End HTTPS Communication
   
Replace direct HTTP communication with HTTPS endpoints to improve transmission security and eliminate mixed-content issues.

-  Elastic IP or API Gateway for Stable Access
  
Use an Elastic IP or expose backend services through API Gateway to avoid service interruptions caused by EC2 public IP changes.

-  Data Lifecycle Management
  
Archive historical sensor data to Amazon S3 for long-term storage and analytics, reducing the load on DynamoDB.
