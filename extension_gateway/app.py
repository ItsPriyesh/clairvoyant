from maxfw.core import MAXApp
from api import PredictAPI
from config import API_TITLE, API_DESC, API_VERSION

max_app = MAXApp(API_TITLE, API_DESC, API_VERSION)
max_app.add_api(PredictAPI, '/predict')
max_app.run()
