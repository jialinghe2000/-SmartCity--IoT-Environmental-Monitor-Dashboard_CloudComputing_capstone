import json
import boto3
from datetime import datetime, timezone

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    source_table = dynamodb.Table('SmartCitySensorData')
    dest_table = dynamodb.Table('SmartCityAggregates')

    try:
        # 1. Scan raw data from Member 2's table
        response = source_table.scan()
        items = response.get('Items', [])

        if not items:
            return {"statusCode": 200, "body": "No data found to aggregate."}

        # 2. Group and calculate sums by district
        districts_data = {}
        for item in items:
            d = item.get('district', 'Unknown')
            if d not in districts_data:
                districts_data[d] = {'temp_sum': 0, 'co2_sum': 0, 'no2_sum': 0, 'count': 0}
            
            districts_data[d]['temp_sum'] += int(item.get('temperature', 0))
            districts_data[d]['co2_sum'] += int(item.get('co2', 0))
            districts_data[d]['no2_sum'] += int(item.get('no2', 0))
            districts_data[d]['count'] += 1

        # 3. Generate current hour timestamp
        current_hour = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:00:00Z')

        # 4. Calculate averages and write to Aggregates table
        for district, stats in districts_data.items():
            avg_temp = int(stats['temp_sum'] / stats['count'])
            avg_co2 = int(stats['co2_sum'] / stats['count'])
            avg_no2 = int(stats['no2_sum'] / stats['count'])

            agg_record = {
                'district': district,
                'aggregate_hour': current_hour,
                'avg_temperature': avg_temp,
                'avg_co2': avg_co2,
                'avg_no2': avg_no2,
                'total_records_processed': stats['count']
            }
            
            dest_table.put_item(Item=agg_record)
            print(f"Aggregation complete for {district}: {agg_record}")

        return {
            "statusCode": 200,
            "body": json.dumps("Hourly aggregation completed successfully!")
        }

    except Exception as e:
        print("Aggregation Error:", str(e))
        return {
            "statusCode": 500,
            "body": json.dumps(f"Error: {str(e)}")
        }
