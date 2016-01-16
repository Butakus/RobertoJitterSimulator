import heapq
import random
from threading import Thread
from time import time, sleep
from math import sqrt

INTRINSIC_DELAY = 200
DELAY_VAR = 100
WEIBULL_SHAPE = 2

class Delayer(Thread):
	"""TODO: Docs"""
	
	def __init__(self, action_callback, intrinsic_delay=INTRINSIC_DELAY, delay_var=DELAY_VAR):

		self.action_callback = action_callback
		
		self.queue = []
		self.intrinsic_delay = intrinsic_delay
		self.delay_var = delay_var

		Thread.__init__(self)
		self.daemon = True
		self.running = True

	def run(self):
		print 'Delayer thread running'
		while self.running:
			if len(self.queue) > 0:
				#print 'current_time: {}\titem_time: {}'.format(time(), self.queue[0][0])

				if self.queue[0][0] <= time():
					action = heapq.heappop(self.queue)
					self.action_callback(action[1], action[2])
			sleep(0.01)

	def random_sample(self):
		scale = sqrt(2) * self.delay_var
		return (self.intrinsic_delay + random.weibullvariate(scale, WEIBULL_SHAPE)) / 1000
		

	def add_action(self, command, argument):
		# TODO: Use the correct delay statistical model, not gaussian distribution
		exit_time = time() + self.random_sample()
		heapq.heappush(self.queue, (exit_time, command, argument))

	def stop(self):
		print 'Stopping Delayer'
		self.running = False

start_t = 0
last_t = 0
def action_cb(command, argument):
	global last_t
	print '-------------------------------'
	print '[OUT]:\tSending command: {}({})'.format(command, argument)
	t = time()
	print 'Global time: {}ms'.format(1000 * (t - start_t))
	print 'Time diff: {}ms'.format(1000 * (t - last_t))
	last_t = t

if __name__ == '__main__':
	# Test
	dlyr = Delayer(action_cb)
	dlyr.start()
	
	start_t = time()
	last_t = start_t
	
	for i in xrange(10):
		dlyr.add_action('VeryCommand', i)
		sleep(0.15)
	sleep(1)
	dlyr.stop()
