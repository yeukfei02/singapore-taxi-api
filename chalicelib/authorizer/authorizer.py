from chalice import Blueprint, AuthResponse
import jwt
import os
import logging as logger

auth_routes = Blueprint(__name__)


@auth_routes.authorizer()
def authorizer(auth_request):
    response = {}

    token = auth_request.token
    logger.info('token = {0}'.format(token))

    principal_id = 'user'
    auth_success = False
    if token:
        token = token.replace('Bearer ', '')
        decoded = jwt.decode(token, os.getenv(
            'JWT_SECRET'), algorithms=["HS256"])
        logger.info('decoded = {0}'.format(decoded))
        if decoded:
            principal_id = decoded['id']
            auth_success = True

    if auth_success:
        response = AuthResponse(routes=['*'], principal_id=principal_id)
    else:
        response = AuthResponse(routes=[], principal_id=principal_id)

    return response
