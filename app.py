from chalice import Chalice, Response, AuthResponse
from chalicelib.routes.main import main_routes
from chalicelib.routes.user import user_routes
from chalicelib.routes.taxi import taxi_routes
from chalicelib.model.FavouritesTaxiStand import FavouritesTaxiStandModel
import jwt
import os
import uuid

from dotenv import load_dotenv
load_dotenv()


app = Chalice(app_name='singapore-taxi-api')
app.register_blueprint(main_routes)
app.register_blueprint(user_routes)
app.register_blueprint(taxi_routes)


@app.authorizer()
def authorizer(auth_request):
    response = {}

    token = auth_request.token
    print('token = {0}'.format(token))

    principal_id = 'user'
    auth_success = False
    if token:
        token = token.replace('Bearer ', '')
        decoded = jwt.decode(token, os.getenv(
            'JWT_SECRET'), algorithms=["HS256"])
        print('decoded = {0}'.format(decoded))
        if decoded:
            principal_id = decoded['id']
            auth_success = True

    if auth_success:
        response = AuthResponse(routes=['*'], principal_id=principal_id)
    else:
        response = AuthResponse(routes=[], principal_id=principal_id)

    return response


@app.route('/add-favourites-taxi-stands', methods=['POST'], authorizer=authorizer, cors=True)
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


@app.route('/get-favourites-taxi-stands/{userId}', methods=['GET'], authorizer=authorizer, cors=True)
def get_favourites_taxi_stands_by_user_id(userId):
    response = {}

    print('userId = {0}'.format(userId))

    if userId:
        favourites_taxi_stand_list = []
        for favouritesTaxiStandFromDB in FavouritesTaxiStandModel.scan(FavouritesTaxiStandModel.userId == userId):
            print('favouritesTaxiStandFromDB = {0}'.format(
                favouritesTaxiStandFromDB))

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


@app.route('/delete-favourites-taxi-stands/{id}', methods=['DELETE'], authorizer=authorizer, cors=True)
def delete_favourites_taxi_stands_by_user_id(id):
    response = {}

    print('id = {0}'.format(id))

    if id:
        for favouritesTaxiStandFormDB in FavouritesTaxiStandModel.scan(FavouritesTaxiStandModel.id == id):
            print('favouritesTaxiStandFormDB = {0}'.format(
                favouritesTaxiStandFormDB))

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
