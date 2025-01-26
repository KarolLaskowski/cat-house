from machine import ADC

def readTemp():
    pico_adc = ADC(4)
    adc_value = pico_adc.read_u16()
    volt = (3.3/65535) * adc_value
    return 27 - (volt - 0.706)/0.001721