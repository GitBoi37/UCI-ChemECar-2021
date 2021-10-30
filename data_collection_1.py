from serial import *
from time import localtime,strftime,sleep

if __name__ == "__main__":
    #figure out what port is really used
    arduino_port = "/COM5" 
    baud = 9600 #arduino uno runs at 9600 baud
    current_time = localtime()
    fTime= strftime('y%Y_m%m_d%d_h%H_m%M', current_time)
    fileName = f"collected_data/color_data_{fTime}.csv" #name of csv generated
    header = "input,colorTemp,lux,R,G,B"
    
    ser = Serial(
        port=arduino_port,
        baudrate=9600,
        timeout=2,
        xonxoff=0,
        rtscts=0,
        interCharTimeout=None
    )
    print(f"Connected to Arduino port: {arduino_port}")
    file = open(fileName, "w")
    print("Created file")
    file.write("")
    file.write(f"{header}\n")
    i = "e"
    print("Ready to collect data! Type end to end, otherwise test name:")
    while True:
        i = input("Input: ")
        ser.flushInput()
        sleep(0.25)
        if(i == "end"):
            #close the file
            file.close()
            break
        #get and display data to terminal
        getData = str(ser.readline())
        print(getData)
        data = getData[0:][2:-5]
        try:
            file.write(str(i) + "," + data +"\n")
        except IOError:
            print("error writing data")
        except TypeError(str):
            print("invalid str in")
        
        
    

    #close the file
    file.close()