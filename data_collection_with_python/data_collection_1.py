from serial import *
from time import localtime,strftime,sleep


if __name__ == "__main__":
    print("Starting up...")
    sleep(2)
    #figure out what port is really used
    try:
        iStr = "What is the number of the port being used? It is the com port selected in the arduino IDE. Enter the number only: "
        zer = input(iStr)
    except Exception as e:
        print("Unknown error")
        print(e)
    arduino_port = f"COM{zer}"
    baud = 9600 #arduino uno runs at 9600 baud
    current_time = localtime()
    fTime= strftime('y%Y_m%m_d%d_h%H_m%M', current_time)
    fileName = f"collected_data/color_data_{fTime}.csv" #name of csv generated
    print("Checking directory...")
    try:
        os.makedirs("/collected_data")
        print("Make folder to store data in \"collected data\"")
    except FileExistsError:
        # directory already exists
        print("Dir exists, continue")
        pass
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
    

    print("Creating .csv file...")
    try:
        file = open(fileName, "w")
        file.write("")
        file.write(f"{header}\n")
    except:
        print("Couldn't write file and idk how exceptions work with that so you're SOL maybe don't have bad file names or something")
        if(file.closed() != True):
            file.close()

    print("File created!")
    i = "e"
    print("Ready to collect data! Please note that data collection is sometimes weird but that's just comm error. Simply record another data point. \nType end to end, otherwise input test name:")
    while True:
        i = input("Input: ")
        ser.flushInput()
        sleep(0.25)
        if(i == "end"):
            print("Ending collection...")
            #close the file
            file.close()
            break
        
        try:
            #get and display data to terminal
            getData = str(ser.readline())
            print(getData)
            data = getData[0:][2:-5]
            file.write(str(i) + "," + data +"\n")
        except IOError:
            print("Error writing data")
        except TypeError(str):
            print("invalid str in")
        except SerialException:
            print("Problem collecting data from Arduino")
        except SerialTimeoutException:
            print("Connection timed out")

        
    if(file.closed != True):
        #close the file if not already closed
        file.close()