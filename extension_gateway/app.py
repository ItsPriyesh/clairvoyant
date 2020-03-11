from maxfw.core import MAXApp
from api import PredictAPI, HeartBeatAPI
from config import API_TITLE, API_DESC, API_VERSION

max_app = MAXApp(API_TITLE, API_DESC, API_VERSION)
max_app.add_api(PredictAPI, '/predict')
max_app.add_api(HeartBeatAPI, '/heartbeat')
max_app.run()
