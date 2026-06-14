# EC2 Dashboard

This module hosts the SmartCity administrative dashboard on AWS EC2.

EC2-hosted Flask Dashboard.

Functions:
- Read sensor data from DynamoDB
- Provide REST API
- Real-time visualization

## Features

- Flask Web Application
- Real-time Sensor Visualization
- REST API (/api/sensors)
- DynamoDB Integration
- Map-based Monitoring

## Architecture

DynamoDB

      ↓
      
Flask API

      ↓
      
Dashboard

