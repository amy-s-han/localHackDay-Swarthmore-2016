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

def tokenReaderTester():

	g = open("token.txt", 'r')

	firstLine = g.readline()
	print firstLine
	timenow = time.time()
	print timenow
	print firstLine
	tokenTime = float(firstLine)
	if timenow - tokenTime < 60:
		print g.readline()

	else:
		print "diff: ", timenow - tokenTime
		g.close()
		g = open("token.txt", 'w')
		g.write(str(timenow) + "\n")
		g.write("blahblahblah\n")

	g.close()

def makeTestTokenTxt():
	g = open("token.txt", 'w')
	timenow = time.time()

	print str(timenow)
	g.write(str(timenow) + "\n")
	g.write("tokenlalalalala")
	g.close()

def imageAPITester():
	# Load raw image file into memory
	pathToFileInDisk = 'bathroom.jpg'
	with open( pathToFileInDisk, 'rb' ) as f:
	    data = f.read()

	# Computer Vision parameters
	params = { 'visualFeatures' : 'Categories, Tags, Description, Faces'} 

	headers = dict()
	headers['Ocp-Apim-Subscription-Key'] = _CVkey
	headers['Content-Type'] = 'application/octet-stream'

	json = None


	start = time.time()
	

	result = msCogServs.processCVRequest(json, data, headers, params )

	if result is not None:

		# Load the original image, fetched from the URL
		data8uint = np.fromstring( data, np.uint8 ) # Convert string to an unsigned int array
		img = cv2.cvtColor( cv2.imdecode( data8uint, cv2.IMREAD_COLOR ), cv2.COLOR_BGR2RGB )

		# in reverse order: lowest confidence -> highest confidence
		tags = sorted(result['tags'], key=lambda x: x['confidence'])

		description = result['description']
		caption = description['captions'][0]['text']

		print "here and:"
		print tags
		print description

	end = time.time()
	print(end - start)

if __name__ == "__main__":

	imageAPITester()

	token = None

	f = open("token.txt", 'r')
	firstLine = f.readline()
	lastTokenTime = float(firstLine)
	currentTime = time.time()
	if currentTime - lastTokenTime > 8 * 60: # need new token
		f.close()
		f = open("token.txt", "w")
		textHeaders = dict()
		textHeaders['Content-Type'] = 'application/json'
		textHeaders['Accept'] = 'application/jwt'
		textHeaders['Ocp-Apim-Subscription-Key'] = _translatorKey
		token = msCogServs.processTokenRequest(textHeaders)

		if token is not None:
			print "YAYAYAYA new token worked"
			print token
			now = time.time()
			f.write(str(now) + "\n")
			f.write(token)
		else:
			print "Could not get token for translation. Exiting."
			exit(0)
	else:
		token = f.readline()
		print "successfully read in token: ##", token, "##"

	f.close()

	print "~~~~~~~~~~~~~~~ NOW TRANSLATING ~~~~~~~~~~~~~~~"

	textToTranslate = 'Hello, my name is Amy.'
	langToTranslateTo = 'ja'

	translatorHeaders = dict()
	translatorHeaders['Accept'] = 'application/xml'
	translatorParameters = dict()
	translatorParameters['appid'] = 'Bearer' + ' ' + token
	translatorParameters['text'] = textToTranslate
	translatorParameters['to'] = langToTranslateTo
	translatorParameters['contentType'] = "text/plain"

	print translatorParameters

	translation = msCogServs.processTranslationRequest(translatorHeaders, translatorParameters)

	print "here and translation: ", translation.content

	# print "~~~~~~~~~~~~~~~ NOW TRANSLATING 2 ~~~~~~~~~~~~~~~"

	# textToTranslate2 = ['Hello, my name is Amy.', 'I like cats', 'I liek mudkips']
	# langToTranslateTo2 = 'es'

	# translatorHeaders2 = dict()
	# translatorHeaders2['Content-Type'] = 'application/x-www-form-urlencoded'
	# translatorHeaders2['Accept'] = 'application/xml'
	# translatorParameters2 = dict()
	# translatorParameters2['appid'] = 'Bearer' + ' ' + token
	# translatorParameters2['texts'] = textToTranslate2
	# translatorParameters2['to'] = langToTranslateTo2

	# print translatorParameters2

	# translation2 = msCogServs.processTranslationArrayRequest(translatorHeaders2, translatorParameters2)

	# print "here and translation: ", translation2
	# print "here and translation: ", translation2.content

	