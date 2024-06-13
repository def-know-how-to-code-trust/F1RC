import serial
import threading
import time

ser = serial.Serial('COM5', 115200)  # open serial port
stop_reading = False  # flag to control the reading process

def start_reading():
    global stop_reading
    while not stop_reading:
        timeNow = time.time()
        line = ser.readline().decode('utf-8').strip()  # read a line from the micro:bit
        if line:  # check if line is not empty
            notLine = line.split(";")
            if len(notLine) >= 4:  # check if notLine has at least 4 elements
                try:
                    notLine[3] = int(notLine[3])
                    timedelay = (time.time() - timeNow) * 1000
                    notLine[3] = (notLine[3] + timedelay)
                    print(notLine)
                except ValueError:
                    print(f"Cannot convert {notLine[3]} to integer.")
                    exit(1)


while True:
    command = input("Enter 'start' to start reading, 'stop' to stop: ")
    if command.lower() == 'start':
        stop_reading = False
        threading.Thread(target=start_reading).start()
    elif command.lower() != 'start':
        stop_reading = True