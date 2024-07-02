import serial
import threading
import time
import logging
import os
import csv
# Get the path to the "Downloads" directory in the user's home directory
downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads")

# Specify the file path for the log file in the "Downloads" directory
log_file_path = os.path.join(downloads_dir, "serial_reader_logs.log")
# Configure logging to write logs to the specified file
#logging.basicConfig(level=logging.WARNING)

def start_reading(ser,sessionDirectory):
    global stop_reading
    if sessionDirectory!="" or sessionDirectory!=None:
        print("session directory is not empty: ", sessionDirectory)
        with open(os.path.join(sessionDirectory,"telemetry.csv"),"a",newline="") as file:
            writer=csv.writer(file)
            while not stop_reading:
                timeNow = time.time()
                line = ser.readline().decode('utf-8').strip()  # read a line from the micro:bit
                if line:  # check if line is not empty
                    notLine = line.split(";")
                    if len(notLine) == 3:  # check if notLine has equal to 5 elements
                        print(notLine)
                        try:
                            float(notLine[0])
                            float(notLine[1])
                            float(notLine[2])
                        except ValueError as e:
                            logging.error("An error occurred: $s",notLine)
                        else:
                            speed=float(notLine[0])
                            yAccel=float(notLine[1])
                            heading=float(notLine[2])
                            timestamp=time.time()
                            
                            
                            #write the data to the file
                            writer.writerow([speed,yAccel,heading,timestamp])
                    print(notLine)
    else:
        print("sessionDirectory is empty")                          
# 

def user_input():
    global stop_reading
    stop_reading = False  # flag to control the reading process
    ser = None
    sessionDirectory= None
    while True:
        try:
            portNo = input("Enter a port number (Go to Device Manager and find USB Serial Device under USB Port, E.g. COM5):")
            ser = serial.Serial('COM'+str(portNo), 115200)  # open serial port1

        except IOError:
            print("Port could not be opened try another port")
        else:
            print("Device Found")
            break

    while True:
            folderDirectory=input("Sessions Folder Path? (Stores a folder containing session data at this path you specify): ")
            if os.path.exists(folderDirectory):
                sessionDirectory=folderDirectory+"\\"+"session_"+str(time.time())
                os.mkdir(sessionDirectory)
                with open(os.path.join(sessionDirectory,"telemetry.csv"),"w",newline="",) as file:
                    header=["x_accel", "y_accel", "z_accel","strength_accel","speed", "heading","timestamp"]
                    writer = csv.writer(file)
                    writer.writerow(header)
                logging.basicConfig(filename=sessionDirectory+"//"+"log", level=logging.WARNING)
                break
            else:
                print("Directory does not exist. Try again...")

    threading.Thread(target=start_reading, args=(ser,sessionDirectory,)).start()  # start reading in a separate thread

    while True:
        command = input("Enter 'stop' to stop: ")
        if command.lower() == 'stop':
            stop_reading = True
            break

# Start the user_input function in a separate thread
threading.Thread(target=user_input).start()
