import time, helper

def write(file, text):
    time_str = helper.getTimeString()
    file.write(time_str + ': ' + text + '\n')
    print(text)
