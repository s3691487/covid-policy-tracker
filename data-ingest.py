# This is a sample Python script.

# prerequisites for this script:
# python version 3.8
# pip install --upgrade pandas-gbq

import pandas as pd
from datetime import date

def query_policy_for_Australia():

    query = """
        SELECT country_name, region_name, date, school_closing_notes, workplace_closing, workplace_closing_notes, cancel_public_events, cancel_public_events_notes, 
        restrictions_on_gatherings, restrictions_on_gatherings_notes, close_public_transit, close_public_transit_notes, stay_at_home_requirements, stay_at_home_requirements_notes, 
        contact_tracing, contact_tracing_notes, confirmed_cases, deaths international_travel_controls, international_travel_controls_notes FROM `bigquery-public-data.covid19_govt_response.oxford_policy_tracker` 
        where country_name like 'Australia' and date BETWEEN '2020-01-01' and '2020-12-31' order by date asc
    """
    df = pd.read_gbq(query, dialect='standard')
    return df

def query_policy_for_China():

    query = """
        SELECT country_name, region_name, date, school_closing_notes, workplace_closing, workplace_closing_notes, cancel_public_events, cancel_public_events_notes, 
        restrictions_on_gatherings, restrictions_on_gatherings_notes, close_public_transit, close_public_transit_notes, stay_at_home_requirements, stay_at_home_requirements_notes, 
        contact_tracing, contact_tracing_notes, confirmed_cases, deaths international_travel_controls, international_travel_controls_notes FROM `bigquery-public-data.covid19_govt_response.oxford_policy_tracker` 
        where country_name like 'China' and date BETWEEN '2020-01-01' and '2020-12-31' order by date asc
    """
    df = pd.read_gbq(query, dialect='standard')
    return df

def query_policy_for_UK():

    query = """
        SELECT country_name, region_name, date, school_closing_notes, workplace_closing, workplace_closing_notes, cancel_public_events, cancel_public_events_notes, 
        restrictions_on_gatherings, restrictions_on_gatherings_notes, close_public_transit, close_public_transit_notes, stay_at_home_requirements, stay_at_home_requirements_notes, 
        contact_tracing, contact_tracing_notes, confirmed_cases, deaths international_travel_controls, international_travel_controls_notes FROM `bigquery-public-data.covid19_govt_response.oxford_policy_tracker` 
        where country_name like 'United Kingdom' and date BETWEEN '2020-01-01' and '2020-12-31' order by date asc
    """
    df = pd.read_gbq(query, dialect='standard')
    return df


def query_policy_for_current_date():
    today = date.today().strftime("%Y-%m-%d")
    query = """
        SELECT country_name, region_name, date, school_closing_notes, workplace_closing, workplace_closing_notes, cancel_public_events, cancel_public_events_notes, 
        restrictions_on_gatherings, restrictions_on_gatherings_notes, close_public_transit, close_public_transit_notes, stay_at_home_requirements, stay_at_home_requirements_notes, 
        contact_tracing, contact_tracing_notes, confirmed_cases, deaths international_travel_controls, international_travel_controls_notes FROM `bigquery-public-data.covid19_govt_response.oxford_policy_tracker` 
        where country_name like 'United Kingdom' or country_name like 'China' or country_name like 'Australia' and date = '%s' order by date asc
    """%today
    df = pd.read_gbq(query, dialect='standard')
    return df


def load_historical_data_to_db():
    #TODO this function is to load data to dynamodb
    au_policy2020_df = query_policy_for_Australia()
    cn_policy2020_df = query_policy_for_China()
    uk_policy2020_df = query_policy_for_UK()


if __name__ == '__main__':
    load_historical_data_to_db()

