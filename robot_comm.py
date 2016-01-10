""" TODO: DOC
"""

import socket
from time import sleep

PORT = 7070


class RobotComm(object):
	"""Thread to communicate the master with the slave (Roberto)"""
	
	def __init__(self, address=''):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.robot_address = (address, PORT)

	def send(self, command, argument=0):
		argument = argument & 0xFF
		msg = command + ',' + str(argument) + '\n'
		self.sock.sendto(msg, self.robot_address)
		print '[RobotComm]:\tSending command: {}({})'.format(command, argument)

	def stop(self):
		print 'Stopping comms'
		self.sock.close()


if __name__ == '__main__':
	# TEST
	comms = RobotComm('127.0.0.1')

	while True:
		command = raw_input()
		if command == 's':
			print 'Sending stop command'
			comms.send('stop')
		elif command == 'f':
			print 'Sending forward command'
			comms.send('forward', 80)
		elif command == 'q':
			break
	comms.stop()