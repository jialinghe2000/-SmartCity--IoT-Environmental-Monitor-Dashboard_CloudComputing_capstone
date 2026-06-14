# SNS Notification

Purpose

Provide real-time environmental alerts.

Trigger Condition

Status == DANGEROUS

Workflow

Lambda
    ↓
SNS Topic
    ↓
Email Notification
