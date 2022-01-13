from serial import *
from time import localtime,strftime,sleep
import json

def connect(arduino_port, tout, baud):
    print(f"Connecting to serial port {arduino_port}")
    ser = Serial(
        port=arduino_port,
        baudrate=baud,
        timeout=tout,
        xonxoff=0,
        rtscts=0,
        interCharTimeout=None
    )
    return ser   

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
    deltaT = data["deltaT"]
    maxT = data["maxT"]
    arduino_port = "COM" + data["COM port"]
    measureTimeToValue = data["measure time to endpoint"]
    headings = data["headings"]
    conductivityIncrease = data["does conductivity increase or decrease"]
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
    return (header,probe,timebased, deltaT, maxT, measureTimeToValue, conductivityIncrease, baud, arduino_port)


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


def collectTimeBasedConductivityData(ser, file, deltaT, maxT):
    maxT = maxT
    deltaT = deltaT
    try:
        print("Time Based Conducitivity Data collection time!")
        abs_start = time.time()
        while True:  
            print("in outside loop")
            loopStart = time.time()
            ser.flushInput()
            try:
                while(True):
                    print("in inside loop")
                    #get and display data to terminal
                    ser.flushInput()
                    print("flushed")
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
                print(f"Wrote: {timeSinceStart},{data}")
                if(timeSinceStart > maxT):
                    break


            except Exception as e:
                print(e)
            
    except:
        print("Program interrupted, ending data collection")


if __name__ == "__main__":
    baud = 115200 #arduino uno runs at 9600 baud, placeholder value
    tout = 2 #timeout for serial input
    location = "data" #folder location of collected data
    file = None
    mode = ""
    config_file = "data_collection_config.json"
    
    print("To exit at any time, press CTRL + C")

    (header,probe, timebased, deltaT, maxT, measureTime,conductivityIncrease, baud, arduino_port) = readConfig(config_file)

    # arduino_port = getPort()
    
    ser = connect(arduino_port, tout, baud)
    
    file = makeFile(header, location)

    print("Beginning time based conductivity data collection")
    collectTimeBasedConductivityData(ser, file, deltaT, maxT)
