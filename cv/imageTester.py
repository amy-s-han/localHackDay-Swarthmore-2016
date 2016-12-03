#!/usr/bin/env python
import sys
sys.path.append('../cvk2')
import cv2
import httplib
import microsoftCVHelpers as msCV
import microsoftTranslatorHelper as msTranslator
import microsoftCogServicesHelper as msCogServs
import numpy as np
import requests
import time


_CVkey = 'e80f8ece393f4eebb3d98b0bb36f04d0'
_translatorKey = '420c6ab49ed1449db517207d6aef32d9'

if __name__ == "__main__":


	# # Load raw image file into memory
	# pathToFileInDisk = 'bathroom.jpg'
	# with open( pathToFileInDisk, 'rb' ) as f:
	#     data = f.read()

	# # Computer Vision parameters
	# params = { 'visualFeatures' : 'Categories, Tags, Description, Faces'} 

	# headers = dict()
	# headers['Ocp-Apim-Subscription-Key'] = _CVkey
	# headers['Content-Type'] = 'application/octet-stream'

	# json = None


	# start = time.time()
	

	# result = msCogServs.processCVRequest(json, data, headers, params )

	# if result is not None:

	# 	# Load the original image, fetched from the URL
	# 	data8uint = np.fromstring( data, np.uint8 ) # Convert string to an unsigned int array
	# 	img = cv2.cvtColor( cv2.imdecode( data8uint, cv2.IMREAD_COLOR ), cv2.COLOR_BGR2RGB )

	# 	# in reverse order: lowest confidence -> highest confidence
	# 	tags = sorted(result['tags'], key=lambda x: x['confidence'])

	# 	description = result['description']
	# 	caption = description['captions'][0]['text']

	# 	print "here and:"
	# 	print tags
	# 	print description

	# end = time.time()
	# print(end - start)

	token = None

	f = open("token.txt", 'r+')
	lastTokenTime = f.readline()

	currentTime = time.time()
	if currentTime - lastTokenTime > 8 * 60:
		textHeaders = dict()
		textHeaders['Content-Type'] = 'application/json'
		textHeaders['Accept'] = 'application/jwt'
		textHeaders['Ocp-Apim-Subscription-Key'] = _translatorKey
		token = msCogServs.processTokenRequest(textHeaders)

		if token is not None:
			print "YAYAYAYA token worked"
			print token
		else:
			print "Could not get token for translation. Exiting."
			exit(0)
	else:
		

	textToTranslate = "Hello, my name is Amy."
	langToTranslateTo = 'ja'

	translatorHeaders = dict()
	translatorHeaders['Accept'] = 'application/xml'
	translatorParameters = dict()
	translatorParameters['appid'] = 'Bearer' + ' ' + token
	translatorParameters['text'] = textToTranslate
	translatorParameters['to'] = langToTranslateTo

	translation = msCogServs.processTranslationRequest(translatorHeaders, translatorParameters)

	print translation