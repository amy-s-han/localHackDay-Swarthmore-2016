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

# translatedLang = "ru"
translatedLang = "es"
# translatedLang = "fr"
# translatedLang = "no"

streamURLS = 'http://130.58.100.149:8080//video'

timeIntervals = [5, 120]

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

def translateSentence(sentence):
	textToTranslate = sentence

	translatorHeaders = dict()
	translatorHeaders['Accept'] = 'application/xml'
	translatorParameters = dict()
	translatorParameters['appid'] = 'Bearer' + ' ' + token
	translatorParameters['text'] = textToTranslate
	translatorParameters['to'] = translatedLang
	translatorParameters['contentType'] = "text/plain"

	translation = msCogServs.processTranslationRequest(translatorHeaders, translatorParameters)

	print "textToTranslate: ", textToTranslate, " and translation: ", translation.content
	length = len(translation.content)
	translationCleaned = translation.content[68:length - 10]
	return translationCleaned


def processImageDescriptions(processedImageDescriptions):
	
	description = processedImageDescriptions['description']
	caption = description['captions'][0]['text']
	print caption

	# tags = sorted(description['tags'], key=lambda x: x['confidence'])
	# print tags
	tags = [""]

	return caption, tags

def handleTranslations(sentence, wordArray):
	print "~~~~~~~~~~~~~~~ NOW TRANSLATING ~~~~~~~~~~~~~~~"

	return translateSentence(sentence), [""]


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

	i = 0

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

			if nowTime - startTime > timeIntervals[i]: #TAKE A PICTURE!
				cv2.destroyAllWindows()
				processedImageDescriptions = processImages(img)
				print "take pic"

				print processedImageDescriptions
				caption, wordArray = processImageDescriptions(processedImageDescriptions)
				tCaption, tWordArray = handleTranslations(caption, wordArray)
				
				# overlay text
				h = img.shape[0]  #Get image height
				cv2.putText(img, tCaption, (16, 16), 
	                cv2.FONT_HERSHEY_SIMPLEX, 0.75,
	                (0,100,0), 3, cv2.CV_AA)

				time.sleep(3)

				cv2.imshow('img', img)
				if cv2.waitKey(1000) == 27:
					print "you tried to exit........"
					exit(0)   

				time.sleep(30)
				i += 1

				if i > len(timeIntervals):
					break
				
			# to exit press ESC!
			if cv2.waitKey(15) == 27:
				print "you tried to exit........"
				exit(0)   

	# source.release()
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