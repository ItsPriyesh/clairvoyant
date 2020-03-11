from flask_restplus import fields
from werkzeug.exceptions import BadRequest
from maxfw.core import MAX_API, CustomMAXAPI

from .gateway import RXTXGateway

# Expected input parameters
input_parser = MAX_API.parser()
input_parser.add_argument('foo', type=float, default=0)

# Expected response
expected_response = MAX_API.model('Response', {
    'status': fields.String(required=True, description='Response status message')
})

class MotionAPI(CustomMAXAPI):

	@MAX_API.expect(input_parser)
	@MAX_API.marshal_with(expected_response)
	def post(self):

		x = RXTXGateway()
		x.get_input_queue().put("motion")

		result = {'status': 'ok'}

		return result
