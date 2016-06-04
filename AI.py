import math
strikerLine_y = 900;
pocket1_x=0;
pocket1_y=0;
pocket2_x=1000;
pocket2_y=0;

def isOnLine(x):
	if x>100 and x <900:
		return True;
	if x>80 and x<85:
		return True;
	if x>915 and x<920:
		return True;
	return False;

class Coin:
	#Class that takes care of coins
	radius =10;
	
	def __init__(self,xcord,ycord):
		self.x = xcord
		self.y = ycord
		self.slope1 = (self.y-pocket1_y)/float((self.x-pocket1_x))
		self.slope2 = (self.y-pocket2_y)/float((self.x-pocket2_x))
		self.intercept1= self.y - self.slope1*self.x 
		self.intercept2= self.y - self.slope2*self.x

	def getx(self):
		return self.x
	def gety(self):
		return self.y
	def getCord(self):
		return (self.x,self.y);
	def setCord(self,xcord,ycord):
		self.x=xcord;
		self.y=ycord;
		self.slope1 = (self.y-pocket1_y)/float((self.x-pocket1_x))
		self.slope2 = (self.y-pocket2_y)/float((self.x-pocket2_x))
		self.intercept1= self.y - self.slope1*self.x 
		self.intercept2= self.y - self.slope2*self.x
	

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

#Creating my beloved coins at ORIGIN
listOfWhiteCoins = [WhiteCoin(500,500) for i in range (9)];
listOfBlackCoins = [BlackCoin(500,500) for i in range (9)];
listOfRedCoins = [RedCoin(500,500) for i in range (1)];


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

printAllCoins();

def isCoinInWay(coinToPot,striker_x,pocketnumber):
	if pocketnumber==1:
		slope=coinToPot.slope1;
		intercept=coinToPot.intercept1;
	if pocketnumber==2:
		slope=coinToPot.slope2;
		intercept=coinToPot.intercept2;

	intercept1=intercept-(2*coinToPot.radius)*math.sqrt(1 + (slope**2));
	intercept2=intercept+(2*coinToPot.radius)*math.sqrt(1 + (slope**2));

	for coin in listOfWhiteCoins:
		if(coin!=coinToPot and coin.gety()<coinToPot.radius +strikerLine_y):
			if ((coin.gety()-slope* coin.getx()-intercept1)*(coin.gety()-slope* coin.getx()-intercept2)) <= 0:
				return False
	for coin in listOfBlackCoins:
		if(coin!=coinToPot and coin.gety()<coinToPot.radius +strikerLine_y):
			if ((coin.gety()-slope* coin.getx()-intercept1)*(coin.gety()-slope* coin.getx()-intercept2)) <= 0:
				return False
	for coin in listOfRedCoins:
		if(coin!=coinToPot and coin.gety()<coinToPot.radius +strikerLine_y):
			if ((coin.gety()-slope* coin.getx()-intercept1)*(coin.gety()-slope* coin.getx()-intercept2)) <= 0:
				return False
	return True;


def directShot(coinToPot):
	strikerLine_x1 = (strikerLine_y - coinToPot.gety())/coinToPot.slope1 + coinToPot.getx();
	if(isOnLine(strikerLine_x1)):
		if(isCoinInWay(coinToPot,strikerLine_x1,1)):
			return True,strikerLine_x1;

	strikerLine_x2 = (strikerLine_y - coinToPot.gety())/coinToPot.slope2 + coinToPot.getx();
	if(isOnLine(strikerLine_x2)):
		if(isCoinInWay(coinToPot,strikerLine_x2,2)):
			return True,strikerLine_x2;

	return False,0;

#Testing
for coin in listOfWhiteCoins:
	boolv,x = directShot(coin)
	if(boolv):
		print("Shoot from position "+ str(x));
	else :
		print("Not possible to shoot");

for coin in listOfBlackCoins:
	boolv,x = directShot(coin)
	if(boolv):
		print("Shoot from position "+ str(x));
	else :
		print("Not possible to shoot");

for coin in listOfRedCoins:
	boolv,x = directShot(coin)
	if(boolv):
		print("Shoot from position "+ str(x));
	else :
		print("Not possible to shoot");