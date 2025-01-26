import time

def toFahrenheit(celsius):
    return celsius * (9/5) + 32.0

def blinkNtimes(times, pauseSecs, ledPin):
    ledPin.value(0)
    while times > 0:
        ledPin.value(1)
        time.sleep(pauseSecs / 2)
        ledPin.value(0)
        time.sleep(pauseSecs / 2)
        times -= 1

def getTimeString():
    dyear, dmonth, dday, dhour, dmin, dsec, dweekday, dyearday = time.localtime()
    return '{:02d}/{:02d}/{:04d} {:02d}:{:02d}:{:02d}'.format(dmonth, dday, dyear, dhour, dmin, dsec)

def getTimestampString():
    return str(time.time())

def getTimeStringForFileName():
    dyear, dmonth, dday, dhour, dmin, dsec, dweekday, dyearday = time.localtime()
    return '{}-{:02d}-{}T{:02d}:{:02d}:{:02d}'.format(dyear, dmonth, dday, dhour, dmin, dsec)