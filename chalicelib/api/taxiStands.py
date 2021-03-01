import requests
import os
import logging as logger

ROOT_URL = 'http://datamall2.mytransport.sg/ltaodataservice'

def get_taxi_stands_request():
    result = None

    url = '{0}/TaxiStands'.format(ROOT_URL)
    headers = {
        'AccountKey': os.getenv('ACCOUNT_KEY'),
        'Accept': 'application/json'
    }
    response = requests.get(url, headers=headers)

    logger.info('response status = {0}'.format(response.status_code))
    logger.info('response json = {0}'.format(response.json()))

    if response.status_code == 200:
        result = response.json()
    
    return result