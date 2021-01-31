import json
import boto3
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)


def lambda_handler(event, context):
    print('event:', json.dumps(event))
    country = event['queryStringParameters']['country_name']
    date = event['queryStringParameters']['date']
    table = dynamodb.Table('covid-cases')

    items = table.get_item(Key={"country_region": country,
                                "date": date})
    if not 'Item' in items:
        items['Item'] = "Data Not Present"
    # print(items['Item'])
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
            'Access-Control-Allow-Credentials': 'true',
            'Content-Type': 'application/json'
        },
        'body': json.dumps(items['Item'], cls=DecimalEncoder)

    }
