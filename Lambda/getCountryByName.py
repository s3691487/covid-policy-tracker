import json
import boto3
from boto3.dynamodb.conditions import Key


def state_name(country):
    capital = ''
    if country.lower() == ('China').lower():
        capital = 'Beijing'
    if country.lower() == ('Australia').lower():
        capital = 'Australian Capital Territory'
    if country.lower() == ('United Kingdom').lower():
        capital = 'United Kingdom'
    return capital


def lambda_handler(event, context):
    country = event['queryStringParameters']['country_name']
    province_state = state_name(country)
    dynamodb = boto3.resource('dynamodb', region_name="ap-southeast-2")
    table = dynamodb.Table("country-location")
    response = table.get_item(
        Key={
            'country_region': country,
            'province_state': province_state
        }
    )
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
            'Access-Control-Allow-Credentials': 'true',
            'Content-Type': 'application/json'
        },
        'body': json.dumps(response['Item'])
    }

