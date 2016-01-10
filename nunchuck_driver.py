""" TODO: Doc
"""

import serial
from time import sleep
from threading import Thread


class NunchuckDriver(Thread):
	"""Thread to communicate with the Nunchuck controller and provide the data"""
	
	def __init__(self, port='/dev/ttyACM0', baudrate=9600):
		self.data = {
			'accelX' : 0,
			'accelY' : 0,
			'accelZ' : 0,
			'joyX' : 0,
			'joyY' : 0,
			'buttonZ' : 0,
			'buttonC' : 0
		}
		self._keys = [
			'accelX',
			'accelY',
			'accelZ',
			'joyX',
			'joyY',
			'buttonZ',
			'buttonC'
		]

		self.connect(port, baudrate)
		sleep(0.2)

		Thread.__init__(self)
		self.daemon = True
		self.running = True

	def connect(self, port, baudrate):
		try:
			print 'Connecting to serial port...'
			self.ser = serial.Serial(port=port, baudrate=baudrate)
		except serial.serialutil.SerialException:
			print '\nSerial device not connected. Program aborted.\n'
			exit(1)
		except ValueError as ve:
			print '\nSerial parameters not valid.\n'
			raise ve
		else:
			print 'Done!\n'

	def stop(self):
		if self.ser.isOpen():
			print '\nClosing serial port...'
			self.ser.close()
			print 'Serial port closed.'
		else:
			print 'Serial port is already closed.'
		print 'Stopping thread...'
		self.running = False

	def run(self):
		while self.running and self.ser.isOpen():
			if self.ser.inWaiting() > 0:
				received = self.ser.read(1)
				# Sets of data separated by newlines
				if received == '\n':
					for i in xrange(7):
						buff = ''
						received = self.ser.read(1)
						# Elements separated by smicolons
						while received != ';':
							buff += received
							received = self.ser.read(1)
						try:
							self.data[self._keys[i]] = int(buff)
						except ValueError, ve:
							print 'Parsing error: {}'.format(ve)


if __name__ == '__main__':
	nunchuck = NunchuckDriver()
	nunchuck.start()
	while True:
		print '\n-------------------------------------\n'
		for d in nunchuck._keys:
			print '{}:   \t{}'.format(d, nunchuck.data[d])
		sleep(0.05)