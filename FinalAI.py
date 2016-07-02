from math import sqrt,atan,degrees

strikerLine_y = 900;
pocket1_x=0
pocket1_y=0
pocket2_x=1000
pocket2_y=0
pocket3_x=1000
pocket3_y=1000
pocket4_x=0
pocket4_y=1000
striker_radius=15;

def isOnLine(x):
	if x>100 and x <900:
		return True
	if x>80 and x<85:
		return True
	if x>915 and x<920:
		return True
	return False

class Coin:
	#Class that takes care of coins
	radius =10
	
	def __init__(self,xcord,ycord):
		self.x = xcord
		self.y = ycord
		self.slope1 = (self.y-pocket1_y)/float((self.x-pocket1_x))
		self.slope2 = (self.y-pocket2_y)/float((self.x-pocket2_x))
		self.slope3 = (self.y-pocket3_y)/float((self.x-pocket3_x))
		self.slope4 = (self.y-pocket4_y)/float((self.x-pocket4_x))
		self.intercept1= self.y - self.slope1*self.x 
		self.intercept2= self.y - self.slope2*self.x 
		self.intercept3= self.y - self.slope3*self.x 
		self.intercept4= self.y - self.slope4*self.x

	def getx(self):
		return self.x
	def gety(self):
		return self.y
	def getCord(self):
		return (self.x,self.y);
	def setCord(self,xcord,ycord):
		self.x=xcord
		self.y=ycord
		self.slope1 = (self.y-pocket1_y)/float((self.x-pocket1_x))
		self.slope2 = (self.y-pocket2_y)/float((self.x-pocket2_x))
		self.slope3 = (self.y-pocket3_y)/float((self.x-pocket3_x))
		self.slope4 = (self.y-pocket4_y)/float((self.x-pocket4_x))
		self.intercept1= self.y - self.slope1*self.x 
		self.intercept2= self.y - self.slope2*self.x
		self.intercept3= self.y - self.slope3*self.x
		self.intercept4= self.y - self.slope4*self.x
	

class WhiteCoin(Coin):
	def __init__(self,xcord,ycord):
		Coin.__init__(self,xcord,ycord)
	def printCoin(self):
		print("I am a " + "White" + " Coin at: " + str(Coin.getx(self)) +" , " + str(Coin.gety(self)))

class BlackCoin(Coin):
	def __init__(self,xcord,ycord):
		Coin.__init__(self,xcord,ycord)
	def printCoin(self):
		print("I am a " + "Black" + " Coin at: " + str(Coin.getx(self)) +" , " + str(Coin.gety(self)))

class RedCoin(Coin):
	def __init__(self,xcord,ycord):
		Coin.__init__(self,xcord,ycord)
	def printCoin(self):
		print("I am a " + "Queen" + " Coin at: " + str(Coin.getx(self)) +" , " + str(Coin.gety(self)))
"""
#Creating a sample test case
listOfWhiteCoins = [WhiteCoin(100,100) for i in range (9)]
listOfBlackCoins = [BlackCoin(100,100) for i in range (9)]
listOfRedCoins = [RedCoin(100,100) for i in range (1)]

#Printing my coins
def printAllCoins():
	for i in range (9):
		listOfWhiteCoins[i].printCoin()
		listOfBlackCoins[i].printCoin()
	listOfRedCoins[0].printCoin()


#Testing out some coordinates
from random import randint
for j in range (9):
	i=j+1
	listOfWhiteCoins[j].setCord(randint(1,999),randint(1,999))
	listOfBlackCoins[j].setCord(randint(1,999),randint(1,999))
listOfRedCoins[0].setCord(randint(1,999),randint(1,999))


"""
listOfWhiteCoins = [WhiteCoin(900,50) for i in range (1)]
listOfBlackCoins = [WhiteCoin(100,100) for i in range (1)]
listOfRedCoins = [WhiteCoin(500,500) for i in range (1)]
def printAllCoins():
	for i in range (1):
		listOfWhiteCoins[i].printCoin()
		listOfBlackCoins[i].printCoin()
	listOfRedCoins[0].printCoin()


printAllCoins();


def isCoinInWay(coinToPot,striker_x,pocketnumber):
	if pocketnumber==1:
		slope=coinToPot.slope1
		intercept=coinToPot.intercept1
	elif pocketnumber==2:
		slope=coinToPot.slope2
		intercept=coinToPot.intercept2
	elif pocketnumber==3:
		slope=coinToPot.slope3
		intercept=coinToPot.intercept3
	elif pocketnumber==4:
		slope=coinToPot.slope4
		intercept=coinToPot.intercept4


	flag = 0 

	intercept1=intercept-(striker_radius+coinToPot.radius)*sqrt(1 + (slope**2))
	intercept2=intercept+(striker_radius+coinToPot.radius)*sqrt(1 + (slope**2))

	for coin in listOfWhiteCoins:
		if(coin!=coinToPot and coin.gety()<coinToPot.radius +strikerLine_y):
			if ((coin.gety()-slope* coin.getx()-intercept1)*(coin.gety()-slope* coin.getx()-intercept2)) <= 0:
				flag = flag+1
				x=coin.getx()
				y=coin.gety()

	for coin in listOfBlackCoins:
		if(coin!=coinToPot and coin.gety()<coinToPot.radius +strikerLine_y):
			if ((coin.gety()-slope* coin.getx()-intercept1)*(coin.gety()-slope* coin.getx()-intercept2)) <= 0:
				flag = flag+1
				x=coin.getx()
				y=coin.gety()

	for coin in listOfRedCoins:
		if(coin!=coinToPot and coin.gety()<coinToPot.radius +strikerLine_y):
			if ((coin.gety()-slope* coin.getx()-intercept1)*(coin.gety()-slope* coin.getx()-intercept2)) <= 0:
				flag = flag+1
				x=coin.getx()
				y=coin.gety()

	if flag==1:
		return flag,x,y 
	return flag,0,0


def directShot(coinToPot):
	strikerLine_x1 = (strikerLine_y - coinToPot.gety())/coinToPot.slope1 + coinToPot.getx();
	if(isOnLine(strikerLine_x1)):
		flag,xcord,ycord=isCoinInWay(coinToPot,strikerLine_x1,1);
		if(flag==0):
			if(degrees(atan(coinToPot.slope1>0))):
				return True,strikerLine_x1,degrees(atan(coinToPot.slope1)),160;
			else:
				return True,strikerLine_x1,(180+degrees(atan(coinToPot.slope1))),160;

	strikerLine_x2 = (strikerLine_y - coinToPot.gety())/coinToPot.slope2 + coinToPot.getx();
	if(isOnLine(strikerLine_x2)):
		flag,xcord,ycord=isCoinInWay(coinToPot,strikerLine_x2,1);
		if(flag==0):
			if(degrees(atan(coinToPot.slope2>0))):
				return True,strikerLine_x2,degrees(atan(coinToPot.slope2)),160;
			else:
				return True,strikerLine_x2,(180+degrees(atan(coinToPot.slope2))),160;

	return False,0,0,0;

"""
def doubleShot(coinToPot)


	intercept1=coinToPot.intercept1-(10)*sqrt(1 + (slope**2))
	intercept2=coinToPot.intercept1+(10)*sqrt(1 + (slope**2))
	strikerLine_x1 = (strikerLine_y - coinToPot.gety())/coinToPot.slope1 + coinToPot.getx()
	if(isOnLine(strikerLine_x1)):
		no_coins,x,y = isCoinInWay(coinToPot,strikerLine_x1,1)  ;
		if(no_coins==0):
			return True,strikerLine_x1
		elif(no_coins==1):
			if ((y-slope*x-intercept1)*(y-slope* x-intercept2)) <= 0:
				return True,strikerLine_x1
			
		
	strikerLine_x2 = (strikerLine_y - coinToPot.gety())/coinToPot.slope2 + coinToPot.getx()
	if(isOnLine(strikerLine_x2)):
		if(!isCoinInWay(coinToPot,strikerLine_x2,2)[0]):
			return True,strikerLine_x2
		elif(isCoinInWay(coinToPot,strikerLine_x1,1)[0]==1):
			if ((isCoinInWay(coinToPot,strikerLine_x1,1)[2]-slope* isCoinInWay(coinToPot,strikerLine_x1,1)[1]-intercept1)*
			(isCoinInWay(coinToPot,strikerLine_x1,1)[2]-slope* isCoinInWay(coinToPot,strikerLine_x1,1)[1]-intercept2)) <= 0:
				return True,strikerLine_x2
				

	return False,0;
"""
def isCoinInRange(coinToPot,x1,y1,x2,y2):
	ymax= max(y1,y2);
	ymin=min(y1,y2);
	xmax= max(x1,x2);
	xmin=min(x1,x2);

	if(coinToPot.getx()<xmin):
		return False;
	if(coinToPot.getx()>xmax):
		return False;
	if(coinToPot.gety()<ymin):
		return False;
	if(coinToPot.getx()<ymax):
		return False;
	return True;

	

def isCoinInWay2(coinToPot,x1,y1,x2,y2):

	slope = float(y2-y1)/float(x2-x1);
	intercept= y1- slope*x1;

	intercept1=intercept-(striker_radius+coinToPot.radius)*sqrt(1 + (slope**2))
	intercept2=intercept+(striker_radius+coinToPot.radius)*sqrt(1 + (slope**2))

	for coin in listOfWhiteCoins:
		if(coin!=coinToPot and coin.gety()<coinToPot.radius +strikerLine_y and isCoinInRange(coinToPot,x1,y1,x2,y2)):
			if ((coin.gety()-slope* coin.getx()-intercept1)*(coin.gety()-slope* coin.getx()-intercept2)) <= 0:
				return True;

	for coin in listOfBlackCoins:
		if(coin!=coinToPot and coin.gety()<coinToPot.radius +strikerLine_y and isCoinInRange(coinToPot,x1,y1,x2,y2)):
			if ((coin.gety()-slope* coin.getx()-intercept1)*(coin.gety()-slope* coin.getx()-intercept2)) <= 0:
				return True;

	for coin in listOfRedCoins:
		if(coin!=coinToPot and coin.gety()<coinToPot.radius +strikerLine_y and isCoinInRange(coinToPot,x1,y1,x2,y2)):
			if ((coin.gety()-slope* coin.getx()-intercept1)*(coin.gety()-slope* coin.getx()-intercept2)) <= 0:
				return True;

	return False;




def sideCollideShot(coinToPot):
	rightCollidePoint_y=(pocket2_x-pocket1_x)*coinToPot.slope1;
	strikerLine_x1 = (rightCollidePoint_y - strikerLine_y)/coinToPot.slope1 + pocket2_x;
	if(isOnLine(strikerLine_x1)):
		if(not isCoinInWay2(coinToPot,strikerLine_x1,strikerLine_y,pocket2_x,rightCollidePoint_y)):
			if(not isCoinInWay2(coinToPot,pocket2_x,rightCollidePoint_y,pocket1_x,pocket1_y)):
				if(degrees(atan(coinToPot.slope1)))>0:
					return True,strikerLine_x1,(180-degrees(atan(coinToPot.slope1))),200
				else:
					return True,strikerLine_x1,(-1)*degrees(atan(coinToPot.slope1)),200

	leftCollidePoint_y=(pocket1_x-pocket2_x)*coinToPot.slope2;
	strikerLine_x2 = (leftCollidePoint_y - strikerLine_y)/coinToPot.slope2 + pocket1_x;
	if(isOnLine(strikerLine_x2)):
		if(not(isCoinInWay2(coinToPot,strikerLine_x2,strikerLine_y,pocket1_x,leftCollidePoint_y) or isCoinInWay2(coinToPot,pocket1_x,leftCollidePoint_y,pocket2_x,pocket2_y))):
			if(degrees(atan(coinToPot.slope2)))<0:
				return True,strikerLine_x2,(-1)*degrees(atan(coinToPot.slope2)),200
			else:
				return True,strikerLine_x2,(180-degrees(atan(coinToPot.slope2))),200

	
	return False,0,0,0;




def cutShot(coinToPot):
	if(coinToPot.gety() > strikerLine_y):
		return False,0,0,0;
	if(coinToPot.getx()< pocket2_x/2):
		pointToHit_x = coinToPot.getx() + (coinToPot.radius + striker_radius)/sqrt(1 + coinToPot.slope1 **2);
		pointToHit_y = coinToPot.gety() + (coinToPot.radius + striker_radius)*coinToPot.slope1/sqrt(1 + coinToPot.slope1 **2);
		strikerLine_x1 = pointToHit_x + (strikerLine_y - pointToHit_y)/coinToPot.slope1*1.5;
		strikerLine_x2 = pointToHit_x + (strikerLine_y - pointToHit_y)/coinToPot.slope1*0.5;
		m1=(pointToHit_y-strikerLine_y)/float(pointToHit_x-strikerLine_x1)
		m2=(pointToHit_y-strikerLine_y)/float(pointToHit_x-strikerLine_x2)
		if(isOnLine(strikerLine_x1)):
			if(not isCoinInWay2(coinToPot,strikerLine_x1,strikerLine_y,pointToHit_x,pointToHit_y)):
				if(not isCoinInWay2(coinToPot,pointToHit_x,pointToHit_y,pocket1_x,pocket1_y)):
					if m1>0:
						return True,strikerLine_x1,degrees(atan(m1)),180;
					else:
						return True,strikerLine_x1,(180+degrees(atan(m1))),180;
		if(isOnLine(strikerLine_x2)):
			if(not isCoinInWay2(coinToPot,strikerLine_x2,strikerLine_y,pointToHit_x,pointToHit_y)):
				if(not isCoinInWay2(coinToPot,pointToHit_x,pointToHit_y,pocket1_x,pocket1_y)):
					if m2>0:
						return True,strikerLine_x2,degrees(atan(m2)),180;
					else:
						return True,strikerLine_x2,(180+degrees(atan(m2))),180;

	else:
		pointToHit_x = coinToPot.getx() - (coinToPot.radius + striker_radius)/sqrt(1 + coinToPot.slope2 **2);
		pointToHit_y = coinToPot.gety() - (coinToPot.radius + striker_radius)*coinToPot.slope2/sqrt(1 + coinToPot.slope2 **2);
		strikerLine_x1 = pointToHit_x + (strikerLine_y - pointToHit_y)/coinToPot.slope2*1.5;
		strikerLine_x2 = pointToHit_x + (strikerLine_y - pointToHit_y)/coinToPot.slope2*0.5;
		m1=(pointToHit_y-strikerLine_y)/float(pointToHit_x-strikerLine_x1)
		m2=(pointToHit_y-strikerLine_y)/float(pointToHit_x-strikerLine_x2)
		if(isOnLine(strikerLine_x1)):
			if(not isCoinInWay2(coinToPot,strikerLine_x1,strikerLine_y,pointToHit_x,pointToHit_y)):
				if(not isCoinInWay2(coinToPot,pointToHit_x,pointToHit_y,pocket2_x,pocket2_y)):
					if m1>0:
						return True,strikerLine_x1,degrees(atan(m1)),180;
					else:
						return True,strikerLine_x1,(180+degrees(atan(m1))),180;
		if(isOnLine(strikerLine_x2)):
			if(not isCoinInWay2(coinToPot,strikerLine_x2,strikerLine_y,pointToHit_x,pointToHit_y)):
				if(not isCoinInWay2(coinToPot,pointToHit_x,pointToHit_y,pocket2_x,pocket2_y)):
					if m1>0:
						return True,strikerLine_x2,degrees(atan(m2)),180;
					else:
						return True,strikerLine_x2,(180+degrees(atan(m2))),180;

	return False,0,0,0;



#Testing
for coin in listOfWhiteCoins:
	boolv,x,angle,power = directShot(coin)
	if(boolv):
		print("Shoot from position "+ str(x)+" from angle "+str(angle))
	else:
		boolv,x,angle,power=sideCollideShot(coin);
		if(boolv):
			print("Side Shoot from position "+ str(x)+" from angle "+str(angle))
		else:
			boolv,x,angle,power=cutShot(coin);
			if(boolv):
				print("Cut Shoot from position "+ str(x)+" from angle "+str(angle))	
			else:
				print("Can't Shoot even after All Your EFFORTS")

for coin in listOfBlackCoins:
	boolv,x,angle,power = directShot(coin)
	if(boolv):
		print("Shoot from position "+ str(x)+" from angle "+str(angle))
	else:
		boolv,x,angle,power=sideCollideShot(coin);
		if(boolv):
			print("Side Shoot from position "+ str(x)+" from angle "+str(angle))
		else:
			boolv,x,angle,power=cutShot(coin);
			if(boolv):
				print("Cut Shoot from position "+ str(x)+" from angle "+str(angle))	
			else:
				print("Can't Shoot even after All Your EFFORTS")

for coin in listOfRedCoins:
	boolv,x,angle,power = directShot(coin)
	if(boolv):
		print("Shoot from position "+ str(x)+" from angle "+str(angle))
	else:
		boolv,x,angle,power=sideCollideShot(coin);
		if(boolv):
			print("Side Shoot from position "+ str(x)+" from angle "+str(angle))
		else:
			boolv,x,angle,power=cutShot(coin);
			if(boolv):
				print("Cut Shoot from position "+ str(x)+" from angle "+str(angle))	
			else:
				print("Can't Shoot even after All Your EFFORTS")
