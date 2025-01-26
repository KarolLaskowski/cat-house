from machine import Pin
import network, time
import helper

STAT_IDLE = 0
STAT_GOT_IP = 3
awaitConnectionTimeoutSec = 40

def connect(ssid, passwrd, ledPin):
    maxWaitSecs = awaitConnectionTimeoutSec
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, passwrd)

    while maxWaitSecs > 0:
        if wlan.status() < STAT_IDLE or wlan.status() >= STAT_GOT_IP:
            break
        maxWaitSecs -= 1
        print('Waiting for connection...')
        ledPin.toggle()
        time.sleep(1)

    if wlan.status() == STAT_GOT_IP:
        times = 5
        pauseSecs = 0.2
        helper.blinkNtimes(times, pauseSecs, ledPin)
        print('Connected to Wi-Fi!')
        status = wlan.ifconfig()
        print('IP = ' + status[0])
        return True
    else:
        ledPin.value(1)
        pauseSecs = 10
        time.sleep(pauseSecs / 2)
        ledPin.value(0)
        raise RuntimeError('Network connection failed')

