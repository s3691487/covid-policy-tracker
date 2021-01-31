import json
from datetime import date, datetime, timedelta
import boto3
from decimal import Decimal
from boto3.dynamodb.conditions import Key
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb', region_name="ap-southeast-2")
table = dynamodb.Table("covid-policy")


def handle_decimal_type(obj):
    if isinstance(obj, Decimal):
        if float(obj).is_integer():
            return int(obj)
        else:
            return float(obj)
    raise TypeError


def lambda_handler(event, context):
    country = event['queryStringParameters']['country_name']
    date = event['queryStringParameters']['date']

    response = table.query(
        KeyConditionExpression=Key('country_name').eq(country) & Key('date').eq(date)
    )

    logger.info(len(response['Items']))

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
            'Access-Control-Allow-Credentials': 'true',
            'Content-Type': 'application/json'
        },
        'body': json.dumps(response['Items'], default=handle_decimal_type)
    }
