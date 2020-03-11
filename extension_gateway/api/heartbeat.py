from flask_restplus import fields
from werkzeug.exceptions import BadRequest
from maxfw.core import MAX_API, CustomMAXAPI


# Expected input parameters
input_parser = MAX_API.parser()
input_parser.add_argument('foo', type=float, default=0)


# Expected response
expected_response = MAX_API.model('Response', {
    'status': fields.String(required=True, description='Response status message')
})


class HeartBeatAPI(CustomMAXAPI):

	@MAX_API.expect(input_parser)
	@MAX_API.marshal_with(expected_response)
	def post(self):

		result = {'status': 'ok'}

		return result
