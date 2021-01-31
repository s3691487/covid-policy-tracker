import json
import boto3

dynamodb = boto3.resource('dynamodb')


def getNames():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('country-location')
    response = table.scan(AttributesToGet=['country_region'])
    return response['Items']


def lambda_handler(event, context):
    response = getNames()
    seen = []
    for row in response:
        if row["country_region"] not in seen:
            seen.append(row["country_region"])

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
            'Access-Control-Allow-Credentials': 'true',
            'Content-Type': 'application/json'
        },
        'body': json.dumps(seen)
    }
