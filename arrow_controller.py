import RPi.GPIO as GPIO
import pygame 
import time
import socket

# Setup GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# Timing
inteval = 0.1
regularUpdate = True

# Motore sinistro
enable_left_pin = 33
left_motor_pin1 = 35
left_motor_pin2 = 37

# Motore destro
enable_right_pin = 36
right_motor_pin1 = 38
right_motor_pin2 = 40

# Setup motore sinistro
GPIO.setup(enable_left_pin,GPIO.OUT)
GPIO.setup(left_motor_pin1,GPIO.OUT)
GPIO.setup(left_motor_pin2,GPIO.OUT)

# Setup motore destro
GPIO.setup(enable_right_pin,GPIO.OUT)
GPIO.setup(right_motor_pin1,GPIO.OUT)
GPIO.setup(right_motor_pin2,GPIO.OUT)

# Flag eventi
global hadEvent
global moveForward
global moveReverse
global moveLeft
global moveRight
global pivotLeftFlag
global pivotRightFlag
global quit

hadEvent = True
moveForward = False
moveReverse = False
moveLeft = False
moveRight = False
pivotLeftFlag = False
pivotRightFlag = False
quit = False

# Pygame setup
pygame.init()
screen = pygame.display.set_mode([200,200])
pygame.display.set_caption("SentientCar")

# Setup PWM
left_motor = GPIO.PWM(enable_left_pin,650)
right_motor = GPIO.PWM(enable_right_pin,650)
left_motor.start(0)
right_motor.start(0)

# Gestore eventi tastiera
def pygameHandler(events):
	
	# Flags
	global hadEvent
	global moveForward
	global moveReverse
	global moveLeft
	global moveRight
	global pivotLeftFlag
	global pivotRightFlag
	global quit
	
	# Listener tastiera
	for event in events:
		
		# Uscita
		if event.type == pygame.QUIT:
			hadEvent = True
			quit = True
		
		# Pressione tasto
		elif event.type == pygame.KEYDOWN:
			hadEvent = True
			if event.key == pygame.K_UP:
				moveForward = True
			elif event.key == pygame.K_DOWN:
				moveReverse = True
			elif event.key == pygame.K_LEFT:
				moveLeft = True
			elif event.key == pygame.K_RIGHT:
				moveRight = True
			elif event.key == pygame.K_UP and event.key == pygame.K_LEFT:
				pivotLeftFlag = True
			elif event.key == pygame.K_UP and event.key == pygame.K_RIGHT:
				pivotRightFlag = True  
			elif event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
				quit = True
		
		# Rilascio tasto
		elif event.type == pygame.KEYUP:
			hadEvent = True
			if event.key == pygame.K_UP:
				moveForward = False
			elif event.key == pygame.K_DOWN:
				moveReverse = False
			elif event.key == pygame.K_LEFT:
				moveLeft = False
			elif event.key == pygame.K_RIGHT:
				moveRight = False
			elif event.key == pygame.K_UP and event.key == pygame.K_LEFT:
				pivotLeftFlag = False
			elif event.key == pygame.K_UP and event.key == pygame.K_RIGHT:
				pivotRightFlag = False
			elif event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
				quit = False


# Movimento in avanti
def forward():
	(GPIO.output(left_motor_pin1,GPIO.LOW))
	(GPIO.output(left_motor_pin2,GPIO.HIGH))
	(GPIO.output(right_motor_pin1,GPIO.LOW))
	(GPIO.output(right_motor_pin2,GPIO.HIGH))

# Movimento indietro
def reverse():
	(GPIO.output(left_motor_pin1,GPIO.HIGH))
	(GPIO.output(left_motor_pin2,GPIO.LOW))
	(GPIO.output(right_motor_pin1,GPIO.HIGH))
	(GPIO.output(right_motor_pin2,GPIO.LOW))

# Svolta a sinistra
def turnLeft():
	(GPIO.output(left_motor_pin1,GPIO.LOW))
	(GPIO.output(left_motor_pin2,GPIO.LOW))
	(GPIO.output(right_motor_pin1,GPIO.LOW))
	(GPIO.output(right_motor_pin2,GPIO.HIGH))

# Svolta a destra
def turnRight():
	(GPIO.output(left_motor_pin1,GPIO.LOW))
	(GPIO.output(left_motor_pin2,GPIO.HIGH))
	(GPIO.output(right_motor_pin1,GPIO.LOW))
	(GPIO.output(right_motor_pin2,GPIO.LOW))

# Pivot sinistra
def pivotLeft():
	(GPIO.output(left_motor_pin1,GPIO.HIGH))
	(GPIO.output(left_motor_pin2,GPIO.LOW))
	(GPIO.output(right_motor_pin1,GPIO.LOW))
	(GPIO.output(right_motor_pin2,GPIO.HIGH))

# Pivot destra
def pivotRight():
	(GPIO.output(left_motor_pin1,GPIO.LOW))
	(GPIO.output(left_motor_pin2,GPIO.HIGH))
	(GPIO.output(right_motor_pin1,GPIO.HIGH))
	(GPIO.output(right_motor_pin2,GPIO.LOW))

# Offmode
def offMode():
	(GPIO.output(left_motor_pin1,GPIO.LOW))
	(GPIO.output(left_motor_pin2,GPIO.LOW))
	(GPIO.output(right_motor_pin1,GPIO.LOW))
	(GPIO.output(right_motor_pin2,GPIO.LOW))	

# Main
try:
	print("Premere [ESC] per uscire")

	# Imposta velocita
	user_speed = raw_input("Inserisci la velocita': ")
	car_speed = int(user_speed[0]) * 10
	left_motor.ChangeDutyCycle(car_speed)
	right_motor.ChangeDutyCycle(car_speed)

	while True:

		# Lettura della tastiera
		pygameHandler(pygame.event.get())
		if hadEvent or regularUpdate:

			hadEvent = False
			if quit:
				break
			elif moveForward:
				forward()
			elif moveReverse:
				reverse()
			elif moveLeft:
				turnLeft()
			elif moveRight:
				turnRight()
			elif pivotLeftFlag:
				pivotLeft()
			elif pivotRightFlag:
				pivotRight()
			else:
				offMode()
		time.sleep(inteval)

except KeyboardInterrupt:
	print("SentientCar Controller - OFF")
	left_motor.stop()
	right_motor.stop()
	GPIO.cleanup()
