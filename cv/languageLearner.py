#!/usr/bin/env python
import sys
sys.path.append('../cvk2')
import cvk2
import cv2
import httplib
import microsoftCogServicesHelper as msCogServs
import numpy as np
import requests
import socket
import urllib
import utils
import time
import threading

_CVkey = 'e80f8ece393f4eebb3d98b0bb36f04d0'
_translatorKey = '420c6ab49ed1449db517207d6aef32d9'

token = None

translatedLang = ""

streamURLS = 'http://130.58.100.149:8080//video'

def processImages(img):
	# Computer Vision parameters
	params = { 'visualFeatures' : 'Categories, Tags, Description, Faces'}
	
	if translatedLang == 'chinese':
		params['language'] = 'zh'
	else:
		params['language'] = 'en'

	headers = dict()
	headers['Ocp-Apim-Subscription-Key'] = _CVkey
	headers['Content-Type'] = 'application/octet-stream'


	json = None

	img_str = cv2.imencode('.jpg', img)[1].tostring()
	result = msCogServs.processCVRequest( json, img_str, headers, params)

	return result

def sendToTicketAgent(luggagePresent):
	# POST. "/submitCVResult" 
	print "POSTING TO TICKET AGENT"

	ticketURL = webpageIP + "/submitCVResult"

	if luggagePresent is None or luggagePresent == '':
		luggagePresent.append("no luggage detected")

	retries = 0
	result = None

	while True:

		payload = '{"result": "' + luggagePresent + '"}'
		headers = {'content-type': "application/json", 'cache-control': "no-cache",}
		response = requests.request("POST", ticketURL, data = payload, headers = headers)

		if response.status_code == 429: 

			print( "Message: %s" % ( response.json()['error']['message'] ) )

			if retries <= _maxNumRetries: 
				time.sleep(1) 
				retries += 1
				continue
			else: 
				print( 'Error: failed after retrying!' )
			break

		elif response.status_code == 200 or response.status_code == 201:

			print "success!!!\n"
		else:
			print( "Error code: %d" % ( response.status_code ) )
			print( "Message: %s" % ( response.json()['error']['message'] ) )

		break
        
def runStream(debug = False):
	print "Hi streamURLS: ", streamURLS

	stream = urllib.urlopen(streamURLS)
	bytes = ''

	# for setting up udp
	# ip = "0.0.0.0"
	# port = 5005

	# sock = socket.socket(socket.AF_INET, # Internet
	#          socket.SOCK_DGRAM) # UDP
	# sock.bind((ip, port))
	# sock.setblocking(0)

	print "here2"

	startTime = time.time()

	while True:
		bytes += stream.read(1024)

		a = bytes.find('\xff\xd8')
		b = bytes.find('\xff\xd9')

		if a != -1 and b != -1:
			jpg = bytes[a:b + 2]
			bytes= bytes[b + 2:]
			img = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.CV_LOAD_IMAGE_COLOR)

			cv2.imshow('img ', img)
			
			nowTime = time.time()

			print nowTime
			if nowTime - startTime > 5: #TAKE A PICTURE!
				print "take pic"
				processedImageDescriptions = processImages(img)
				print processedImageDescriptions
				break
			# to exit press ESC!
			if cv2.waitKey(15) == 27:
				print "you tried to exit........"
				exit(0)   

	source.release()
	cv2.destroyAllWindows()

def eightMinTimer():
	textHeaders = dict()
	textHeaders['Content-Type'] = 'application/json'
	textHeaders['Accept'] = 'application/jwt'
	textHeaders['Ocp-Apim-Subscription-Key'] = _translatorKey

	while True:
		time.sleep(8 * 60) # sleep for 8 minutes, then get new token

		token = msCogServs.processTokenRequest(textHeaders)

		if token is not None:
			print "YAYAYAYA token worked"
			print token
			now = time.time()
			f = open("token.txt", "w")
			f.write(str(now) + "\n")
			f.write(token)
			f.close()



def translator():
	pass

if __name__ == "__main__":

	

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


	worker = threading.Thread(target = eightMinTimer)
	worker.daemon = False
	worker.start()

	# worker = threading.Thread(target = translator)
	# worker.daemon = False
	# worker.start()

	runStream()

	if cv2.waitKey(1) == 27:
		exit(0)