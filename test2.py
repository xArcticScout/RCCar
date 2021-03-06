from gpiozero import DigitalOutputDevice, InputDevice, LED, PWMLED
from time import sleep, time
from gpiozero import MCP3002

# establish connection to the line sensor on channel zero of the MCP3002
sensor = MCP3002(0)  # import the necessary libraries.

# establish motor pins
right = LED(14)
left = LED(15)
forward = PWMLED(18)
reverse = PWMLED(23)

stopDistance = 20

mode = "forward"


# functions to simplify driving commands
def leftSteer():
    left.on()
    right.off()


def rightSteer():
    right.on()
    left.off()


def forwardDrive(speed, time):
    forward.value = speed
    reverse.off()
    sleep(time)
    stop()


def reverseDrive(speed, time):
    reverse.value = speed
    forward.off()
    sleep(time)
    stop()


def stop():
    forward.off()
    reverse.off()


def straightSteer():
    left.off()
    right.off()


# variables associated with pin numbers to connect distance sensor

triggerPin = 20
echoPin = 26

trigger = DigitalOutputDevice(triggerPin)
echo = InputDevice(echoPin)


# function that measures the distance of an obstacle from the HC-SRO4 sensor

def distance():
    trigger.off()
    sleep(0.1)
    trigger.on()
    sleep(0.00001)
    trigger.off()
    testStart = time()
    pulseStart = 0
    while echo.is_active == False:
        pulseStart = time()
        if time() - testStart > 1:
            print ("Sensor Failed")
            pulseStart = 0
            break
    pulseEnd = pulseStart + 1
    while echo.is_active == True:
        pulseEnd = time()

    pulseDuration = pulseEnd - pulseStart
    distance = pulseDuration * 17150
    distance = round(distance, 2)
    print ("Distance:", distance, "cm")
    return distance


# function to identify and avoid obstacles

def obstacle():
    while True:
        if mode == "forward":
            dist = distance()
            if dist > stopDistance:
                forward.value = 0.7
                reverse.off()
            else:
                mode = "reverse"
        if mode == "reverse":
            stop()
            sleep(0.5)
            rightSteer()
            reverseDrive(0.7, 0.75)
            sleep(0.25)
            leftSteer()
            forwardDrive(0.7, 0.75)
            straightSteer()
            mode = "forward"


def line():
    while True:
        forward.value = 0.7
        reverse.off()
        if sensor.value < 0.5:
            leftSteer()
        else:
            rightSteer()
