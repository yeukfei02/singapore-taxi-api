from chalice import Chalice
from chalicelib.routes.main import main_routes
from chalicelib.authorizer.authorizer import auth_routes
from chalicelib.routes.user import user_routes
from chalicelib.routes.favourites import favourites_routes
from chalicelib.routes.taxi import taxi_routes

from dotenv import load_dotenv
load_dotenv()


app = Chalice(app_name='singapore-taxi-api')
app.register_blueprint(main_routes)
app.register_blueprint(auth_routes)
app.register_blueprint(user_routes)
app.register_blueprint(favourites_routes)
app.register_blueprint(taxi_routes)
