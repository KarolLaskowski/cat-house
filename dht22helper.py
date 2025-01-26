import dht

def connect(pin):
    return dht.DHT22(pin)

def read(dht22_sensor):
    # DHT22 sensor read
    dht22_sensor.measure()
    tempMainC = dht22_sensor.temperature()
    humidityMainPerc = dht22_sensor.humidity()
    return tempMainC, humidityMainPerc