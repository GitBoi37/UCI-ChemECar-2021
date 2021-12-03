from serial import *
from time import localtime,strftime,sleep
import json

def connect(arduino_port, tout, baud):
    print("Connecting to serial port...")
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


def cleanup(file):
    try:
        if(file != None):
            if(file.closed != True):
                #close the file if not already closed
                file.close()
    except Exception as e:
        print(e)




def readConfig(config_file):
    with open(config_file) as json_data_file:
        data = json.load(json_data_file)
    header = ""
    probe = data["probe"]
    timebased = data["time based"]
    deltaT = data["deltaT"]
    maxT = data["maxT"]
    measureTimeToValue = data["measureTimeToValue"]
    headings = data["headings"]
    if(measureTimeToValue == "Y"):
        try:
            header = headings["measureTimeToValue"][probe]
        except Exception as e:
            print(f"Error readings config in the measuretimetovalue section:\n{e}")
    elif(measureTimeToValue == "N"):
        try:
            header = headings["noMeasureTimeToValue"][probe][timebased]
        except Exception as e:
            print(f"Error reading config in the nomeasuretimetovalue section:\n{e}")
    else:
        print("unrecognized measuretimetovalue value, must be Y or N")
        sleep(1)
        sys.exit()
    return (header,probe,timebased, deltaT, maxT, measureTimeToValue)


def makeFile(header, location):
    file = None
    while(True):
        name = input("Enter test name to append to file name: ")
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
        except Exception as e:
            print(e)
            if(file != None):
                if(file.closed() != True):
                    file.close()

        return file


def collectTimeBasedColorData(ser, file, deltaT, maxT):
    try:
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


def collectTimeBasedConductivityData(ser, file, deltaT, maxT):
    try:
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



def collectEventBasedColorData(ser, file):
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
                #len3 = len(getData.split(","))
                #print(f"Raw data, len 1, len2, len 3: {getData} , {len(getData[0:])} , {len2} , {len3}")
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

def collectEventBasedConductivityData(ser, file):
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
                len2 = len(getData[0:].split(",")) #the [0:] doesnt do anything but if you wanted to filter out first two do [3:]
                #len3 = len(getData.split(","))
                #print(f"Raw data, len 1, len2, len 3: {getData} , {len(getData[0:])} , {len2} , {len3}")
                data = getData[0:][2:-5] #same thing as above, [2:-5] actually does some filtering im not sure why anymore
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


def measureColorTime(ser, file):
    print("this function is not implemented yet... sorry about that...")

def measureConductivityTime(ser, file, deltaT, maxT):
    # IF THERE IS A PROBLEM THIS IS PROBABLY WRONG
    checkLen = 3
    print("This function is also not implemented fully yet lol... oops")
    sValue = None
    while(True):
        ser.flushInput()
        sleep(0.25)
        getData = str(ser.readline())
        try:
            len2 = len(getData)
            if(len2 < checkLen):
                print("invalid start point, remeasuring")
            else:
                sValue = getData[0:][2:-5]
                break
        except Exception as e:
            print("not having a good time collecting data")
            print(e)
        
    i = "e"
    #outer loop for taking multiple trials
    while(True):
        i = input("Input value to measure the time until it reaches that or end to end: ")
        if(i == "end"):
            print("Ending collection...")
            break
        print("\nUse Ctrl^C to end while collecting data")
        try:
            print("Data collection time!")
            abs_start = time.time()
            eValue = ""
            while True:  
                loopStart = time.time()
                ser.flushInput()
                try:
                    while(True):
                        #get and display data to terminal
                        ser.flushInput()
                        getData = str(ser.readline())
                        try:
                            dataLen= len(getData)
                            eValue = getData[2:-5] #starting from second position, go to end -5 from back, not sure if this works
                            if(dataLen < checkLen):
                                print("invalid data point, remeasuring...")
                            else:
                                break
                        except Exception as e:
                            print("not having a good time collecting data")
                            print(e)
                    #measure time passed and do corrections to make deltaT epic
                    delta = time.time() - loopStart
                    if(delta < deltaT):
                        sleep(deltaT - delta)
                    timeSinceStart = time.time() - abs_start
                    
                    #if time elapsed passed maxT then it don't matta
                    if(timeSinceStart > maxT):
                        break
                    if(float(eValue > float(i))):
                        break
                except IOError as e:
                    print(e)
                except TypeError(str):
                    print("invalid str in")
                except SerialException:
                    print("Problem collecting data from Arduino")
                except SerialTimeoutException:
                    print("Connection timed out")
            file.write(f"{timeSinceStart},{sValue},{eValue},{str(float(eValue) - float(sValue))}\n")   
        except KeyboardInterrupt:
            print("Program interrupted, ending data collection")
        


if __name__ == "__main__":
    baud = 9600 #arduino uno runs at 9600 baud
    tout = 2 #timeout for serial input
    location = "data" #folder location of collected data
    file = None
    mode = ""
    print("Starting up...")
    sleep(1)

    arduino_port = getPort()

    ser = connect(arduino_port, tout, baud)

    (header,probe, timebased, deltaT, maxT, measureTime) = readConfig("data_collection_config.json")
    
    file = makeFile(header, location)
    #I separated out collection of color and conductivity data even though the process is very similar since I didn't want to do some weird thing
    #and for that to end up not working, plus the implementation of the data collection could change and then I would need to figure another thing
    #out so it would be easier to just separate things out. Right now they are the exact same and I need to test how this works with the conductivity
    #probe but will need to revise this at a later hour when I can bust those babies out
    if(measureTime == "N"):
        if(timebased == "Y"):
            if(probe == "color"):
                print("Beginnning time based color data collection")
                collectTimeBasedColorData(ser, file, deltaT, maxT)
            else:
                print("Beginning time based conductivity data collection")
                collectTimeBasedConductivityData(ser, file, deltaT, maxT)
        else:
            if(probe == "color"):
                print("Beginning event based color data collection")
                collectEventBasedColorData(ser, file, deltaT, maxT)
            else:
                print("Beginning event based conductivitiy data collection")
                collectEventBasedConductivityData(ser,file, deltaT, maxT)
    else:
        #insert functions to measure time it takes to get to a certain value here
        if(probe == "color"):
            print("It's measuring the time it takes to get to a value with the color sensor o'clock!")
            measureColorTime(ser, file)
        else:
            print("It's measuring the time it takes to get to  a value with the conductivity probe o'clock!")
            measureConductivityTime(ser, file)

    try:
        if(file != None):
            cleanup(file)
    except Exception as e:
        #I don't know what could go wrong here but yanever know, I'm bad at coding so it'll probably happen
        print("Something went wrnog trying to cleanup, but it's likely not catastrophic, have a great day!")
        print(e)