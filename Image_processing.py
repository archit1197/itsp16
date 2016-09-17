
import cv2.cv as cv
import cv2
import numpy as np
import serial
import time

#colour range, radius, and Hough Transform parameters FOR BLACK/WHITE Coins
minR=9
maxR=13
p1=100
p2=10
minD=minR
radius=0
pocketParam=5
tolerance=0.8

#same params for RED ENDS
RminR=5
RmaxR=10
RminD=RminR

#global variables to store colors(b,g,r)
#colors for function and colorRed, colorBlack, colorWhite for individual storage
colors=[]
colorRed=[]
colorBlack=[]
colorWhite=[]
rangeRedEnd=[[0,0],[0,0]]
rangeBW=[[0,0],[0,0,0]]
rangeB=[[0,0],[0,0]]
rangeW=[[0,0],[0,0]]

#global for coords of pockets	
pockets=[]

#calibration flag
calib=1

#create serial object and variable for serial reading
#ser=serial.Serial('/dev/ttyACM0', 9600)
#apna shot pehle B-)
buttonPress='1'

#striker parameters
strikerLine_y=0
strikerLine_End=0
strikerLine_Start=0
striker_radius=0

#mouse callback functions, for pockets, red/color and BW
def get_values(event,x,y,flags,param):
	if event == cv2.EVENT_LBUTTONDOWN:
		colors.append([q[y,x,0],q[y,x,1],q[y,x,2]])

#def get_values_BW(event,x,y,flags,param):
#	if event == cv2.EVENT_LBUTTONDOWN:
#		colors.append(j[y,x])

def get_coords(event,x,y,flags,param):
 	if event == cv2.EVENT_LBUTTONDOWN:
		pockets.append([y,x])

#for creating a window, binding the function to it, and showing the image in it
def show_Window(purpose):
	cv2.namedWindow(purpose)
	cv2.setMouseCallback(purpose,get_values)
	#show the required image(p) in the window
	while(1):
		cv2.imshow(purpose,p)
		if cv2.waitKey(20) & 0xFF == 27 :
			break
	cv2.destroyAllWindows()

def show_Window_coords(purpose):
	cv2.namedWindow(purpose)
	cv2.setMouseCallback(purpose,get_coords)
	#show the required image(p) in the window
	while(1):
		cv2.imshow(purpose,p)
		if cv2.waitKey(20) & 0xFF == 27 :
			break
	cv2.destroyAllWindows()

#calculating ranges for red, black, white in H and S
def calc_Range(array):
	big=0
	small=0
	for a in range(0,len(array[0])-1) :
		big=array[0][a]
		small=array[0][a]
		for b in range(0, len(array)) :
			big=max(big,array[b][a])
			small=min(small,array[b][a])
		rangeRedEnd[0][a]+=big+tolerance*(big-small)
		rangeRedEnd[1][a]+=small-tolerance*(big-small)

def calc_Range_BW(array):
	big=0
	small=0
	for a in range(0,len(array[0])-1) :
		big=array[0][a]
		small=array[0][a]
		for b in range(0, len(array)) :
			big=max(big,array[b][a])
			small=min(small,array[b][a])
		rangeBW[0][a]+=big+tolerance*(big-small)
		rangeBW[1][a]+=small-tolerance*(big-small)

#best-fit square from selected pocket centres
def make_Square(array):
	avgx=0
	avgy=0
	devx=0
	devy=0
	for i in pockets:
		avgx=avgx+i[0]
		avgy=avgy+i[1]
	avgx=avgx/4
	avgy=avgy/4
	for i in pockets:
		devx+=abs(i[0]-avgx)
		devy+=abs(i[1]-avgy)
	devx=devx/4
	devy=devy/4
	return [[avgx-devx,avgy-devy],[avgx+devx,avgy-devy],[avgx+devx,avgy+devy],[avgx-devx,avgy+devy]]

def isPointAroundPocket(point,pocketArray):
	#fill this later
	pass

#calibrate only once
if calib :
	"""
	#declare default camera object
	cap = cv2.VideoCapture(0)	
	time.sleep(1)
	# Capture a frame
	ret, p = cap.read()
	#release the resource
	cap.release()
	"""

	p=cv2.imread('SingleTest.jpg',-1)
	
	#read image as grayscale(Hough needs a single channel image)
	#j is grayscale, p is color(RGB), q is color(HSV)
	j=cv2.cvtColor(p,cv2.COLOR_BGR2GRAY)
	q=cv2.cvtColor(p,cv2.COLOR_BGR2HSV)
	q=cv2.medianBlur(q,11)
	j=cv2.medianBlur(j,5)
	centrej=cv2.cvtColor(j,cv2.COLOR_GRAY2RGB)

	#read coordinates of pockets
	show_Window_coords('Click on all pockets')
	
	#read red, black and white colour arrays(b,g,r)
	show_Window('Click on all the red ends')
	colorRed=colors
	colors=[]
	show_Window('Click on all the black coins')
	colorBlack=colors
	colors=[]
	show_Window('Click on all the white coins')
	colorWhite=colors
	colors=[]

	#calculating and displaying ranges of red ends, and black white coins
	calc_Range(colorRed)
	calc_Range_BW(colorBlack)
	rangeB=rangeBW
	rangeBW=[[0,0],[0,0]]
	calc_Range_BW(colorWhite)
	rangeW=rangeBW
	rangeBW=[[0,0],[0,0]]

	#get the square from pockets for AI boundary
	square=make_Square(pockets)
	pocket2_x=square[3][1]-square[0][1]
	pocket3_x=square[2][1]-square[0][1]
	pocket3_y=square[2][0]-square[0][0]
	pocket4_y=square[1][0]-square[0][0]
	
	#find circles using the Hough Transform
	circles=cv2.HoughCircles(j,cv.CV_HOUGH_GRADIENT,1,minD,param1=p1,param2=p2,minRadius=minR,maxRadius=maxR)
	circles=np.uint16(np.around(circles))
	circlesW=[]
	circlesB=[]
	redEnds=[]
	#show circles in green and centres in red
	#also classify coins based on the colors at their centres(values by calib)
	#and exclude the circles lying beyond the square formed by 4 pockets
	for i in circles[0, :] :
		cv2.circle(centrej,(i[0],i[1]),i[2],(0,255,0),2)
		cv2.circle(centrej,(i[0],i[1]),2,(0,255,0),3)
		if i[0]>(square[3][1]+pocketParam) or i[0]<(square[0][1]-pocketParam) :
			pass
		elif i[1]<(square[0][0]-pocketParam) or i[1]>(square[1][0]+pocketParam) :
			pass
		#elif q[i[1],i[0],1]>rangeRedEnd[1][1] and q[i[1],i[0],1]<rangeRedEnd[0][1] and q[i[1],i[0],0]>rangeRedEnd[1][0] and q[i[1],i[0],0]<rangeRedEnd[0][0] :
		#	redEnds.append([i[1]-square[0][0],i[0]-square[0][1]])
		elif q[i[1],i[0],1]>rangeB[1][1] and q[i[1],i[0],1]<rangeB[0][1] and q[i[1],i[0],0]>rangeB[1][0] and q[i[1],i[0],0]<rangeB[0][0]:
			circlesB.append([i[1]-square[0][0],i[0]-square[0][1]])
			radius+=i[2]
		elif q[i[1],i[0],1]>rangeW[1][1] and q[i[1],i[0],1]<rangeW[0][1] and q[i[1],i[0],0]>rangeW[1][0] and q[i[1],i[0],0]<rangeW[0][0]:
			circlesW.append([i[1]-square[0][0],i[0]-square[0][1]])
			radius+=i[2]

	radius=radius/(len(circlesW)+len(circlesB))
	striker_radius=radius*1.3
	
	#"""FOR RED ENDS AND THUS STIKER LINE
	#find circles using the Hough Transform
	circles=cv2.HoughCircles(j,cv.CV_HOUGH_GRADIENT,1,RminD,param1=p1,param2=p2,minRadius=RminR,maxRadius=RmaxR)
	circles=np.uint16(np.around(circles))
	redEnds=[]
	for i in circles[0, :] :
		cv2.circle(centrej,(i[0],i[1]),i[2],(0,0,255),2)
		cv2.circle(centrej,(i[0],i[1]),2,(0,255,0),3)
		if i[0]>(square[3][1]+pocketParam) or i[0]<(square[0][1]-pocketParam) :
			pass
		elif i[1]<(square[0][0]-pocketParam) or i[1]>(square[1][0]+pocketParam) :
			pass
		elif q[i[1],i[0],1]>rangeRedEnd[1][1] and q[i[1],i[0],1]<rangeRedEnd[0][1] and q[i[1],i[0],0]>rangeRedEnd[1][0] and q[i[1],i[0],0]<rangeRedEnd[0][0] :
			redEnds.append([i[1]-square[0][0],i[0]-square[0][1]])	

	for i in redEnds :
		strikerLine_y=max(strikerLine_y,i[0])
	strikerLine_y-=square[0][0]

	strikerLineEnds=[0,0]
	m=0
	for i in redEnds :
		if abs(i[0]-strikerLine_y-square[0][0])<15 :
			strikerLineEnds[m]=i[1]
			m+=1

	strikerLine_Start=min(strikerLineEnds[0],strikerLineEnds[1])
	strikerLine_End=max(strikerLineEnds[0],strikerLineEnds[1])
	#"""

	#"""TESTING
	for i in redEnds :
		cv2.circle(centrej,(i[1],i[0]),2,(255,255,255),3)
	cv2.imshow('RED ENDS shown WHITE',centrej)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	print pockets
	print colorRed
	print colorBlack
	print colorWhite
	print rangeRedEnd
	print rangeB
	print rangeW
	print square
	print redEnds
	print radius
	print striker_radius
	print strikerLine_y
	print strikerLineEnds
	print strikerLine_Start
	print strikerLine_End
	#"""

#once calibrated, set flag
calib=0

while True :
	while(buttonPress!='1') :
		#buttonPress=ser.read()
		pass

	"""
	#declare default camera object
	cap = cv2.VideoCapture(0)
	time.sleep(1)
	# Capture a frame
	ret, p = cap.read()
	#release the resource
	cap.release()
	#"""

	p=cv2.imread('SingleTest.jpg',-1)
	#read image as grayscale(Hough needs a single channel image)
	#j is grayscale, p is color(RGB), q is color(HSV)
	j=cv2.cvtColor(p,cv2.COLOR_BGR2GRAY)
	q=cv2.cvtColor(p,cv2.COLOR_BGR2HSV)
	q=cv2.medianBlur(q,11)
	j=cv2.medianBlur(j,5)
	centrej=cv2.cvtColor(j,cv2.COLOR_GRAY2RGB)
	
	#find circles using the Hough Transform
	circles=cv2.HoughCircles(j,cv.CV_HOUGH_GRADIENT,1,minD,param1=p1,param2=p2,minRadius=minR,maxRadius=maxR)
	circles=np.uint16(np.around(circles))
	circlesW=[]
	circlesB=[]
	redEnds=[]

	#show circles in green and centres in red
	#also classify coins based on the colors at their centres(values by calib)
	for i in circles[0, :] :
		cv2.circle(centrej,(i[0],i[1]),i[2],(0,255,0),2)
		cv2.circle(centrej,(i[0],i[1]),2,(0,0,255),3)
		if i[0]>(square[3][1]+pocketParam) or i[0]<(square[0][1]-pocketParam) :
			pass
		elif i[1]<(square[0][0]-pocketParam) or i[1]>(square[1][0]+pocketParam) :
			pass
		#elif q[i[1],i[0],1]>rangeRedEnd[1][1] and q[i[1],i[0],1]<rangeRedEnd[0][1] and q[i[1],i[0],0]>rangeRedEnd[1][0] and q[i[1],i[0],0]<rangeRedEnd[0][0] :
		#	redEnds.append([i[1]-square[0][0],i[0]-square[0][1]])
		elif q[i[1],i[0],1]>rangeB[1][1] and q[i[1],i[0],1]<rangeB[0][1] and q[i[1],i[0],0]>rangeB[1][0] and q[i[1],i[0],0]<rangeB[0][0]:
			circlesB.append([i[1]-square[0][0],i[0]-square[0][1]])
			radius+=i[2]
		elif q[i[1],i[0],1]>rangeW[1][1] and q[i[1],i[0],1]<rangeW[0][1] and q[i[1],i[0],0]>rangeW[1][0] and q[i[1],i[0],0]<rangeW[0][0]:
			circlesW.append([i[1]-square[0][0],i[0]-square[0][1]])
			radius+=i[2]
	
	#"""TESTING
	cv2.imshow('DETECTED circles and centres',centrej)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	print redEnds
	print circlesW
	print circlesB
	for i in circlesW :
		cv2.circle(centrej,(i[1],i[0]),2,(255,255,255),3)
	for i in circlesB :
		cv2.circle(centrej,(i[1],i[0]),2,(0,0,0),3)
	for i in redEnds :
		cv2.circle(centrej,(i[1],i[0]),2,(0,0,255),3)
	cv2.imshow('CLASSIFIED: With their colors',centrej)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	#"""
	#sweg bitches!

	buttonPress='0'
