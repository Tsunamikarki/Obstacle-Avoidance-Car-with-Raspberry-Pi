import RPi.GPIO as GPIO 
import time

#motors 
enRt=33 #enA 
enLt=35 #enB
rtFwd=11 #in1
rtRev=13 #in2
ltFwd=18 #in3
ltRev=16 #in4 

#ultrasonic sensor
trig=29
echo=31
safeDis=20 
disAtScan = [3]
angles = [0,90,180]
#servo
servoPin=32
duty=90

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(rtFwd, GPIO.OUT) #in1 forwardpin
GPIO.setup(rtRev, GPIO.OUT) #in2
GPIO.setup(ltRev, GPIO.OUT) #in3
GPIO.setup(ltFwd, GPIO.OUT) #in4 forwardpin
GPIO.setup(enRt, GPIO.OUT) #ENABLE for right motor 
GPIO.setup(enLt, GPIO.OUT) #ENABLE for left motor 
speedEnRt = GPIO.PWM(enRt, 1000)
speedEnLt = GPIO.PWM(enLt, 1000)

#ultrasonic sensor
GPIO.setup(trig, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)

#servo motor
GPIO.setup(servoPin, GPIO.OUT)
servo=GPIO.PWM(servoPin, 50) #50 is 50Hz pulse
servo.start(0)



def getDistance():
	GPIO.output(trig, False)
	time.sleep(0.000002)
	GPIO.output(trig, True)
	time.sleep(0.00001)
	GPIO.output(trig, False)
	
	while GPIO.input(echo)==0:
		echoStartTime=time.time()
	
	while GPIO.input(echo)==1:
		echoStopTime=time.time()
	timeElapsed=echoStopTime-echoStartTime
	distance=timeElapsed * 17150
	
	print(round(distance,2), 'cm')
	#time.sleep(0.2)
	return distance
	
def setServoAngle(angle):
	duty=angle / 18 + 2
	GPIO.output(servoPin, True)
	servo.ChangeDutyCycle(duty)
	time.sleep(1)
	GPIO.output(servoPin, False)
	servo.ChangeDutyCycle(0)

def rotateServo():
	for i in range(3):
		setServoAngle(angles[i])
		servoDistance=getDistance()
		disAtScan.append(servoDistance)
		rightDis=disAtScan.index("1")
		print(f"Right Dis =  {rightDis}")
        leftDis=disAtScan[2]
		
#start PWM
speedEnRt.start(50)
speedEnLt.start(50)

#Forward Motion 
def forward(): 
	GPIO.output(rtFwd, GPIO.HIGH)
	GPIO.output(rtRev, GPIO.LOW)
	GPIO.output(ltFwd, GPIO.HIGH)
	GPIO.output(ltRev, GPIO.LOW)
	print("Moving forward!")

#Backward Motion
def reverse():
	GPIO.output(rtFwd, GPIO.LOW)
	GPIO.output(rtRev, GPIO.HIGH)
	GPIO.output(ltFwd, GPIO.LOW)
	GPIO.output(ltRev, GPIO.HIGH)
	print("Moving backward!")

#Right Turn
def right():
	GPIO.output(rtFwd, GPIO.LOW)
	GPIO.output(rtRev, GPIO.HIGH)
	GPIO.output(ltFwd, GPIO.HIGH)
	GPIO.output(ltRev, GPIO.LOW)

#Left Turn
def left():
	GPIO.output(rtFwd, GPIO.HIGH)
	GPIO.output(rtRev, GPIO.LOW)
	GPIO.output(ltFwd, GPIO.LOW)
	GPIO.output(ltRev, GPIO.HIGH)

#Stop Motors
def stop():
	GPIO.output(rtFwd, GPIO.LOW)
	GPIO.output(rtRev, GPIO.LOW)
	GPIO.output(ltFwd, GPIO.LOW)
	GPIO.output(ltRev, GPIO.LOW)

while True:
	setServoAngle(90)
	frontDis=getDistance()
	if(frontDis < 20):
		print("Obstacle Detected")
		stop()
	rotateServo()
		
	
GPIO.cleanup()
