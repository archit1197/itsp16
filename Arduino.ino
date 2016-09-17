

int i=0;
String temp;
int d=0;
float a=0.0;

void setup(){
  Serial.begin(9600);
  pinMode(8,1);
  pinMode(9,1);
  pinMode(10,1);
  pinMode(11,1);
  Serial.write('1');
  //delay(10000);
}

void loop(){
  if(Serial.available()>0){
    while(Serial.available()>0){
      temp=Serial.readString();
    }
    for(int i=0; i<6; i++){
      if(i<3){
        d=+temp[i]*pow(10,2-i);
      }
      else{
        a+=temp[i]*pow(10,5-i);
      }
    }
    //going to specified position
    digitalWrite(10,0);  
    for(int i=0; i<d*2.1*100/18; i++){
      digitalWrite(11,1);
      delay(10);
      digitalWrite(11,0);
      delay(10);
    }
    delay(1000);
    //aiming at specified angle
    digitalWrite(8,1);
    for(int i=0; i<int(a*100/180); i++){
      digitalWrite(9,1);
      delay(50);
      digitalWrite(9,0);
      delay(50);
    }
    //This part is for automatic shot through L293D controlled DC Motor
    /*delay(10000);
    digitalWrite(2,1);
    digitalWrite(3,0);
    delay(200);
    digitalWrite(2,0);
    digitalWrite(3,0);
    */
    delay(1000);
    //returning to original angle
    digitalWrite(8,0);
    for(int i=0; i<int(a*100/180); i++){
      digitalWrite(9,1);
      delay(50);
      digitalWrite(9,0);
      delay(50);
    }
    delay(1000);
    //returning to original position
    digitalWrite(10,1);  
    for(int i=0; i<d*2.1*100/18; i++){
      digitalWrite(11,1);
      delay(10);
      digitalWrite(11,0);
      delay(10);
    }
  }
  Serial.write('0');
}

 
