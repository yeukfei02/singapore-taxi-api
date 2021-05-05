from chalice import Blueprint, Response
import uuid
import bcrypt
import logging as logger
import jwt
import os
from chalicelib.model.User import UserModel

user_routes = Blueprint(__name__)


@user_routes.route('/signup', methods=['POST'], cors=True)
def signup():
    response = {}

    request_body = user_routes.current_request.json_body
    if request_body:
        email = request_body['email']
        password = request_body['password']

        if email and password:
            logger.info('email = {0}', email)
            logger.info('password = {0}', password)

            uuidStr = str(uuid.uuid4())

            salt = bcrypt.gensalt()
            hashedPassword = bcrypt.hashpw(password.encode('utf-8'), salt)
            hashedPasswordDecoded = hashedPassword.decode('utf-8')

            userModel = UserModel(id=uuidStr, email=email,
                                  password=hashedPasswordDecoded)
            userModel.save()

            body = {
                'message': 'signup'
            }
            response = Response(body=body, status_code=200)

    return response


@user_routes.route('/login', methods=['POST'], cors=True)
def login():
    response = {}

    request_body = user_routes.current_request.json_body
    if request_body:
        email = request_body['email']
        password = request_body['password']

        if email and password:
            logger.info('email = {0}', email)
            logger.info('password = {0}', password)

            for userFromDB in UserModel.scan(UserModel.email == email):
                logger.info('userFromDB = {0}', userFromDB)
                if userFromDB:
                    userHashedPasswordFromDB = userFromDB.password
                    isPasswordValid = bcrypt.checkpw(password.encode(
                        'utf-8'), userHashedPasswordFromDB.encode('utf-8'))
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
                else:
                    body = {
                        'message': 'login error, no this user',
                    }
                    response = Response(body=body, status_code=400)

    return response
