import requests
import hashlib

baseUrl = 'http://localhost:8081'
userEndpoint = '/createUser'

pw = 'password'
# hash pw in md5 because fe hashes pw in md5 in request
initialHashPw = hashlib.md5(pw.encode()).hexdigest()

data = {'firstName':'Test',
		'lastName':'User',
		'email':'test@test.com',
		'password':initialHashPw}

try:
	response = requests.post(url = baseUrl+userEndpoint, data = data)
	response.raise_for_status()
except requests.exceptions.HTTPError as e:
	print(e)

# using sql to create nodes and datapoints for now (since
# endpoints are unavailable)
