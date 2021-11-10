from sys import getdefaultencoding
from serial import *
from time import localtime,strftime,sleep
import pathlib

def connect(arduino_port, tout, baud):
    try:
        ser = Serial(
            port=arduino_port,
            baudrate=baud,
            timeout=tout,
            xonxoff=0,
            rtscts=0,
            interCharTimeout=None
        )
    except (SerialException,FileNotFoundError):
        print("Aborting program... wrong port / port in use / nothin in port")
        sleep(4)
        sys.exit()
    print(f"Connected to Arduino port: {arduino_port}")
    return ser   



def getPort():
    while(True):
        try:
            portIn = input("What is the number of the port being used? It is the com port selected in the arduino IDE. Enter the number only: ")
            arduino_port = f"COM{portIn}"
            break
        except Exception as e:
            print("Unknown error")
            print(e)
    return arduino_port




def makeFileTimeBased(header, location, name):
    current_time = localtime()
    fTime= strftime('y%Y_m%m_d%d_h%H_m%M', current_time)
    fileName = f"{location}/{name}_time_based_data_{fTime}.csv" #name of csv generated
    print("Checking directory...")
    try:
        os.makedirs(location)
        print(f"Make folder to store data in {location}")
    except Exception as e:
        # directory already exists
        print(e)
        pass

    print("Creating .csv file...")
    try:
        file = open(fileName, "w")
        file.write("")
        file.write(f"{header}\n")
        print(f"file created at {os.path.realpath(file.name)}")
        #print(f"File created at {print(pathlib.Path(file).parent.absolute())}!")
    except Exception as e:
        print(e)
        if(file.closed   != True):
            file.close()
    return file



def makeFileEventBased(header, location, name):
    current_time = localtime()
    fTime= strftime('y%Y_m%m_d%d_h%H_m%M', current_time)
    fileName = f"{location}/{name}_event_based_data_{fTime}.csv" #name of csv generated
    print("Checking directory...")
    try:
        os.makedirs(location)
        print(f"Make folder to store data in \"{location}\"")
    except Exception as e:
        # directory already exists
        print(e)
        pass
    print("Creating .csv file...")
    try:
        file = open(fileName, "w")
        file.write("")
        file.write(f"{header}\n")
        print(f"file created at {os.path.realpath(file.name)}")
        #print(f"File created at {print(pathlib.Path(file).parent.absolute())}!")
    except Exception as e:
        print(e)
        if(file.closed() != True):
            file.close()

    
    return file



def collectTimeBasedData(ser, file):
    deltaT = ""
    maxT = ""
    try:
        while(True):
            try:
                deltaT = float(input('Enter the time interval between collection in seconds: '))
                maxT = float(input("Enter the longest trial time. Type 0 for indefinite collection: "))
                break
            except Exception as e:
                print("Error in input, try again")
        
        print("Data collection time!")
        abs_start = time.time()
        while True:  
            loopStart = time.time()
            ser.flushInput()
            try:
                while(True):
                    #get and display data to terminal
                    ser.flushInput()
                    getData = str(ser.readline())
                    dataLen= len(getData[0:].split(","))
                    #len3 = len(getData.split(","))
                    #print(f"Raw data, len 1, len2, len 3: {getData} , {len(getData[0:])} , {len2} , {len3}")
                    data = getData[0:][2:-5]
                    print(f"Data: {data}")
                    if(dataLen < 6):
                        print("invalid data point, remeasuring...")
                    else:
                        break
                delta = time.time() - loopStart
                if(delta < deltaT):
                    sleep(deltaT - delta)

                timeSinceStart = time.time() - abs_start
                file.write(f"{timeSinceStart},{data}\n")
                if(timeSinceStart > maxT):
                    break

                
            except IOError as e:
                print(e)
            except TypeError(str):
                print("invalid str in")
            except SerialException:
                print("Problem collecting data from Arduino")
            except SerialTimeoutException:
                print("Connection timed out")
            
    except:
        print("Program interrupted, ending data collection")



def collectEventBasedData(ser, file):
    print("Ready to collect data! Please note that data collection is sometimes weird but that's just comm error. Simply record another data point. \nType end to end, otherwise input test name:")
    i = "e"
    while True:  
        i = input("Input: ")
        if(i == "end"):
            print("Ending collection...")
            #close the file
            file.close()
            break
        
        try:
            while(True):
                #get and display data to terminal
                ser.flushInput()
                sleep(0.25)
                getData = str(ser.readline())
                len2 = len(getData[0:].split(","))
                len3 = len(getData.split(","))
                print(f"Raw data, len 1, len2, len 3: {getData} , {len(getData[0:])} , {len2} , {len3}")
                data = getData[0:][2:-5]
                if(len2 < 6):
                    print("invalid point, remeasuring...")
                else:
                    break
            file.write(str(i) + "," + data +"\n")
        except IOError as e:
            print(e)
        except TypeError(str):
            print("invalid str in")
        except SerialException:
            print("Problem collecting data from Arduino")
        except SerialTimeoutException:
            print("Connection timed out")

def getFile():
    file = None
    mode = ""
    baseHead = "Color Temperature,Lux,Clear,Raw Red,Raw Green,Raw Blue,R,G,B"
    while(True):
        mode = input("Time or event based data collection? Enter T or E: ")
        name = input("Enter test name to append to file name: ")
        if(mode == "T"):
            header = f"time(s),{baseHead}"
            file = makeFileTimeBased(header, location, name)
            break
        elif(mode == "E"):
            header = f"input,{baseHead}"
            file = makeFileEventBased(header, location, name)
            break
        else:
            print("Invalid input")
    return (file,mode)

if __name__ == "__main__":
    baud = 9600 #arduino uno runs at 9600 baud
    tout = 2 #timeout for serial input
    location = "data"
    file = None
    mode = ""
    print("Starting up...")
    sleep(2)

    arduino_port = getPort()
    print("Connecting to serial port...")

    ser = connect(arduino_port, tout, baud)
    (file, mode) = getFile()

    if(mode == "T"):
        print("Beginnning time based data collection")
        collectTimeBasedData(ser, file)
    else:
        print("Beginning event based data collection")
        collectEventBasedData(ser, file)
    if(file.closed != True):
        #close the file if not already closed
        file.close()
