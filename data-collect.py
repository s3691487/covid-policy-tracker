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
        "project_id": "<project_id>",
        "private_key_id": "<private_key_id>",
        "private_key": "-----BEGIN PRIVATE KEY-----\n<private_key>\n-----END PRIVATE KEY-----\n",
        "client_email": "<client_email>",
        "client_id": "<client_id>",
        "auth_uri": "<auth_uri>",
        "token_uri": "<token_uri>",
        "auth_provider_x509_cert_url": "<auth_provider_x509_cert_url>",
        "client_x509_cert_url": "<client_x509_cert_url>"
    },)

yesterday = (datetime.now() - timedelta(1)).strftime("%Y-%m-%d")

def define_data_type(dataframe):
    dataframe['date'] = dataframe['date'].dt.strftime("%Y-%m-%d")
    dataframe['confirmed_cases'] = dataframe['confirmed_cases'].fillna(0.0).astype(int)
    dataframe['international_travel_controls'] = dataframe['international_travel_controls'].fillna(0.0).astype(int)
    return dataframe

def define_country_data_type(df):
    df['date'] = df['date'].dt.strftime("%Y-%m-%d")
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
        SELECT country_region, date, sum(confirmed) as confirmed, sum(deaths) as deaths, sum(active) as active 
        FROM `bigquery-public-data.covid19_jhu_csse.summary` 
        where (country_region like 'Australia' or country_region like 'China' or country_region like 'United Kingdom') and 
        date between '2020-01-01' and '%s' group by country_region, date order by date asc
    """%yesterday
    df = pd.read_gbq(query, dialect='standard', project_id=project_id, credentials=credentials)
    define_country_data_type(df)
    return df

def query_yesterday_country_data():
    query = """
        SELECT country_region, date, sum(confirmed) as confirmed, sum(deaths) as deaths, sum(active) as active 
        FROM `bigquery-public-data.covid19_jhu_csse.summary` 
        where (country_region like 'Austral:qia' or country_region like 'China' or country_region like 'United Kingdom') and 
        date = '%s' group by country_region, date
    """%yesterday
    df = pd.read_gbq(query, dialect='standard', project_id=project_id, credentials=credentials)
    define_country_data_type(df)
    return df

def query_geo_data():
    query = """
        SELECT max(province_state) as province_state, country_region, latitude, longitude FROM `bigquery-public-data.covid19_jhu_csse_eu.summary` 
        where (country_region like 'Australia' or country_region like 'China' or country_region like 'United Kingdom') and province_state is not null 
        group by country_region, latitude, longitude order by country_region asc
    """
    df = pd.read_gbq(query, dialect='standard', project_id=project_id, credentials=credentials)
    df['latitude'] = df['latitude'].astype(str)
    df['longitude'] = df['longitude'].astype(str)
    return df


def load_daily_data_to_table(dataframe, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', aws_access_key_id='<aws_access_key_id>', aws_secret_access_key='<aws_secret_access_key>',region_name='ap-southeast-2')

    table_policy = dynamodb.Table('covid-policy')
    policy_data = dataframe.T.to_dict().values()
    for policy in policy_data:
        table_policy.put_item(Item=policy)

    table_country = dynamodb.Table('covid_cases')
    country_data = query_yesterday_country_data().T.to_dict().values()
    for country in country_data:
        table_country.put_item(Item=country)


def load_historical_country_data(dynamodb=None):

    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', aws_access_key_id='<aws_access_key_id>', aws_secret_access_key='<aws_secret_access_key>' ,region_name='ap-southeast-2')
    table = dynamodb.Table('covid-cases')
    covid_cases_data = query_country_data().T.to_dict().values()
    for country in covid_cases_data:
        table.put_item(Item=country)

    table = dynamodb.Table('country-location')
    location_data = query_geo_data().T.to_dict().values()
    for location in location_data:
        table.put_item(Item=location)


def load_historical_data_to_db():
    df = query_historical_policy()
    load_daily_data_to_table(df)
    load_historical_country_data()


def load_daily_data_to_db():
    df = query_policy_for_current_date()
    load_daily_data_to_table(df)


if __name__ == '__main__':
    # load_historical_data_to_db()
    load_daily_data_to_db()