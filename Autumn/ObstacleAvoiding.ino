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
//initializing input variables
int trigPin = 12;
int echoPin = 13;

float duration, distance;


//set-up initial status of pins
void setup()
{
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
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("Look at me goooo!");
  Serial.begin(9600);

}


void loop()
{
  digitalWrite(trigPin, LOW);
  delayMicroseconds(10);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  duration = pulseIn(echoPin, HIGH);
  distance = (duration * 0.0343)/2;
if (distance > 50){
  straight(); 
}
else if (distance<50){
  notmove();
  delay(1000);
  reverse();
  delay(1000);
  right();
  delay(1000);
}
  Serial.println(distance);
  delay(1000);
}














void straight(){

       
    digitalWrite(in1,HIGH);
    digitalWrite(in2,LOW);
    digitalWrite(in3,HIGH);
    digitalWrite(in4,LOW);
    analogWrite (enA, 105);
    analogWrite (enB, 100);
   
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
      //Tilt robot towards right by stopping the right wheel and moving the left one
    digitalWrite(in1,LOW);     // If I want to turn right then the speed of the right wheel should be less than that of the left wheel, here, let a be the right wheel
    digitalWrite(in2,LOW);
    digitalWrite(in3,HIGH);
    digitalWrite(in4,LOW);
    analogWrite (enA,91);
    analogWrite (enB,10);
}

void left(){
      //Tilt robot towards left by stopping the left wheel and moving the right one
    digitalWrite(in1,HIGH);     
    digitalWrite(in2,LOW);
    digitalWrite(in3,LOW);
    digitalWrite(in4,LOW);
    analogWrite (enA, 10);
    analogWrite (enB, 91);
}
