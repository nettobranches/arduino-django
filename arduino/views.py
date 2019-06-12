from django.shortcuts import render
from django.http import HttpResponse
from .controllers.arduinoController import ArduinoController

from .api.serializers import SubjectSerializer
from rest_framework.response import Response

arduino = None

def index(request):	
	return render(request, 'index.html')

def init(request, port):
	global arduino
	arduino = ArduinoController()
	res = arduino.setPort(port)
	return HttpResponse(res)

def set_value(request):
	html = "set value"
	return HttpResponse(html)

def get_value(request, tipo, idx):
	pin = arduino.getData(tipo, idx)
	return HttpResponse(pin)

def test_read(request):
	now = 111
	html = "<html><body>It is now %s.</body></html>" % now
	return HttpResponse(html)

def startAnalogPin(request, idx, mode):
	res = arduino.startAnalogPin(idx, mode)
	return HttpResponse(res)

def startDigitalPin(request, idx, mode):
	res = arduino.startDigitalPin(idx, mode)
	return HttpResponse(res)

def getAnalogVal(request, idx):
	res = arduino.getAnalogPin(idx)
	return HttpResponse(res)

def getDigitalVal(request, idx):
	res = arduino.getDigitalPin(idx)
	return HttpResponse(res)

def setDigitalVal(request, idx, val):
	res = arduino.setDigitalPin(idx, val)
	return HttpResponse(res)

def moveServo(request, deg):
	arduino.moveServo(deg) #grados
	return HttpResponse('move')

def startServo(request):
	arduino.startServo(2)
	return HttpResponse('start')

def semaforo(request):
	port = "COM3"
	global arduino
	arduino = ArduinoController()
	arduino.setPort(port)
	arduino.startDigitalPin('8', 'o')
	arduino.startDigitalPin('9', 'o')
	arduino.startDigitalPin('10', 'o')

	return render(request, 'semaforo.html')

def start_semaforo(request, r, y, g):

	return HttpResponse('start')
