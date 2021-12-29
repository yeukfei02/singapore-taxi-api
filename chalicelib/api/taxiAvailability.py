import requests
import os

ROOT_URL = 'http://datamall2.mytransport.sg/ltaodataservice'


def get_taxi_availability_request():
    result = None

    try:
        url = '{}/Taxi-Availability'.format(ROOT_URL)
        headers = {
            'AccountKey': os.getenv('ACCOUNT_KEY'),
            'Accept': 'application/json'
        }
        response = requests.get(url, headers=headers)

        print('response status = ', response.status_code)
        print('response json = ', response.json())

        if response.status_code == 200:
            result = response.json()
    except Exception as e:
        print('error = ', e)

    return result
