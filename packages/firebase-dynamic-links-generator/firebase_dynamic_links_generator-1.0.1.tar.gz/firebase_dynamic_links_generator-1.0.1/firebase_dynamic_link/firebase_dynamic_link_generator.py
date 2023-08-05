# -*- coding:utf-8 -*-

import requests, json
from oauth2client.service_account import ServiceAccountCredentials
from httplib2 import Http

class GenerateFirebaseDynamicLink():

	FIREBASE_API_URL = 'https://firebasedynamiclinks.googleapis.com/v1/managedShortLinks:create'

	def __init__(self, domain, file_path, name):
		self.file_path 		= file_path
		self.domain 		= domain
		self.name 			= name

		## generate crediantials
		self.credentials = ServiceAccountCredentials.from_json_keyfile_name(self.file_path, scopes=['https://www.googleapis.com/auth/firebase'])

	def generate_dynamic_link(self, link, linkinfo_params={}, suffix_params={}):
		payload = {
				"dynamicLinkInfo": {
				"domainUriPrefix": self.domain,
				"link": link
			},
			"name": self.name,
				"suffix": {
				"option": "SHORT"
			}
		}

		## update the parameters
		payload['dynamicLinkInfo'].update(linkinfo_params)
		payload['suffix'].update(suffix_params)

		## payload dump
		payload = json.dumps(payload)


		http_auth = self.credentials.authorize(Http())

		response, content = http_auth.request(
		    method="POST",
		    uri=self.FIREBASE_API_URL,
		    headers={'Content-Type': 'application/json'},
		    body=payload
		)

		## decode the response data
		response_data = content.decode()
		response_data = json.loads(response_data)

		return response_data