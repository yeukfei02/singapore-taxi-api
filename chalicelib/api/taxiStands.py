import requests
import os

ROOT_URL = 'http://datamall2.mytransport.sg/ltaodataservice'


def get_taxi_stands_request():
    result = None

    try:
        url = '{0}/TaxiStands'.format(ROOT_URL)
        headers = {
            'AccountKey': os.getenv('ACCOUNT_KEY'),
            'Accept': 'application/json'
        }
        response = requests.get(url, headers=headers)

        print('response status = {0}'.format(response.status_code))
        print('response json = {0}'.format(response.json()))

        if response.status_code == 200:
            result = response.json()
    except Exception as e:
        print('error = {0}'.format(e))

    return result
