# UCIChemECar2021
Repository created by Lance to centralize code storage and stop google docs
If you don't have GitHub Desktop installed or if that's not working for whatever reason (which I would recommend if iyou're updating this code often, you basically just click a button and it synchronizes the repository on your local machine to whatever I've pushed to the server) then you can download the .zip file on the website
If one of the arduino scripts doesn't work, specifically one using the DFRobot library, install necessary libraries
Some libraries can be found in the libraries folder, some others may be required to be installed

rgb sensor tests:
test_DFRobot has worked the best so far
test_getRawData is definitely broken for the old sensor for some reason
test_getRGB is not broken for any sensors, unsure of working status, using first test for now
color_reproduction is good but requires a specific pinup on the breadboard which is in the comments

For data collection:
I have preserved the working code as data_collection_manual_input.exe
data_collection_manual_input.exe is 
Testing has to be done on the new code (data_collection.exe) which not only utilizes a configuration file to streamline data collection but also contains the mode of operation dedicated to measuring the time
until a given data point is reached


To collect data launch the .exe file in the data_collection_with_python folder and follow the prompts, this should work without anything else to be installed. The arduino must be connected to the same computer and running the data_collection_arduino code with serial monitor set to 9600 baud. 
 -- THE SERIAL MONITOR WINDOW MUST BE CLOSED -
This frustrated me early on and was confusing but just close the window, it will collect data and tell you all about it in the program so just trust it. 
Any collected data will be stored in a a .csv file in the data folder which you can open into excel or google sheets and do some data analysis
There are options time based and event based data collection, with the event based data collection you get to input the name of each trial in case you'd ever want that.

Note: for a time-based data collection, the inputed time interval is what the program aims for, but processing time slows down data collection.
The exact time it takes to collect data and write it to the file is taken into account already and is part of the time in the file.
Abort the program at any time by pressing ctrl C

Got problems? @ me on discord, it's a work in progress.

Ignore commpy and .vscode