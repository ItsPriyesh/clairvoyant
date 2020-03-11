from maxfw.core import MAXApp
from api import RXTXGateway
from api import PredictAPI, HeartBeatAPI, MotionAPI
from config import API_TITLE, API_DESC, API_VERSION

gateway_terminal = RXTXGateway()
gateway_terminal.run()

max_app = MAXApp(API_TITLE, API_DESC, API_VERSION)
max_app.add_api(PredictAPI, '/predict')
max_app.add_api(HeartBeatAPI, '/heartbeat')
max_app.add_api(MotionAPI, '/motion')
max_app.run()


