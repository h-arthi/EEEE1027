#include<LiquidCrystal.h>

//initialize the pins for my reference
//int rs=8, en=9, d4=4,d5=5,d6=6, d7=7;
//initialize the pins with the lcd library
LiquidCrystal lcd(8,9,4,5,6,7);


//initilaizing the motor A
int enA = 3;
int in1 = A1;
int in2 = A2;
//initializing motor B
int enB = 11;
int in3 = A3;
int in4 = A4;
int trigPin = 12;
int echoPin = 13;
float duration, distance;



void setup(){

  pinMode(enA, OUTPUT);
  pinMode(enB, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);



  
 //turn off all motors at initial state
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);
  digitalWrite(in4, LOW);

  
  //setting up lcd
  lcd.begin(16,2);
  lcd.setCursor(0,0);
  lcd.print("Hi I am Jeff");
  delay (1000);
 /* lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("I am connected!");*/
  Serial.begin(9600);

}



void loop(){
int Incoming_value = 0;
Serial.println(Incoming_value);
if(Serial.available()>0)
delay(1000);{
  Incoming_value = Serial.read();
  Serial.println(Incoming_value);
  delay(1000);
  switch(Incoming_value){
    case 103:
      straight();
      break;
    case 108:     
      left();
      delay(2000);
      notmove();
      break;     
    case 114:
       right(); 
       delay(2000);
      notmove();
     break;
   case 98:
       reverse();
       break;
     case 115:
       notmove();
     break;
     }
    }
  } 





void straight(){

       
    digitalWrite(in1,HIGH);
    digitalWrite(in2,LOW);
    digitalWrite(in3,HIGH);
    digitalWrite(in4,LOW);
    analogWrite (enA, 95);
    analogWrite (enB, 90);
   
}


void reverse(){
     
    digitalWrite(in1,LOW);
    digitalWrite(in2,HIGH);
    digitalWrite(in3,LOW);
    digitalWrite(in4,HIGH);
    analogWrite (enA, 105);
    analogWrite (enB, 100);
}

void notmove(){
      //Stop both Motors
    digitalWrite(in1,LOW);
    digitalWrite(in2,LOW);
    digitalWrite(in3,LOW);
    digitalWrite(in4,LOW);
    analogWrite (enA, 0);
    analogWrite (enB, 0);
}

void right(){
  //set to 0
  analogWrite(enA, 91);
  analogWrite(enB, 90);
  //set motor A 
  digitalWrite(in1,LOW);
  digitalWrite(in2,HIGH);
  //set motor B 
  digitalWrite(in3,HIGH);
  digitalWrite(in4,LOW);
}

void left(){
  analogWrite(enA, 90);
  analogWrite(enB, 91);
  //set motor A 
  digitalWrite(in1,HIGH);
  digitalWrite(in2,LOW);
  //set motor B 
  digitalWrite(in3, LOW);
  digitalWrite(in4,HIGH);
}
