import RPi.GPIO as GPIO
import dht11

TempHumidityPin = 7

GPIO.setmode(GPIO.BOARD)

instance = dht11.DHT11(TempHumidityPin)

result = instance.read()
if result.is_valid():
  #  print("Last valid input: " + str(datetime.datetime.now()))
  #  print("Temperature: %d C" % result.temperature)
 #   print("Humidity: %d %%" % result.humidity)
    print result.temperature