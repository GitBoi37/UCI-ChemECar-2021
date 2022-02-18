from calendar import TUESDAY
from serial import *
from time import localtime,strftime,sleep
import json

def connect(arduino_port, tout, baud):
    print(f"Connecting to serial port {arduino_port}")
    try:
        ser = Serial(
            port=arduino_port,
            baudrate=baud,
            timeout=tout,
            xonxoff=0,
            rtscts=0,
            interCharTimeout=None
        )
    
    except Exception as e:
        print("Aborting program... wrong port / port in use / nothin in port")
        print(e)
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
    baud = data["baud"]
    timebased = data["time based"]
    deltaT = float(data["deltaT"])
    maxT = float(data["maxT"])
    arduino_port = "COM" + data["COM port"]
    measureTimeToValue = data["measure time to endpoint"]
    headings = data["headings"]
    conductivityIncrease = data["does conductivity increase or decrease"]
    append = data["to append to file name"]
    if(measureTimeToValue == "Y"):
        try:
            header = headings["time to endpoint"][probe]
        except Exception as e:
            print(f"Error readings config in the 'time to endpoint' section:\n{e}")
    elif(measureTimeToValue == "N"):
        try:
            header = headings["value over time or event"][probe][timebased]
        except Exception as e:
            print(f"Error reading config in the 'value over time or event' section:\n{e}")
    else:
        print("unrecognized measuretimetovalue value, must be Y or N")
        sleep(1)
        sys.exit()
    return (header,probe,timebased, deltaT, maxT, measureTimeToValue, conductivityIncrease, baud, arduino_port, append)


def makeFile(header, location, append):
    file = None
    while(True):
        name = input("Enter test name to append to file name: ")
        current_time = localtime()
        fTime= strftime('y%Y_m%m_d%d_h%H_m%M', current_time)
        if(append != ""):
            fileName = f"{location}/{name}_{append}_data_{fTime}.csv" #name of csv generated
        else:
            fileName = f"{location}/{name}_{append}_data_{fTime}.csv" #name of csv generated
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
    maxT = float(maxT)
    deltaT = float(deltaT)
    try:
        print("Initiating time based conductivity data collection sequence")
        abs_start = time.time()
        while True:  
            loopStart = time.time()
            ser.flushInput()
            try:
                while(True):
                    #get and display data to terminal
                    ser.flushInput()
                    rawData = str(ser.readline())
                    print(f"Raw data: {rawData}", end="  |  ")
                    dataLen= len(rawData[0:].split(","))
                    print(f"Length of data: {dataLen}", end="  |  ")
                    #len3 = len(getData.split(","))
                    #print(f"Raw data, len 1, len2, len 3: {getData} , {len(getData[0:])} , {len2} , {len3}")
                    data = rawData[0:][2:-5]
                    print(f"Data: {data}", end = "  |  ")
                    if(dataLen != 1):
                        print("invalid data point, remeasuring...")
                    else:
                        break


                delta = time.time() - loopStart
                if(delta < float(deltaT)):
                    sleep(deltaT - delta)

                timeSinceStart = time.time() - abs_start
                file.write(f"{timeSinceStart},{data}\n")
                print(f"Wrote to file: {timeSinceStart},{data}")
                if(timeSinceStart > maxT):
                    break


            except Exception as e:
                print(e)

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

def measureConductivityTime(ser, file, deltaT, maxT, conductivityIncrease): 
    maxT = float(maxT)
    deltaT = float(deltaT)
    
    #outer loop for multiple trials
    while(True):
        timeSinceStart = 0
        data = ""
        s = True
        sValue = 0
        try:
            endpt = float(input("Enter the value to end data collection: "))
            abs_start = time.time()
            #loop to handle data collection / processing
            while True:  
                loopStart = time.time()
                ser.flushInput()
                try:
                    #get and display data to terminal
                    while(True):
                        ser.flushInput()
                        rawData = str(ser.readline())
                        print(f"Raw data: {rawData}", end="  |  ")
                        dataLen= len(rawData[0:].split(","))
                        print(f"Length of data: {dataLen}", end="  |  ")
                        #len3 = len(getData.split(","))
                        #print(f"Raw data, len 1, len2, len 3: {getData} , {len(getData[0:])} , {len2} , {len3}")
                        data = rawData[0:][2:-5]
                        print(f"Data: {data}", end = "  |  ")
                        if(dataLen != 1):
                            print("invalid data point, remeasuring...")
                        else:
                            print("Valid")
                            break
                    
                    #collected data, synchronize with time step
                    delta = time.time() - loopStart
                    if(delta < float(deltaT)):
                        sleep(deltaT - delta)
                    
                    if(s):
                        sValue = data
                        s = False
                    
                    if(conductivityIncrease == "increase"):
                        if(float(data) > endpt):
                            break
                    else:
                        if(float(data) < endpt):
                            break

                    #quit if max time exceeded
                    timeSinceStart = time.time() - abs_start
                    if(timeSinceStart > maxT):
                        break

                except Exception as e:
                    print(e)
            file.write(f"{timeSinceStart},{sValue},{data},{str(float(data) - float(sValue))}\n")   
            print(f"Wrote to file: {timeSinceStart},{sValue},{data},{str(float(data) - float(sValue))}\n")

        except:
            print("Program interrupted, ending data collection")
            break
        

'''
too much work

def editConfig(config_file):
    with open(config_file) as json_data_file:
        data = json.load(json_data_file)
    
    print(data)
'''        


if __name__ == "__main__":
    baud = 0 #arduino uno runs at 9600 baud, placeholder value
    tout = 2 #timeout for serial input
    location = "data" #folder location of collected data
    file = None
    mode = ""
    config_file = "data_collection_config.json"
    
    (header,probe, timebased, deltaT, maxT, measureTime,conductivityIncrease, baud, arduino_port, append) = readConfig(config_file)

    # arduino_port = getPort()
            
    ser = connect(arduino_port, tout, baud)
    
    print("To exit at any time, press CTRL + C")
    while(True):
        try:

            
            file = makeFile(header, location, append)
            
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
                        collectEventBasedColorData(ser, file)
                    else:
                        print("Beginning event based conductivitiy data collection")
                        collectEventBasedConductivityData(ser,file)
            else:
                #functions to measure time it takes to get to a certain value here
                if(probe == "color"):
                    print("It's measuring the time it takes to get to a value with the color sensor o'clock!")
                    measureColorTime(ser, file, deltaT, maxT)
                else:
                    print("It's measuring the time it takes to get to  a value with the conductivity probe o'clock!")
                    measureConductivityTime(ser, file, deltaT, maxT, conductivityIncrease)
        except KeyboardInterrupt:
            i = input("Y to exit, anything else to start over")
            if(i == "Y"):
                print("cleaning up and exiting")
                try:
                    if(file != None):
                        cleanup(file)
                except Exception as e:
                    #I don't know what could go wrong here but yanever know, I'm bad at coding so it'll probably happen
                    print("Something went wrnog trying to cleanup, but it's likely not catastrophic, have a great day!")
                    print(e)
                finally:
                    break
            else:
                print("Starting over")