#!/usr/bin/env python
import RPi.GPIO as GPIO
import dht11
import datetime
import time

LightOnSecs = 10

TempHumidityPin = 7
SmartThingsPin = 11 # pin11 smartthings controlled pin --- GPIO-17
LedPin = 13    # pin13 --- led GPIO-
MovPin = 12    # pin12 --- movement sensor GPIO-18
LightPin = 15 # pin15 --- light sensor GPIO-22

data = []

lastOnTime = datetime.datetime(2000, 1, 1, 0, 0)

def setup():
        GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
        GPIO.setup(SmartThingsPin, GPIO.OUT)
        GPIO.setup(LedPin, GPIO.OUT)   # Set LedPin's mode is output
        GPIO.setup(MovPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Set pins mode is input, and pull up to high level(3.3V)
        GPIO.setup(LightPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.output(LedPin, GPIO.HIGH) # Set LedPin high(+3.3V) to off led

        instance = dht11.DHT11(TempHumidityPin)
             
def swMov(ev=None):
        global lastOnTime

        currentTime = datetime.datetime.utcnow()
        lastOnTime = currentTime

        isLightOff = GPIO.input(LightPin)
        if isLightOff:
                print 'Moving: Its dark!'
                lightOn()
                return

        print 'Moving: Its light! I do not need to do anything'

def swLight(ev=None):
        isLightOff = GPIO.input(LightPin)
        if not isLightOff:
                print 'Its light!'
                lightOff()

def lightOff():
        print 'Light OFF'
        lastOnTime = datetime.datetime(2000, 1, 1, 0, 0)
        GPIO.output(LedPin, GPIO.HIGH)

def lightOn():
        print 'Light ON'
        lastOnTime = datetime.datetime.utcnow()
        GPIO.output(LedPin, GPIO.LOW)
        
def bin2dec(string_num):
        return str(int(string_num, 2))

def tempAndHumidity():
        result = instance.read()
        if result.is_valid():
                print("Last valid input: " + str(datetime.datetime.now()))
                print("Temperature: %d C" % result.temperature)
                print("Humidity: %d %%" % result.humidity)
        else:
                print "oops"
        # GPIO.setup(TempHumidityPin,GPIO.OUT)
        # GPIO.output(TempHumidityPin,GPIO.HIGH)
        # time.sleep(0.025)
        # GPIO.output(TempHumidityPin,GPIO.LOW)
        # time.sleep(0.02)
        
        # GPIO.setup(TempHumidityPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # for i in range(0,500):
        # 	data.append(GPIO.input(TempHumidityPin))
        # bit_count = 0
        # tmp = 0
        # count = 0
        # HumidityBit = ""
        # TemperatureBit = ""
        # crc = ""
        
        # try:
	#         while data[count] == 1:                        
	# 	        tmp = 1
	# 	        count = count + 1
                
        #         for i in range(0, 32):
	# 	        bit_count = 0
 
	# 	        while data[count] == 0:
	# 		        tmp = 1
	# 		        count = count + 1
 
	# 	        while data[count] == 1:
	# 		        bit_count = bit_count + 1
	# 		        count = count + 1
 
	# 	        if bit_count > 3:
	# 		        if i>=0 and i<8:
	# 			        HumidityBit = HumidityBit + "1"
	# 		        if i>=16 and i<24:
	# 			        TemperatureBit = TemperatureBit + "1"
	# 	        else:
	# 		        if i>=0 and i<8:
	# 			        HumidityBit = HumidityBit + "0"
	# 		        if i>=16 and i<24:
	# 			        TemperatureBit = TemperatureBit + "0"
 
        # except Exception, e:
        #         print "ERR_RANGE - Humidity or Temperature error"
	#         print e
	#         exit(0)

        # Humidity = bin2dec(HumidityBit)
        # print "Humidity is: " +  Humidity

        # Temperature = bin2dec(TemperatureBit)
        # print "Temperature is: " + Temperature

        # try:
	#         for i in range(0, 8):
	# 	        bit_count = 0
 
	# 	        while data[count] == 0:
	# 		        tmp = 1
	# 		        count = count + 1
 
	# 	        while data[count] == 1:
	# 		        bit_count = bit_count + 1
	# 		        count = count + 1
 
	# 	        if bit_count > 3:
	# 		        crc = crc + "1"
	# 	        else:
	# 		        crc = crc + "0"
        # except Exception, e:
        #         print "ERR_RANGE - crc error"
	#         print e

        # if int(Humidity) + int(Temperature) - int(bin2dec(crc)) == 0:
	#         print "Humidity:"+ Humidity +"%"
	#         print "Temperature:"+ Temperature +"C"
        # else:
	#         print "ERR_CRC"

def loop():
        GPIO.add_event_detect(MovPin, GPIO.FALLING, callback=swMov, bouncetime=200) # wait for falling and set bouncetime to prevent the callback function from being called multiple times when the button is pressed
        GPIO.add_event_detect(LightPin, GPIO.FALLING, callback=swLight, bouncetime=200)
        while True:
                smartOn = GPIO.input(SmartThingsPin)
                if smartOn:
                        print 'SmartThings requests light is ON'
                        lightOn()
                else:
                        currentTime = datetime.datetime.utcnow()
                        elapsedTime = currentTime - lastOnTime

                        print 'Elapsed time: ' + str(elapsedTime)
                        if elapsedTime.total_seconds() > LightOnSecs:
                                lightOff()

                tempAndHumidity()
                
                time.sleep(1)   # Don't do anything

def destroy():
        GPIO.output(LedPin, GPIO.HIGH)     # led off
        GPIO.cleanup()                     # Release resource

if __name__ == '__main__':     # Program start from here
        setup()
        try:
                loop()
        except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
                destroy()
