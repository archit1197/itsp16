# itsp16

ITSP 2K16

This repository is for my project "Autonomus Carrom Playing Bot", completed under Institute Technical Summer Project, IIT Bombay. 

Details of included files:
1.FinalAI.py 
  for deciding the best shot to be made
2.Image_processing.py
  for identifying the positions of the carrom coins and classifying them, using OpenCV library
3.Fullcode.py
  amalgamation of the two mentioned files above
4.Arduino.ino
  basic arduino code for taking power,angle input from the py script and translating it to the motors
  
(Image_processing and Arduino can be found on here: https://github.com/Kkrrish/ITSP16-CarromStrike1.6 

The included python script attempts to decide the best shot for our carrom bot. Basically, through Image Processing, we will first 
obtain the co-ordinates of all the black, white, and red coins, and also their radius. Once that happens, we need to pick a 
coin that will be the easiet shot for our bot. So we build up from various cases like single shot, double shot, cut shot etc. 
and the final objective is to return the angle and power with which to strike. These values are transferred to the arduino code which drives the motors accordingly.

