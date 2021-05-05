from chalicelib.model.FavouritesTaxiStand import FavouritesTaxiStandModel
from chalice import Blueprint, Response
import uuid
import logging as logger
from chalicelib.authorizer.authorizer import authorizer

favourites_routes = Blueprint(__name__)


@favourites_routes.route('/add-favourites-taxi-stands', methods=['POST'], authorizer=authorizer, cors=True)
def add_favourites_taxi_stands():
    response = {}

    request_body = favourites_routes.current_request.json_body

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


@favourites_routes.route('/get-favourites-taxi-stands/{userId}', methods=['GET'], authorizer=authorizer, cors=True)
def get_favourites_taxi_stands_by_user_id(userId):
    response = {}

    logger.info('userId = {0}'.format(userId))

    if userId:
        favourites_taxi_stand_list = []
        for favouritesTaxiStandFromDB in FavouritesTaxiStandModel.scan(FavouritesTaxiStandModel.userId == userId):
            logger.info('favouritesTaxiStandFromDB = {0}'.format(
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


@favourites_routes.route('/delete-favourites-taxi-stands/{id}', methods=['DELETE'], authorizer=authorizer, cors=True)
def delete_favourites_taxi_stands_by_user_id(id):
    response = {}

    logger.info('id = {0}'.format(id))

    if id:
        for favouritesTaxiStandFormDB in FavouritesTaxiStandModel.scan(FavouritesTaxiStandModel.id == id):
            logger.info('favouritesTaxiStandFormDB = {0}'.format(
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
