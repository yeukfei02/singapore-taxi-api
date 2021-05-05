from chalice import Blueprint, Response
from chalicelib.api.taxiStands import get_taxi_stands_request
from chalicelib.api.taxiAvailability import get_taxi_availability_request

taxi_routes = Blueprint(__name__)


@taxi_routes.route('/get-taxi-availability', methods=['GET'], cors=True)
def get_taxi_availability():
    response = {}

    get_taxi_availability_result = get_taxi_availability_request()
    print('get_taxi_availability_result = {0}'.format(
        get_taxi_availability_result))

    taxi_availability_list = []
    if get_taxi_availability_result:
        valueList = get_taxi_availability_result['value']
        if valueList:
            for value in valueList:
                latitude = value['Latitude']
                longitude = value['Longitude']

                obj = {
                    'latitude': latitude,
                    'longitude': longitude
                }
                taxi_availability_list.append(obj)

    body = {
        'message': 'get-taxi-availability',
        'taxiAvailability': taxi_availability_list
    }
    response = Response(body=body, status_code=200)

    return response


@taxi_routes.route('/get-taxi-stands', methods=['GET'], cors=True)
def get_taxi_stands():
    response = {}

    get_taxi_availability_result = get_taxi_stands_request()
    print('get_taxi_availability_result = {0}'.format(
        get_taxi_availability_result))

    taxi_stands_list = []
    if get_taxi_availability_result:
        valueList = get_taxi_availability_result['value']
        if valueList:
            for value in valueList:
                taxiCode = value['TaxiCode']
                latitude = value['Latitude']
                longitude = value['Longitude']
                bfa = value['Bfa']
                ownership = value['Ownership']
                type = value['Type']
                name = value['Name']

                obj = {
                    'taxiCode': taxiCode,
                    'latitude': latitude,
                    'longitude': longitude,
                    'bfa': bfa,
                    'ownership': ownership,
                    'type': type,
                    'name': name
                }
                taxi_stands_list.append(obj)

    body = {
        'message': 'get-taxi-stands',
        'taxiStands': taxi_stands_list
    }
    response = Response(body=body, status_code=200)

    return response
