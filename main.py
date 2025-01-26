import socket, onewire, ds18x20, time
import uasyncio as asyncio, urequests, ubinascii, json
from machine import Pin
import wifiTools, helper
import dht22helper as dht22
import proximitySensorHelper as hcsr04
import picoHelper as pico
import logger as log
from layout import _layoutHtml

# constants
catName = 'Czosnek'
readSensorsIntervalSec = 5
catIsInLedIntervalSec = 2
proximitySensorMaxDistanceFromTheCatMm = 300
remoteLogServerUrl = 'https://192.168.0.31:8443/'
rpiServerLogin = 'cathouse'
rpiServerPassword = 'Evergreen1-Thumping-Speckled'
base64CredentialsBytes = ubinascii.b2a_base64(rpiServerLogin + '$$$' + rpiServerPassword)
authHeaderString = 'Basic ' + base64CredentialsBytes.decode('utf-8').rstrip()
# GPIO pin numbers
prox_trig_pin_num = 5
prox_echo_pin_num = 6
ds18b20_pin_num = 1
dht22_pin_num = 0
blue_led_pin_num = 13
red_led_pin_num = 12
white_led_pin_num = 14
# DHT22 sensor readings
tempMainC = 0.0
humidityMainPerc = 0.0
tempMainF = 0.0
# DS18B20 sensor readings
tempPadC = 0.0
tempPadF = 0.0
# proximity sensor
distance_mm = 0.0
isCatIn = False
# Pico temp sensor readings
tempInternalC = 0.0
tempInternalF = 0.0
# Wi-Fi credentials
ssid = 'Pierogy'
passwrd = '%r4k3nP13rd4k3N'
# statuses
serverStarted = False
# log file
file = open('./logs/logs-{}.txt'.format(helper.getTimeStringForFileName()), "w")
log.write(file, 'Initialization...')

# proximity sensor init
prox_trig_pin = Pin(prox_trig_pin_num, Pin.OUT)
prox_echo_pin = Pin(prox_echo_pin_num, Pin.IN)
log.write(file, 'Proximity trigger pin at GPIO{}'.format(prox_trig_pin_num))
log.write(file, 'Proximity echo pin at GPIO{}'.format(prox_echo_pin_num))

# DS18B20 temp sensor init
log.write(file, 'DS18B20 temperature sensor pin at GPIO{}'.format(ds18b20_pin_num))
ds_temp_pin = Pin(ds18b20_pin_num)
ds_temp_sensor = ds18x20.DS18X20(onewire.OneWire(ds_temp_pin))
roms = ds_temp_sensor.scan()
log.write(file, 'Found {} DS18B20 devices!'.format(len(roms)))

# Raspberry PI Pico W LED pin
pico_led = Pin('LED', Pin.OUT)

# DHT22 sensor init
log.write(file, 'DHT22 temperature and humidity sensor pin at GPIO{}'.format(dht22_pin_num))
dht22_pin = Pin(dht22_pin_num)
dht22_sensor = dht22.connect(dht22_pin)

# blue LED
log.write(file, 'Blue status LED pin at GPIO{}'.format(blue_led_pin_num))
blue_led = Pin(blue_led_pin_num, Pin.OUT)

# red LED
log.write(file, 'Red status LED pin at GPIO{}'.format(red_led_pin_num))
red_led = Pin(red_led_pin_num, Pin.OUT)

# cat indicator white LED
log.write(file, 'White status LED pin at GPIO{}'.format(white_led_pin_num))
white_led = Pin(white_led_pin_num, Pin.OUT)

def send_log_to_db():
    try:
        headers = {
            "Authorization": authHeaderString,
            "Content-Type": 'application/x-www-form-urlencoded'
        }
        post_data = {
            "distanceMm": distance_mm,
            "isCatIn": isCatIn,
            "tempMainC": tempMainC,
            "humidityMainPerc": humidityMainPerc,
            "tempPadC": tempPadC,
            "tempInternalC": tempInternalC
        }
        json_string = (json.dumps(post_data)).encode()

        result = urequests.post(remoteLogServerUrl, data=json_string, headers=headers)
        
        print('{}: {}'.format(result.status_code, result.text))
        
        result.close()
    except Exception as e:
        helper.blinkNtimes(times = 3, pauseSecs = 0.1, ledPin = red_led)
        print('Error sending data to DB: ', e)

async def handle_client(reader, writer):
    # Client Connected
    request_line = await reader.readline()
    while await reader.readline() != b"\r\n":
        pass
    
    request = str(request_line, 'utf-8').split()[1]
    log.write(file, 'Request: {}'.format(request_line))    
    
    catInStateStr = 'IN' if isCatIn else 'OUT'
    response = _layoutHtml.format(catName, catInStateStr, tempMainC, tempMainF, humidityMainPerc, tempPadC, tempPadF, tempInternalC, tempInternalF)
    
    # Send the HTTP response and close the connection
    writer.write('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
    writer.write(response)
    await writer.drain()
    await writer.wait_closed()
    # Client Disconnected
    blue_led.on()
    await asyncio.sleep(0.01)
    blue_led.off()

async def readSensors():
    while True:
        # proximity sensor read
        global distance_mm, isCatIn
        distance_mm = hcsr04.read(prox_trig_pin, prox_echo_pin)
        isCatIn = distance_mm < proximitySensorMaxDistanceFromTheCatMm
        
        # DHT22 sensor read
        global tempMainC, humidityMainPerc, tempMainF
        tempMainC, humidityMainPerc = dht22.read(dht22_sensor)
        tempMainF = helper.toFahrenheit(tempMainC)

        # DS18B20 sensor read
        global tempPadC, tempPadF
        ds_temp_sensor.convert_temp()
        tempPadC = ds_temp_sensor.read_temp(roms[0])
        tempPadF = helper.toFahrenheit(tempPadC)
        
        # Pico temp sensor read
        global tempInternalC, tempInternalF
        tempInternalC = pico.readTemp()
        tempInternalF = helper.toFahrenheit(tempInternalC)
        
        catInStateStr = 'IN' if isCatIn else 'OUT'
        data_entry = 'Cat is {}, mainTemp: {:.1f}℃, mainHum: {:.1f}%, padTemp: {:.1f}℃, picoTemp: {:.1f}℃'.format(catInStateStr, tempMainC, humidityMainPerc, tempPadC, tempInternalC)
        log.write(file, data_entry)

        if serverStarted:
            send_log_to_db()
        
        pico_led.on()
        await asyncio.sleep(0.2)
        pico_led.off()
    
        await asyncio.sleep(readSensorsIntervalSec)

async def blinkIfCatIsIn():
    while True:
        if isCatIn:
            white_led.on()
        await asyncio.sleep(0.25)
        if isCatIn:
            white_led.off()
        await asyncio.sleep(catIsInLedIntervalSec)

async def heartbeat5sec():
    while True:
        if serverStarted:
            pico_led.on()
            print("5sec heartbeat")
            await asyncio.sleep(0.25)
            pico_led.off()
            await asyncio.sleep(5)

async def heartbeat2hours():
    while True:
        if serverStarted:
            print("2 hours heartbeat")
            await asyncio.sleep(7200)

async def main():
    log.write(file, 'Connecting to Wi-Fi...')
    if not wifiTools.connect(ssid, passwrd, pico_led):
        raise RuntimeError('Wi-Fi connection failed')
    
    log.write(file, 'Setting up webserver...')
    server = asyncio.start_server(handle_client, "0.0.0.0", 80)        
    asyncio.create_task(server)
    log.write(file, 'Webserver ready!')
    global serverStarted
    serverStarted = True
    
loop = asyncio.get_event_loop()
loop.create_task(readSensors())
loop.create_task(main())
loop.create_task(blinkIfCatIsIn())

try:
    loop.run_forever()
except Exception as e:
    log.write(file, 'Fatal error occured: ', e)
except KeyboardInterrupt:
    log.write(file, 'Program interrupted by the user')
finally:
    log.write(file, 'Closing program')
    file.close()