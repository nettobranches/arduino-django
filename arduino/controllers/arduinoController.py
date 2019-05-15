import pyfirmata

arduino = {
	'digital': tuple(x for x in range(14)),
	'analog': tuple(x for x in range(6)),
	'pwm':(3,5,6,9,10,11),
	'use_ports': True,
	'disabled': (0,1)
}

class ArduinoController(object):
	"""docstring for ClassName"""
	def __init__(self):
		print('create arduino')

	def setPort(self, port):
		try:
			self.port = port
			self.board = pyfirmata.Arduino(self.port)
			self.analogPins = {}
			self.digitalPins = []
			it = pyfirmata.util.Iterator(self.board)
			it.start()
			return True
		except Exception as e:
			print('reason:', e)
			return False

	def startAnalogPin(self, idx, mode):
		if( int(idx) <= 13 and int(idx) >=2 and ( mode == 'i' or mode == 'o' ) ):
			self.analogPins[str(idx)] = self.board.get_pin( 'a:'+str(idx)+':'+mode );
			print("start analog pin in ", idx, " mode ",mode)
		return True

	def startDigitalPin(self, idx, mode):
		if( int(idx) <= 5 and int(idx) >=0 and ( mode == 'i' or mode == 'o' or mode == 'p' ) ):
			self.digitalPins.append( self.board.get_pin( 'd:'+str(idx)+':'+mode ) )

	def getAnalogPin(self, idx):
		value = 0
		if( True ):
			value = self.analogPins[str(idx)].read()
			print('pin '+str(idx)+" value "+str(value))
		return value

	def getData(self, tipo='a', idx='2'):
		return str(self.analog2input.read())

	def setData(self, tipo, idx, value):
		pin= self.board.get_pin( tipo+':'+idx+':'+operation )
		return pin.write()
		