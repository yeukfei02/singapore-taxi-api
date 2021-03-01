from chalice import Chalice, AuthResponse, Response
import uuid
import bcrypt
import jwt
import os
import logging as logger

from dotenv import load_dotenv
load_dotenv()

from api.taxiAvailability import get_taxi_availability_request
from api.taxiStands import get_taxi_stands_request

from model.User import UserModel
from model.FavouritesTaxiStand import FavouritesTaxiStandModel

app = Chalice(app_name='singapore-taxi-api')

@app.route('/', methods=['GET'])
def main():
    body = {
        'message': 'singapore-taxi-api'
    }
    return Response(body=body, status_code=200)


@app.route('/signup', methods=['POST'])
def signup():
    response = {}

    request_body = app.current_request.json_body
    if request_body:
        email = request_body['email']
        password = request_body['password']

        if email and password:
            logger.info('email = %s', email)
            logger.info('password = %s', password)

            uuidStr = str(uuid.uuid4())

            salt = bcrypt.gensalt()
            hashedPassword = bcrypt.hashpw(password.encode('utf-8'), salt)
            hashedPasswordDecoded = hashedPassword.decode('utf-8')
            
            userModel = UserModel(id=uuidStr, email=email, password=hashedPasswordDecoded)
            userModel.save()

            body = {
                'message': 'signup'
            }
            response = Response(body=body, status_code=200)
    
    return response


@app.route('/login', methods=['POST'])
def login():
    response = {}

    request_body = app.current_request.json_body
    if request_body:
        email = request_body['email']
        password = request_body['password']

        if email and password:
            logger.info('email = %s', email)
            logger.info('password = %s', password)

            for userFromDB in UserModel.scan(UserModel.email == email):
                print('userFromDB = ', userFromDB)
                if userFromDB:
                    userHashedPasswordFromDB = userFromDB.password
                    isPasswordValid = bcrypt.checkpw(password.encode('utf-8'), userHashedPasswordFromDB.encode('utf-8'))
                    if isPasswordValid:
                        token = jwt.encode(
                            {
                                "id": str(uuid.uuid4()), 
                                "email": email
                            }, 
                            os.getenv('JWT_SECRET'), 
                            algorithm="HS256"
                        )

                        body = {
                            'message': 'login',
                            'token': token,
                            'userId': userFromDB.id
                        }
                        response = Response(body=body, status_code=200)
                    else:
                        body = {
                            'message': 'login error, wrong password',
                        }
                        response = Response(body=body, status_code=400)

    return response


@app.authorizer()
def authorizer(auth_request):
    response = {}

    token = auth_request.token
    logger.info('token = {0}'.format(token))

    principal_id = 'user'
    auth_success = False
    if token:
        token = token.replace('Bearer ', '')
        decoded = jwt.decode(token, os.getenv('JWT_SECRET'), algorithms=["HS256"])
        logger.info('decoded = {0}'.format(decoded))
        if decoded:
            principal_id = decoded['id']
            auth_success = True
    
    if auth_success:
        response = AuthResponse(routes=['*'], principal_id=principal_id)
    else:
        response = AuthResponse(routes=[], principal_id=principal_id)

    return response


@app.route('/add-favourites-taxi-stands', methods=['POST'], authorizer=authorizer)
def add_favourites_taxi_stands():
    response = {}

    request_body = app.current_request.json_body

    if request_body:
        userId = request_body['userId']
        taxiCode = request_body['taxiCode']
        latitude = request_body['latitude']
        longitude = request_body['longitude']
        bfa = request_body['bfa']
        ownership = request_body['ownership']
        type = request_body['type']
        name = request_body['name']

        uuidStr = str(uuid.uuid4())

        favouritesTaxiStandModel = FavouritesTaxiStandModel(
            id=uuidStr, 
            userId=userId, 
            taxiCode=taxiCode, 
            latitude=latitude,
            longitude=longitude,
            bfa=bfa,
            ownership=ownership,
            type=type,
            name=name
        )
        favouritesTaxiStandModel.save()

        body = {
            'message': 'add-favourites-taxi-stands'
        }
        response = Response(body=body, status_code=200)

    return response


@app.route('/get-favourites-taxi-stands/{userId}', methods=['GET'], authorizer=authorizer)
def get_favourites_taxi_stands_by_user_id(userId):
    response = {}

    logger.info('userId = {0}'.format(userId))

    if userId:
        favourites_taxi_stand_list = []
        for favouritesTaxiStandFromDB in FavouritesTaxiStandModel.scan(FavouritesTaxiStandModel.userId==userId):
            logger.info('favouritesTaxiStandFromDB = {0}'.format(favouritesTaxiStandFromDB))

            if favouritesTaxiStandFromDB:
                obj = {
                    'id': favouritesTaxiStandFromDB.id,
                    'taxiCode': favouritesTaxiStandFromDB.taxiCode,
                    'latitude': favouritesTaxiStandFromDB.latitude,
                    'longitude': favouritesTaxiStandFromDB.longitude,
                    'bfa': favouritesTaxiStandFromDB.bfa,
                    'ownership': favouritesTaxiStandFromDB.ownership,
                    'type': favouritesTaxiStandFromDB.type,
                    'name': favouritesTaxiStandFromDB.name,
                    'userId': favouritesTaxiStandFromDB.userId,
                    'createdAt': str(favouritesTaxiStandFromDB.createdAt),
                    'updatedAt': str(favouritesTaxiStandFromDB.updatedAt)
                }
                favourites_taxi_stand_list.append(obj)

        body = {
            'message': 'getFavouritesTaxiStands',
            'favouritesTaxiStand': favourites_taxi_stand_list
        }
        response = Response(body=body, status_code=200)
    else:
        body = {
            'message': 'get_favourites_taxi_stands error, please enter userId'
        }
        response = Response(body=body, status_code=400)

    return response


@app.route('/delete-favourites-taxi-stands/{id}', methods=['DELETE'], authorizer=authorizer)
def delete_favourites_taxi_stands_by_user_id(id):
    response = {}

    logger.info('id = {0}'.format(id))

    if id:
        for favouritesTaxiStandFormDB in FavouritesTaxiStandModel.scan(FavouritesTaxiStandModel.id==id):
            logger.info('favouritesTaxiStandFormDB = {0}'.format(favouritesTaxiStandFormDB))

            if favouritesTaxiStandFormDB:
                favouritesTaxiStandFormDB.delete()
            
                body = {
                    'message': 'deleteFavouritesTaxiStands',
                }
                response = Response(body=body, status_code=200)
            else:
                body = {
                    'message': 'deleteFavouritesTaxiStands error, no this favouritesTaxiStand id',
                }
                response = Response(body=body, status_code=400)
    else:
        body = {
            'message': 'deleteFavouritesTaxiStands error, please enter favouritesTaxiStand id',
        }
        response = Response(body=body, status_code=400)

    return response


@app.route('/get-taxi-availability', methods=['GET'])
def get_taxi_availability():
    response = {}

    get_taxi_availability_result = get_taxi_availability_request()
    logger.info('get_taxi_availability_result = {0}'.format(get_taxi_availability_result))

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

    if taxi_availability_list:
        body = {
            'message': 'get-taxi-availability',
            'taxiAvailability': taxi_availability_list
        }
        response = Response(body=body, status_code=200)

    return response


@app.route('/get-taxi-stands', methods=['GET'])
def get_taxi_stands():
    response = {}

    get_taxi_availability_result = get_taxi_stands_request()
    logger.info('get_taxi_availability_result = {0}'.format(get_taxi_availability_result))

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

    if taxi_stands_list:    
        body = {
            'message': 'get-taxi-stands',
            'taxiStands': taxi_stands_list
        }
        response = Response(body=body, status_code=200)

    return response

