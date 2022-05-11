# Required Python Libraries

- Dronekit - https://dronekit-python.readthedocs.io/en/latest/guide/quick_start.html
- You might have to install other libraries such as, pyserial, for Arduino communications.
  > pip install pyserial

# Required Files

> <strong>Note:</strong> For all of these to make sense, I recommend reading the code in all files.

**1. trashcan.weights**

- The Yolov4-tiny-288 model target detection provided this weight file. The Jetson Nano need this file in order to detect the target. Simply modify the weight file to your weight if you wish to detect a different target.  
  <strong>NOTE: Don't forget to change your config file</strong>

**2. trashcan.cfg**

- This is the configuration file included with the weight file. This is also required for detect.py to work.

**3. detect.py**

- This file is in charge of recognizing the target and informing the other program, move.py, about when and where the drone should move.

**4. move.py**

- This file is in charge of controlling the drone's movement.

**5. commands.txt**

- The team must create a txt file to function as the communicator because detect.py and move.py do not support the same version of Python.
- For instance, detect.py will send commands to commands.txt, which will be read by move.py. If move.py is ready for the next command after executing the current command, it will communicate with commands.txt.

<br>

# Running the programs

> NOTE: Remote in to your Jetson Nano and execute these programs.

**1. First run move.py**

> python move.py

**2. Run detect.py**

> python3 detect.py

- <strong>Note:</strong> Once these two programs are up and running, instruct your pilot to turn on the autonomous switch to begin the delivery. For all of them to make sense, I recommend reading the code in all python files.

<br>

# Electrical Components

Propeller : T-Motor 13\*4.4  
Motor: Antigravity MN4006  
Battery: FCONEGY 6s 5500mAh  
Receiver: Radiolink R9DSM 2.4GHz  
Processor 1: Jetson Nano Developer Kit 4gb  
Microcontroller: Arduino Mega  
Controller: Radiolink AT9S Pro  
ESC: HAKRC 45A 4-1 ESC  
FC: Matek H743 Slim  
Payload Motor: Nema 17 Bipolar 1.8deg 16Ncm   
Flight Camera: Jetson Camera IMX219  
GPS/Compass: M9N-5883 Matek System  
H-Bridge: L298N  
Level Shifter: HiLetgo TXS0108E
