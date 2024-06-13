import serial
import threading
import time
import logging
import os
# Get the path to the "Downloads" directory in the user's home directory
downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads")

# Specify the file path for the log file in the "Downloads" directory
log_file_path = os.path.join(downloads_dir, "serial_reader_logs.log")

# Configure logging to write logs to the specified file
logging.basicConfig(filename=log_file_path, level=logging.WARNING)

def start_reading(ser):
    global stop_reading
    while not stop_reading:
        timeNow = time.time()
        line = ser.readline().decode('utf-8').strip()  # read a line from the micro:bit
        if line:  # check if line is not empty
            notLine = line.split(";")
            if len(notLine) >= 4:  # check if notLine has at least 4 elements
                try:
                    notLine[3] = float(notLine[3])  # Convert to float instead of int
                    timedelay = (time.time() - timeNow) * 1000
                    notLine[3] += timedelay
                    print(notLine)
                except ValueError:
                    logging.warning(f"Cannot convert '{notLine[3]}' to a number.")

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
