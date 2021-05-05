from chalice import Blueprint, Response

main_routes = Blueprint(__name__)


@main_routes.route('/', methods=['GET'], cors=True)
def main():
    body = {
        'message': 'singapore-taxi-api'
    }
    return Response(body=body, status_code=200)
