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




def makeFileTimeBased(header, location):
    current_time = localtime()
    fTime= strftime('y%Y_m%m_d%d_h%H_m%M', current_time)
    fileName = f"{location}/time_based_data{fTime}.csv" #name of csv generated
    print("Checking directory...")
    try:
        os.makedirs(location)
        print(f"Make folder to store data in {location}")
    except Exception as e:
        # directory already exists
        print(e)
        pass
    header = "input,colorTemp,lux,R,G,B"

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



def makeFileEventBased(header, location):
    current_time = localtime()
    fTime= strftime('y%Y_m%m_d%d_h%H_m%M', current_time)
    fileName = f"{location}/event_based_data_{fTime}.csv" #name of csv generated
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
        cum_time = 0
        while True:  
            s_time = time.time()
            print("s_time" + str(s_time))
            ser.flushInput()
            sleep(0.1)
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
                        print("invalid data point, remeasuring...")
                    else:
                        break
                delta = time.time() - s_time
                print("delta" + str(delta))
                if(delta < deltaT):
                    sleep(deltaT - delta)
                print("cum_time" + str(cum_time))
                cum_time += deltaT
                file.write(f"{cum_time},{data}\n")
                if(cum_time > maxT):
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



if __name__ == "__main__":
    baud = 9600 #arduino uno runs at 9600 baud
    tout = 2 #timeout for serial input
    location = "data"
    header = "input,colorTemp,lux,R,G,B"
    file = None
    mode = ""
    print("Starting up...")
    sleep(2)

    arduino_port = getPort()
    print("Connecting to serial port...")

    ser = connect(arduino_port, tout, baud)

    '''
    try:
        current_time = localtime()
        fTime= strftime('y%Y_m%m_d%d_h%H_m%M', current_time)
        fileName = f"{location}/event_based_data_{fTime}.csv"
        file = open(fileName, "w")
        file.write("")
        file.write(f"{header}\n")
    except Exception as e:
        print(e)
    '''

    while(True):
        mode = input("Time or event based data collection? Enter T or E: ")
        if(mode == "T"):
            file = makeFileTimeBased(header, location)
            break
        elif(mode == "E"):
            file = makeFileEventBased(header, location)
            break
        else:
            print("Invalid input")
    

    if(mode == "T"):
        print("Beginnning time based data collection")
        collectTimeBasedData(ser, file)
    else:
        print("Beginning event based data collection")
        collectEventBasedData(ser, file)
    if(file.closed != True):
        #close the file if not already closed
        file.close()
