# UCI Chem E Car 2021
Repository created by Lance to centralize code storage for the UCI ChemE Car Team.

## Quick Start Guide:
Most files have descriptive names, but if you're wondering what exactly you need for a specific task I've documented it here!

Nick's starting team:
1. [To test operation of car](https://github.com/GitBoi37/UCI-ChemECar-2021/blob/main/car%20control/nick_button_start/nick_button_start.ino)

Sama's starting team:
1. [To test operation of car](https://github.com/GitBoi37/UCI-ChemECar-2021/blob/main/car%20control/sama_button_start/sama_button_start.ino)

Giselle's stopping team(s)s:
1. [To calibrate the ecprobe use this code NOT anything else](https://github.com/GitBoi37/UCI-ChemECar-2021/blob/main/conductivity%20sensor%20arduino%20code/ecprobe_calibration/ecprobe_calibration.ino)
2. [To collect standard time-to-endpoint data with a hardcoded endpoint (I think this is what you guys have been regularly using)](https://github.com/GitBoi37/UCI-ChemECar-2021/blob/main/conductivity%20sensor%20arduino%20code/measure_time_to_endpt/measure_time_to_endpt.ino)
3. [To collect time-to-endpoint conductivity data with an endpoint that changes every trial](https://github.com/GitBoi37/UCI-ChemECar-2021/blob/main/conductivity%20sensor%20arduino%20code/measure_time_to_variable_endpt/measure_time_to_variable_endpt.ino)

4. [To test car with stopping reaction running](https://github.com/GitBoi37/UCI-ChemECar-2021/blob/main/car%20control/button_start_w_conductivity/button_start_w_conductivity.ino)
 tweak targetvalue variable to be whatever endpoint you want it to be and run the car off a 9V. Requires a pretty specific set-up so just talk to me if you wanna do this.

If you don't want to be harassed to input a specific endpoint, choose the measure_time_to_endpt code and hardcode a value in as the *endpoint* variable on line 30. Once you've made this change you need to compile and push it to the arduino. If you're going to be changing the endpoint after every test, choose the measure_time_to_variable_endpt code.






If you don't have GitHub Desktop installed or if that's not working for whatever reason (which I would recommend if you're updating this code often, you basically just click a button and it synchronizes the repository on your local machine to whatever I've pushed to the server) then you can download the .zip file on the website or copy paste
If one of the arduino scripts doesn't work, specifically one using the DFRobot library, install necessary libraries
Some libraries can be found in the libraries folder, some others may be required to be installed

### rgb sensor tests:
test_DFRobot has worked the best so far
test_getRawData is definitely broken for the old sensor for some reason
test_getRGB is not broken for any sensors, unsure of working status, using first test for now
color_reproduction is good but requires a specific pinup on the breadboard which is in the comments of the code

### For developer:
If you modify the .py scripts and wonder why the .exe doesn't reflect any of your changes simply launch the appropriate .bat script and that will rebuild the .exe and delete any created files in the process, very helpful

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
