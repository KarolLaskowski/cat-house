from machine import time_pulse_us
import time

SOUND_SPEED=340
TRIG_PULSE_DURATION_US=10

def read(prox_trig_pin, prox_echo_pin):
    # proximity sensor read
    prox_trig_pin.value(0)
    time.sleep_us(5)
    prox_trig_pin.value(1)
    time.sleep_us(TRIG_PULSE_DURATION_US)
    prox_trig_pin.value(0)
    
    ultrason_duration = time_pulse_us(prox_echo_pin, 1, 30000)
    return (SOUND_SPEED * ultrason_duration / 20000) * 10