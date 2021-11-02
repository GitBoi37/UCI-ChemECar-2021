from sys import getdefaultencoding
from serial import *
from time import localtime,strftime,sleep

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




def makeFileTimeBased(header):
    current_time = localtime()
    fTime= strftime('y%Y_m%m_d%d_h%H_m%M', current_time)
    fileName = f"/collected_data/event_based_data_{fTime}.csv" #name of csv generated
    print("Checking directory...")
    try:
        os.makedirs("/collected_data")
        print("Make folder to store data in \"collected data\"")
    except FileExistsError:
        # directory already exists
        print("Dir exists, continue")
        pass
<<<<<<< HEAD
    header = "input,colorTemp,lux,R,G,B"
    try:
        ser = Serial(
            port=arduino_port,
            baudrate=9600,
            timeout=2,
            xonxoff=0,
            rtscts=0,
            interCharTimeout=None
        )
    except (SerialException,FileNotFoundError):
        print("Aborting program... wrong port / port in use / nothin in port")
        sleep(4)
        sys.exit()

    print(f"Connected to Arduino port: {arduino_port}")
    

=======
    print("Creating .csv file...")
    try:
        file = open(fileName, "w")
        file.write("")
        file.write(f"{header}\n")
    except Exception:
        print("Couldn't write file and idk how exceptions work with that so you're SOL maybe don't have bad file names or something")
        if(file.closed() != True):
            file.close()
    return file



def makeFileEventBased(header):
    current_time = localtime()
    fTime= strftime('y%Y_m%m_d%d_h%H_m%M', current_time)
    fileName = f"/collected_data/event_based_data_{fTime}.csv" #name of csv generated
    print("Checking directory...")
    try:
        os.makedirs("/collected_data")
        print("Make folder to store data in \"collected data\"")
    except FileExistsError:
        # directory already exists
        print("Dir exists, continue")
        pass
>>>>>>> TestBranch
    print("Creating .csv file...")
    try:
        file = open(fileName, "w")
        file.write("")
        file.write(f"{header}\n")
    except:
        print("Couldn't write file and idk how exceptions work with that so you're SOL maybe don't have bad file names or something")
        if(file.closed() != True):
            file.close()
<<<<<<< HEAD

    print("File created!")
    i = "e"
    print("Ready to collect data! Please note that data collection is sometimes weird but that's just comm error. Simply record another data point. \nType end to end, otherwise input test name:")
    while True:
        i = input("Input: ")
        ser.flushInput()
        sleep(0.25)
=======
    return file



def collectTimeBasedData(ser):
    try:
        while(True):
            try:
                deltaT = float(input('Enter the time interval between collection in seconds: '))
                maxT = float(input("Enter the longest trial time. Type 0 for indefinite collection: "))
                break
            except Exception as e:
                print("Error in input, try again")
        
        print("Data collection time!")
        while True:  
            s_time = time.time()
            cum_time = 0
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
                file.write(f"{time.time() - s_time},{data}\n")
            except IOError as e:
                print(e)
            except TypeError(str):
                print("invalid str in")
            except SerialException:
                print("Problem collecting data from Arduino")
            except SerialTimeoutException:
                print("Connection timed out")
            while(time.time() - s_time < deltaT):
                pass
            cum_time += time.time() - s_time
            if(cum_time > maxT and maxT != 0):
                break
    except:
        print("Program interrupted, ending data collection")



def collectEventBasedData(ser):
    print("Ready to collect data! Please note that data collection is sometimes weird but that's just comm error. Simply record another data point. \nType end to end, otherwise input test name:")
    i = "e"
    while True:  
        i = input("Input: ")
>>>>>>> TestBranch
        if(i == "end"):
            print("Ending collection...")
            #close the file
            file.close()
            break
<<<<<<< HEAD
        
        try:
            #get and display data to terminal
            getData = str(ser.readline())
            print(getData)
            data = getData[0:][2:-5]
            file.write(str(i) + "," + data +"\n")
        except IOError:
            print("Error writing data")
=======
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
>>>>>>> TestBranch
        except TypeError(str):
            print("invalid str in")
        except SerialException:
            print("Problem collecting data from Arduino")
        except SerialTimeoutException:
            print("Connection timed out")

<<<<<<< HEAD
=======


if __name__ == "__main__":
    baud = 9600 #arduino uno runs at 9600 baud
    tout = 2 #timeout for serial input
    header = "input,colorTemp,lux,R,G,B"
    file = None
    mode = ""
    print("Starting up...")
    sleep(2)

    arduino_port = getPort()
    print("Connecting to serial port...")

    ser = connect(arduino_port, tout, baud)

    while(True):
        mode = input("Time or event based data collection? Enter T or E: ")
        if(mode == "T"):
            file = makeFileTimeBased(header)
            break
        elif(mode == "E"):
            file = makeFileEventBased(header)
            break
        else:
            print("Invalid input")

    print("File created!")

    if(mode == "T"):
        print("Beginnning time based data collection")
        collectTimeBasedData(ser)
    else:
        print("Beginning event based data collection")
        collectEventBasedData(ser)
>>>>>>> TestBranch
        
    if(file.closed != True):
        #close the file if not already closed
        file.close()