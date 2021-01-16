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
        "project_id": "s3691487-cc2021",
        "private_key_id": "1180e315a577da24e35e3cb3f17ee96b725d92bf",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDK5igimpKmuM+I\nOUK8E7n1XnTZZ5Cw6RJhteT9Xz4ppzRCUmReheWA7Q03RrKKF26tk5fgbapXfQSI\nWD1CPldqwLoTbqLFHhkdaxPiE+lFAaEUITuYtgPpYiS7esLTaZ1zI9UHJXkTotWa\nqd4h/6gEduQlG5ohuRXx+/xiTJlzVjqjBbxOnIgsFF/Gh9vH4QtxM8XcWpKq+Kbq\nmsnYmt88v+Y5bk8oG3OptyCOVZy7c2/kvzGOWX8DMwKVWuZcx+rTSZnVw1Eok5z2\nfTOgoFh5GWFibnRZ5RVoq3sYXOID7To2mDhZ2mq/MglQwU6nFVUpLPpThMzd41+l\nd+bTePF5AgMBAAECggEABOeyNGUnVfOVhGeaX8JPUzZhhBVfN8B1GUEeap5E+hjo\nqCpmcqvxS8ZcGy6KZ7dTNBi9FqfrP6dOHUvnmtFRTjHS3cZ/L11zDuIoWyV1lN1w\nkWeQEZ9KC9HIU9lbwLFZ/qJXYE9m2uA4VaXOvbFfR7cmSU8rRC6KcGzrboBUQyfZ\nVcClwRy/VTEyKje6gLUvKFL32FIgkFHSxBH++VnqQrJJ7mkbX40zSxoKBK/ey3Kt\nBY4hmqvvNaErAYKSM2Lsma/vvc9PZz4IldIFkNiy9UGaVcihB86Lbqd8paZDcDrV\n88cKPQqUtSpyd9mHxsfSe9WsCOew2+piDwt0SH08DQKBgQDkZejs62L2BHGngS1z\n0Gse7BmlKwxr1glTYzMp4Y6xZNpjb0E6kvkLLWhA/ALOxBoRknILKP0Z4BjdD9PH\nwcQQ7zi6Bt6RHweO73XJdkGg7WhKv5iMw83baS1z/HDZy9L8Om9dg49V9ZagEUh1\nCiXrc1x4UTUl5RNP9J9FF2Sr5QKBgQDja14m8kvIJgwocikUk8JwF/NH2njuv2oY\n8u9Fx4MqPw7EF7RNNxMZZlHgH/NYhLybpPME1dCO7XorCPgaWtCqIkjbdEVZUfg2\nWWbMQhA4cALhwMILSi8qnaDEcXPyjWOLxpjPtQuD/u2HZjxHAmI6zWNdfMsGU91W\n2rvdrp3eBQKBgHat1bi2HzgC2yPU5c9WLzNkL3c5xTyLfVENLNrIT6Mx6qDcgKJ1\nGF+Meq25xaO3FmynEgdmhw3Y+lJ0FPGpZ7388BcJ1sDFxOGq4CONBVEfy597q0MJ\nw4ANSQcJ14H0fW9+1btbzzE1ac1G7cWTPlz4FsaWO+2y+LQFQnVeUHtZAoGBAI9k\nIUdZOqMGKmBOKszIpa5by48gl2Oh2VnFw0wyEefPPpYxhAOzmB1JwJIaUysa9nkE\nth30Wr3jykXcL+MeI7dCSsHkO92nq2NJV2Guvd938Lk6+p53teme3cE+76ads4hs\nPemo84vUbxwSQCtdu2XsHpzRlIl203ZyEEYkVXGpAoGAIwbR6Fc0hZ61wvygLpdy\n29BFuxDuzOreXGCGev0iqFHsX4Tmwt+ogsKAgKNcx2u+fKb7zOjzqMOAU810OLpr\nZ3K+lLmNqZYnTdNID26aptMX7w7oSBvIsEukr7+YU5MHr8RQb0kmaNTLFESggjj5\nfx9v2YPLX7zYx2ARZjioSXA=\n-----END PRIVATE KEY-----\n",
        "client_email": "data-collector@s3691487-cc2021.iam.gserviceaccount.com",
        "client_id": "107646228197472050558",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/data-collector%40s3691487-cc2021.iam.gserviceaccount.com"
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
        where (country_region like 'Australia' or country_region like 'China' or country_region like 'United Kingdom') and 
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

    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', aws_access_key_id='AKIA3XOJ3BFU4PZWW3NA', aws_secret_access_key='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',region_name='ap-southeast-2')
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