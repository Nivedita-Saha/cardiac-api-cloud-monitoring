# Cardiac API Cloud Monitoring

Production-style monitoring and alerting system for a serverless cardiac disease prediction API using AWS services.

## Overview

This project demonstrates how to implement monitoring and observability for a serverless API deployed on AWS Lambda. CloudWatch dashboards and alarms were configured to detect failures and performance issues, with SNS email notifications for real-time alerts.

## Architecture

Test Request → AWS Lambda → CloudWatch Metrics → CloudWatch Alarm → SNS → Email Alert

## Technologies Used

- Python
- AWS Lambda
- Amazon CloudWatch
- Amazon SNS
- Boto3

## Monitoring Features

The following monitoring capabilities were implemented:

- Lambda error monitoring
- Duration performance monitoring
- Invocation tracking
- CloudWatch dashboards
- Automated alarm triggering
- Email notifications via SNS

## Alarm Configuration

### cardiac-api-errors-alarm
Triggers when:
Errors ≥ 1 within 5 minutes

### cardiac-api-duration-alarm
Triggers when:
Duration > 3000 ms

### cardiac-api-throttles-alarm
Triggers when:
Throttles > 0

## Testing Alarm Workflow

The script `test_alarms.py` was created to simulate Lambda failures and verify the monitoring pipeline.

Run:

```bash
python test_alarms.py# cardiac-api-cloud-monitoring
Serverless cardiac disease prediction API with AWS Lambda, CloudWatch monitoring, alarms, and SNS email alerting.
