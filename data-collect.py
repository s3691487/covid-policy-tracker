# This is a sample Python script.

# prerequisites for this script:
# python version 3.8
# pip install --upgrade pandas-gbq

import pandas as pd
from datetime import date, datetime, timedelta
from google.oauth2 import service_account
import boto3

project_id = "s3691487-cc2021"
credentials = service_account.Credentials.from_service_account_info(
    {
        "type": "service_account",
        "project_id": "YOUR_PROJECT_ID",
        "private_key_id": "YOUR_PriVATe_KEY_ID",
        "private_key": "YOUR_PRIVATE_KEY",
        "client_email": "YOUR_CLIENT_EMAIL",
        "client_id": "YOUR_CLIENT_ID",
        "auth_uri": "YOUR AUTH",
        "token_uri": "YOUR TOKEN",
        "auth_provider_x509_cert_url": "YOUR CERTS URL",
        "client_x509_cert_url": "LIENT CERT URL"
    },)

yesterday = (datetime.now() - timedelta(1)).strftime("%Y-%m-%d")

def define_data_type(dataframe):
    dataframe['date'] = dataframe['date'].dt.strftime("%Y-%m-%d")
    dataframe['confirmed_cases'] = dataframe['confirmed_cases'].fillna(0.0).astype(int)
    dataframe['international_travel_controls'] = dataframe['international_travel_controls'].fillna(0.0).astype(int)
    return dataframe

def define_country_data_type(df):
    df['date'] = df['date'].dt.strftime("%Y-%m-%d")
    df['latitude'] = df['latitude'].astype(str)
    df['longitude'] = df['longitude'].astype(str)
    df['confirmed'] = df['confirmed'].fillna(0.0).astype(int)
    df['deaths'] = df['deaths'].fillna(0.0).astype(int)
    df['active'] = df['active'].fillna(0.0).astype(int)

def query_historical_policy():

    query = """
        SELECT country_name, region_name, date, school_closing_notes, workplace_closing, workplace_closing_notes, cancel_public_events, cancel_public_events_notes, 
        restrictions_on_gatherings, restrictions_on_gatherings_notes, close_public_transit, close_public_transit_notes, stay_at_home_requirements, stay_at_home_requirements_notes, 
        contact_tracing, contact_tracing_notes, confirmed_cases, deaths international_travel_controls, international_travel_controls_notes FROM `bigquery-public-data.covid19_govt_response.oxford_policy_tracker` 
        where country_name like 'United Kingdom' or country_name like 'China' or country_name like 'Australia' and date BETWEEN '2020-01-01' and '%s' order by date asc
    """%yesterday
    df = pd.read_gbq(query, dialect='standard', project_id=project_id, credentials=credentials)
    df = define_data_type(df)
    return df


def query_policy_for_current_date():
    today = date.today().strftime("%Y-%m-%d")
    query = """
        SELECT country_name, region_name, date, school_closing_notes, workplace_closing, workplace_closing_notes, cancel_public_events, cancel_public_events_notes, 
        restrictions_on_gatherings, restrictions_on_gatherings_notes, close_public_transit, close_public_transit_notes, stay_at_home_requirements, stay_at_home_requirements_notes, 
        contact_tracing, contact_tracing_notes, confirmed_cases, deaths international_travel_controls, international_travel_controls_notes FROM `bigquery-public-data.covid19_govt_response.oxford_policy_tracker` 
        where ( country_name like 'United Kingdom' or country_name like 'China' or country_name like 'Australia') and date = '%s' order by date asc
    """%today
    df = pd.read_gbq(query, dialect='standard', project_id=project_id, credentials=credentials)
    df = define_data_type(df)
    return df

def query_country_data():
    query = """
        SELECT province_state, country_region, date, latitude, longitude, location_geom, confirmed, deaths, active FROM 
        `bigquery-public-data.covid19_jhu_csse.summary` where (country_region like 'Australia' 
        or country_region like 'China' or country_region like 'United Kingdom') order by date asc
    """
    df = pd.read_gbq(query, dialect='standard', project_id=project_id, credentials=credentials)
    return df

def query_yesterday_country_data():
    query = """
        SELECT province_state, country_region, date, latitude, longitude, location_geom, confirmed, deaths, active FROM 
        `bigquery-public-data.covid19_jhu_csse.summary` where (country_region like 'Australia' 
        or country_region like 'China' or country_region like 'United Kingdom') order by date asc
    """
    df = pd.read_gbq(query, dialect='standard', project_id=project_id, credentials=credentials)
    return df

def load_data_to_table(dataframe, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', aws_access_key_id='AKIA3XOJ3BFU4PZWW3NA', aws_secret_access_key='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',region_name='ap-southeast-2')

    table_policy = dynamodb.Table('covid-policy')
    policy_data = dataframe.T.to_dict().values()
    for policy in policy_data:
        table_policy.put_item(Item=policy)

    table_country = dynamodb.Table('country')
    country_data = query_yesterday_country_data().T.to_dict().values()
    for country in country_data:
        table_country.put_item(Item=country)


def load_historical_country_data(dynamodb=None):
    dataframe = query_country_data()
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', aws_access_key_id='AKIA3XOJ3BFU4PZWW3NA', aws_secret_access_key='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',region_name='ap-southeast-2')
    define_country_data_type(dataframe)
    print(dataframe.dtypes)
    table = dynamodb.Table('country')
    data = dataframe.T.to_dict().values()
    for country in data:
        table.put_item(Item=country)


def load_historical_data_to_db():
    df = query_historical_policy()
    load_data_to_table(df)

def load_today_data_to_db():
    df = query_policy_for_current_date()
    load_data_to_table(df)


if __name__ == '__main__':
    # load_historical_data_to_db()
    load_historical_country_data()
    # load_today_data_to_db()