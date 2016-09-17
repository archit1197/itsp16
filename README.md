# itsp16

ITSP 2K16

This repository is for my project "Autonomus Carrom Playing Bot", completed under Institute Technical Summer Project, IIT Bombay.  
The included python script attempts to decide the best shot for our carrom bot. Basically, through Image Processing, we will first 
obtain the co-ordinates of all the black, white, and red coins, and also their radius. Once that happens, we need to pick a 
coin that will be the easiet shot for our bot. So we build up from various cases like single shot, double shot, cut shot etc. 
and the final objective is to return the angle and power with which to strike. These values are transferred to the arduino code which drives the motors accordingly.

