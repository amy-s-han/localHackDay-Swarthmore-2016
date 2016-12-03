from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit
import urllib2
import datetime
import json
import config
import time
import socket
import struct 

app = Flask(__name__)
apiKey = config.deltaKey
socketio = SocketIO(app)

if __name__ == '__main__':
    socketio.run(app)

@app.route('/')
def index():
    return render_template('estimator.html')

# @app.route('/submitCVResult', methods=['POST'])
# def submitCVResult():
#     resultJSON = request.json
#     print resultJSON
#     typeOfBag = resultJSON['result']

#     volume = 2
#     dimensions = simpleLuggageDims[typeOfBag]
#     for val in dimensions:
#         volume = volume * val

#     updateOverheadBinStatus(volume)

#     global luggageCount
#     if typeOfBag == "bag":
#         luggageCount = (luggageCount[0], luggageCount[1] + 1)
#     else:
#         luggageCount = (luggageCount[0] + 1, luggageCount[1])
    
#     socketio.emit("updated_luggage_count", { "bags": luggageCount[1], "suitcases": luggageCount[0], "updated": typeOfBag})

#     return "lol"

# @socketio.on('flight_info_query')
# def handle_my_flight_info_query(json):
#     global totalOverHeadVolume

#     flightnumber = json['flightnumber']
#     #print flightnumber
#     flightStatusJSON = getFlightStatus(flightnumber)
#     if flightStatusJSON != None:
#         aircraftType = getAircraftType(flightStatusJSON)
#         if aircraftType in simpleBinDims:	
#             dimensions = simpleBinDims[aircraftType]
#             volume = 1
#             for element in dimensions:
#                 volume = volume*element
#             totalOverHeadVolume = volume
#             print "Volume of ", aircraftType, dimensions, " is ", volume
#         else:
#             print "No dimension info on that flight's aircraft"
#             emit('flight_info_query_fail', { "error": "No dimension info on that flight's aircraft"})
# 		#print aircraftType, dim 
#     else:
#         print "That flight number does not exist"
#         emit('flight_info_query_fail', { "error": "That flight number does not exist"})

# @socketio.on('initiate_scan')
# def handle_initiate_scan(json):

#     ip = config.CVip # CV's ip address
#     port = config.CVport
#     message = "TAKEPIC"
#     sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     sock.sendto(message, (ip, port))

#     global boardingPassIndex
#     boardingPassData = boardingPasses[boardingPassIndex]
#     boardingPassIndex += 1
#     boardingPass = {}
#     boardingPass['name'] = boardingPassData[0]
#     boardingPass['class'] = boardingPassData[1]
#     boardingPass['seat'] = boardingPassData[2]
#     boardingPass['destination'] = boardingPassData[3]
#     emit('passenger_information_update', boardingPass)

    
# @socketio.on('override_request')
# def handle_override_request(json):
#     approved = json['approved']
#     if approved == True:
#         updateOverheadBinStatus()

# def updateOverheadBinStatus(currentLuggageVolume):
#     global currentOverHeadVolume
#     global totalOverHeadVolume
#     currentOverHeadVolume = currentOverHeadVolume + currentLuggageVolume
#     percentage = float(currentOverHeadVolume)/ totalOverHeadVolume
#     print percentage
#     socketio.emit("new_overhead_volume", { 'percentage': percentage})

# def getFlightStatus(flightNumber):
#     date = now.strftime("%Y-%m-%d")
#     url = deltaAPIBaseUrl + "status?flightNumber=" + flightNumber + "&flightOriginDate=" + date + "&apikey=" + apiKey
#     #print url
#     response = urllib2.urlopen(url)
#     if response.getcode() == 200:
#         rawData = response.read()
#         jsonData = json.loads(rawData)
#         #print jsonData
#         status = jsonData['flightStatusResponse']['status']
#         if status == "FAIL":
#             return None
#         return jsonData
#     else:
#         return None

# def getAircraftType(j):
#     try:
#         equipmentType = j['flightStatusResponse']['statusResponse']['flightStatusTO']['flightStatusLegTOList']['equipmentCodeDelta']
#     except:
#         equipmentType = j['flightStatusResponse']['statusResponse']['flightStatusTO']['flightStatusLegTOList'][0]['equipmentCodeDelta']
# return equipmentType