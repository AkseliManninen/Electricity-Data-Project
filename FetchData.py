import boto3
import urllib3
import requests
import json
from datetime import date

today = date.today()
d1 = today.strftime("%Y-%m-%d")

# Get the token for the API
token = "djnK2W5vhk3W4fDZIZA9ka3Blr4ncJsv4R3mgFYK"

# Header for the api
headers = {'x-api-key': token}

# Randomly selected start and end times
#start_time = "2022-10-25T00:00:00+03:00"
#end_time = "2022-10-26T00:00:00+03:00"

start_time = d1 + "T00:00:00+03:00"
end_time = d1 + "T23:00:00+03:00"


query = {
        "start_time": start_time,
        "end_time": end_time,
        }

# URL for the API, where 124 is the variableId
url = "https://api.fingrid.fi/v1/variable/124/events/csv?" 

response = requests.get(url, headers=headers, params = query)

print(response.status_code)

bucket_name = "electricity-data-bucket"
file_name = "electricity_data.csv"
s3_path = file_name


def lambda_handler(event, context):

    string = response.text

    s3 = boto3.resource("s3")

    # get existing data from s3
    current_data = boto3.client('s3').get_object(Bucket = bucket_name, Key = s3_path)['Body'].read().decode('utf-8')
    
    string = string.splitlines(True)[1:]
    string = ''.join(string)

    append_data = str(current_data) + string
    
    #s3.Bucket(bucket_name).put_object(Key=s3_path, Body=string)
    s3.Bucket(bucket_name).put_object(Key=s3_path, Body=append_data)
    return {
        'statusCode': 200,
    }



    





    