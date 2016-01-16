""" TODO: DOC
"""

from nunchuck_driver import NunchuckDriver
from robot_comm import RobotComm
from delay_sim import Delayer
from time import sleep


""" Commands available in robot driver:
	stop
	forward
	backward
	left
	right
	arm_left
	arm_right
	arm_up
	arm_down
	arm_h_pos
	arm_v_pos
	wrist_left
	wrist_right
	wrist_pos
	open_grasp
	close_grasp
"""

FIXED_SPEED = 100
FIXED_STEP = 5

# Nunchuck limit values
# Accel ranges
LIM_X_LEFT = (73,127)
LIM_X_RIGHT = (-128,-80)
LIM_Y_UP = (70,127)
LIM_Y_DOWN = (-128,-88)
# Joy ranges
LIM_JOY_X_LEFT = (24,127)
LIM_JOY_X_RIGHT = (-128,-30)
LIM_JOY_Y_UP = (-34,-128)
LIM_JOY_Y_DOWN = (127,31)

# Arm limit values
ARM_H_MIN = 0
ARM_H_MAX = 180
ARM_V_MIN = 70
ARM_V_MAX = 180
WRIST_MIN = 0
WRIST_MAX = 180
GRASP_MIN = 50
GRASP_MAX = 180

# Sampling loop time
UPDATE_TIME = 0.5

def translate(val, src_min, src_max, dst_min, dst_max):
	""" Move a value from the range [src_min,src_max] to [dst_min,dst_max]"""
	src_length = float(src_max - src_min)
	dst_length = float(dst_max - dst_min)
	# 0-1 range
	new_val = float(val - src_min) / src_length
	# dst range
	return dst_min + dst_length*new_val

if __name__ == '__main__':
	nunchuck = NunchuckDriver()
	nunchuck.start()
	
	robot = RobotComm()
	delayer = Delayer(robot.send)
	delayer.start()

	# IMPLEMENTATION EXAMPLE:
	try:
		while True:
			# Base movement
			if nunchuck.data["buttonZ"] == 1 and nunchuck.data["buttonC"] == 0:
				x = nunchuck.data["accelX"]
				y = nunchuck.data["accelY"]
				# Check which movement is stronger (for/back or turn)
				if abs(y) < abs(x): # Y strongerclose_grasp
					if y < 0 and y > -120:
						speed = 255
						if y < (LIM_Y_DOWN[1] - 10):
							speed = translate(y, LIM_Y_DOWN[1] - 10, LIM_Y_DOWN[0], 255, 200)
						delayer.add_action("forward", speed)
					elif y > 0 and y < 120:
						speed = 255
						if y > (LIM_Y_UP[0] + 10):
							speed = translate(y, LIM_Y_UP[0] + 10, LIM_Y_UP[1], 255, 200)
						delayer.add_action("backward", speed)
					else:
						delayer.add_action("stop", 0)
				else: # X stronger
					if x < 0 and x > -120:
						speed = 255
						if x < (LIM_X_RIGHT[1] - 10):
							speed = translate(x, LIM_X_RIGHT[1] - 10, LIM_X_RIGHT[0], 255, 200)
						delayer.add_action("right", speed)
					elif x > 0 and x < 120:
						speed = 255
						if x > (LIM_X_LEFT[0] + 10):
							speed = translate(x, LIM_X_LEFT[0] + 10, LIM_X_LEFT[1], 255, 200)
						delayer.add_action("left", speed)
					else:
						delayer.add_action("stop", 0)

			# Arm movement (joy relative, accel absolute)
			elif nunchuck.data["buttonZ"] == 0 and nunchuck.data["buttonC"] == 1:
				x = nunchuck.data["accelX"]
				y = nunchuck.data["accelY"]
				joyX = nunchuck.data["joyX"]
				joyY = nunchuck.data["joyY"]
				val = 90
				# left/right
				if joyX < 0 and joyX > -120:
					delayer.add_action("arm_right", FIXED_STEP)
				elif joyX > 0 and joyX < 120:
					delayer.add_action("arm_left", FIXED_STEP)

				# up/down
				if y < 0:
					val = translate(y, LIM_Y_DOWN[0], LIM_Y_DOWN[1], ARM_V_MAX/2, ARM_V_MIN)
				else:
					val = translate(y, LIM_Y_UP[0], LIM_Y_UP[1], ARM_V_MAX, ARM_V_MAX/2)
				delayer.add_action("arm_v_pos", val)
				
				# wrist left/right
				if x < 0:
					val = translate(x, LIM_X_RIGHT[0], LIM_X_RIGHT[1], WRIST_MAX/2, WRIST_MIN)
				else:
					val = translate(x, LIM_X_LEFT[0], LIM_X_LEFT[1], WRIST_MAX, WRIST_MAX/2)
				delayer.add_action("wrist_pos", val)
				
				# grasp open/close
				if joyY < 0 and joyY > -120:
					delayer.add_action("close_grasp", FIXED_STEP)
				elif joyY > 0 and joyY < 120:
					delayer.add_action("open_grasp", FIXED_STEP)

			else: # No button or both buttons pushed -> stop
				delayer.add_action("stop", 0)

			sleep(UPDATE_TIME)

	except:
		nunchuck.stop()
		robot.stop()
		raise