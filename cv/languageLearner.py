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

NUM_CAMS = 1
webpageIP = 'http://192.168.43.31:5000'

token = None


def processImages(img):
	# Computer Vision parameters
	params = { 'visualFeatures' : 'Categories, Tags, Description, Faces'} 

	headers = dict()
	headers['Ocp-Apim-Subscription-Key'] = _key
	headers['Content-Type'] = 'application/octet-stream'

	json = None

	img_str = cv2.imencode('.jpg', img)[1].tostring()
	result = msCV.processRequest( json, img_str, headers, params)

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
        
def runStream(streamURL, debug = False):
	print "Hi url: ", streamURL

	stream = urllib.urlopen(streamURL)
	bytes = ''

	# for setting up udp
	# ip = "0.0.0.0"
	# port = 5005

	# sock = socket.socket(socket.AF_INET, # Internet
	#          socket.SOCK_DGRAM) # UDP
	# sock.bind((ip, port))
	# sock.setblocking(0)

	print "here2"


	while True:
		bytes += stream.read(1024)

		a = bytes.find('\xff\xd8')
		b = bytes.find('\xff\xd9')

		if a != -1 and b != -1:
			jpg = bytes[a:b + 2]
			bytes= bytes[b + 2:]
			img = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.CV_LOAD_IMAGE_COLOR)

			cv2.imshow('img ', img)
			

			# FIX THIS TO FIT THIS LANGLEARNER
			try:
				data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
				if data == "TAKEPIC": # ticket was scanned! Go process the picture!
					# print "hi"
					luggagePresent = idLuggage(img)
					sendToTicketAgent(luggagePresent)
			except:
				pass

			# to exit press ESC!
			if cv2.waitKey(1) == 27:
				print "you tried to exit........"
				exit(0)   

	source.release()
	cv2.destroyAllWindows()

def eightMinTimer():
	textHeaders = dict()
	textHeaders['Content-Type'] = 'application/json'
	textHeaders['Accept'] = 'application/jwt'
	textHeaders['Ocp-Apim-Subscription-Key'] = _key

	while True:
		sleep(8 * 60) # sleep for 8 minutes, then get new token

		token = msCogServs.processTokenRequest(textHeaders)

		if token is not None:
			print "YAYAYAYA token worked"
			print token





if __name__ == "__main__":

	streamURLS = 'http://192.168.43.100:8080/video'

	worker = threading.Thread(target = runStream, args = (streamURLS))
	worker.daemon = False
	worker.start()

	worker = threading.Thread(target = eightMinTimer, args = ())
	worker.daemon = False
	worker.start()

	worker = threading.Thread(target = translator, args = ())
	worker.daemon = False
	worker.start()


	textHeaders = dict()
	textHeaders['Content-Type'] = 'application/json'
	textHeaders['Accept'] = 'application/jwt'
	textHeaders['Ocp-Apim-Subscription-Key'] = _key
	token = msCogServs.processTokenRequest(textHeaders, _tokenURL)

	if token is not None:
		print "YAYAYAYA token worked"
		print token
	else:
		print "Could not get token for translation. Exiting."
		exit(0)


	if cv2.waitKey(1) == 27:
		exit(0)