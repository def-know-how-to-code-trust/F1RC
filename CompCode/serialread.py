import serial
import threading
import time

def start_reading(ser):
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

def user_input():
    global stop_reading
    stop_reading = False  # flag to control the reading process
    ser = None
    while True:
        try:
            startCommand = input("Enter a port number (Go to Device Manager and find USB Serial Device under USB Port, E.g. COM5):")
            ser = serial.Serial('COM'+str(startCommand), 115200)  # open serial port1
        except IOError:
            print("Port could not be opened try another port")
        else:
            print("Device Found")
            break

    threading.Thread(target=start_reading, args=(ser,)).start()  # start reading in a separate thread

    while True:
        command = input("Enter 'stop' to stop: ")
        if command.lower() == 'stop':
            stop_reading = True
            break

# Start the user_input function in a separate thread
threading.Thread(target=user_input).start()
