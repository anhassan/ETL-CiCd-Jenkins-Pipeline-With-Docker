import requests
import random
import json
import pandas as pd

list_countries = ["UK","USA","India","Pakistan","Kenya","Argentina","China","Denmark","Egypt","Canada"]
NUM_ROWS = 10
FILE_NAME = "customer_data"

# Utility functions for parsing data from relevant REST Api's

# Parsing json data from random customer based REST Api
def parse_customer_api(list_countries):
  BASE_URL = "https://randomuser.me/api/0.8"
  customer_json = json.loads(requests.get(BASE_URL).text)
  customer_data = customer_json["results"][0]
  customer_name = customer_data["user"]["name"]["first"] +" " +\
                  customer_data["user"]["name"]["last"]
  customer_gender = customer_data["user"]["gender"]
  customer_email = customer_data["user"]["email"]
  customer_contact = customer_data["user"]["phone"]
  customer_username = customer_data["user"]["username"]
  customer_password = customer_data["user"]["password"]
  customer_location = list_countries[random.randint(0,len(list_countries)-1)]
  return [customer_name,customer_gender,customer_email,customer_contact,
  customer_username,customer_password,customer_location]

# Parsing json data from country based REST Api
JOIN_PARAM = 'country'
def parse_api_response(country_name):
  get_request_url = "https://restcountries.eu/rest/v2/name/{}?fullText=true".format(country_name)
  response = requests.get(get_request_url)
  response_text = json.loads(response.text)[0]
  return [response_text["capital"], response_text["latlng"][0], response_text["latlng"][1]]

#---------------------------------------------EXTRACT & TRANSFORM PHASE-------------------------------------------------

customer_data = [parse_customer_api(list_countries) for row in range(0,NUM_ROWS)]
customer_df = pd.DataFrame.from_records(customer_data,
                                        columns=["name","gender","email","contact","username","password","country"])
customer_country = customer_df["country"].unique()
country_data = [[country] + parse_api_response(country) for country in customer_country]
country_df = pd.DataFrame.from_records(country_data, columns=["country","capital","latitude","longitude"])

customer_data_transformed = customer_df.set_index(JOIN_PARAM).join(country_df.set_index(JOIN_PARAM)).reset_index()
data_columns = customer_data_transformed.columns
data_columns_resequenced =  list(data_columns[1:-1]) + [data_columns[0]]
customer_data_transformed = customer_data_transformed[data_columns_resequenced]

#--------------------------------------------------LOAD PHASE-----------------------------------------------------------
print("ETL terminated.....")
customer_data_transformed.to_csv("/etl/data/{}.csv".format(FILE_NAME))



