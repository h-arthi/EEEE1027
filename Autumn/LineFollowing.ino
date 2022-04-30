#include<LiquidCrystal.h>

//initialize the pins for my reference
//int rs=8, en=9, d4=4,d5=5,d6=6, d7=7;
//initialize the pins with the lcd library
LiquidCrystal lcd(8,9,4,5,6,7);
 int i;
 int input1;
 int input2;
 int period;
//this is for the car to go straight
int carspeedA = 75;
int carspeedB = 70;
//this is for the car to turn left
int leftspeedA = 10;
int leftspeedB = 91;
//this is for the car to turn right
int rightspeedA = 90;
int rightspeedB =11;


//initilaizing the motor A
int enA = 3;
int in1 = A1;
int in2 = A2;
//initializing motor B
int enB = 11;
int in3 = A3;
int in4 = A4;
//initializing input variables
int IR1 = 1;//ready-made
int IR2 = 2;//diy


//set-up initial status of pins
void setup()
{
  pinMode(enA, OUTPUT);
  pinMode(enB, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);
  pinMode(IR1, INPUT);
  pinMode(IR2, INPUT);
  
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
  lcd.print("Time Elapsed:");

}


void loop()
{
      lcd.setCursor(0,2);
      lcd.print(millis()/1000);

      if(digitalRead(IR1)==LOW && digitalRead(IR2)== HIGH)//WHEN IT DOESNT LIGHT UP
      {
        notmove();
      }
      else if(digitalRead(IR1)== HIGH && digitalRead(IR2) == LOW)//WHEN IT  LIGHT UP
      {  
        if(millis()>50000){
          carspeedA = 125;
          carspeedB= 125;
        }
          else if(millis()>25000){
          carspeedA = 95;
          carspeedB= 90;
        }
        else if(millis()>32000){
          carspeedA = 65;
          carspeedB= 60;
        }
        straight();
      }
    
      else if(digitalRead(IR1)==LOW && digitalRead(IR2)== LOW)//car moves right
      {
          if(millis()>50000){
          rightspeedA = 92;
          rightspeedB = 70;
        }
          else if(millis()>32000){
          rightspeedA = 85;
          rightspeedB = 10;
        }

        right();
      }
 else if(digitalRead(IR1)==HIGH && digitalRead(IR2)== HIGH){//car moves left  
          if(millis()>50000){
          leftspeedA = 30;
          leftspeedB = 90;
        }
         else if(millis()>32000){
          leftspeedA = 10;
          leftspeedB = 85;
        }
        left();
       }
    }







void straight(){

       
    digitalWrite(in1,HIGH);
    digitalWrite(in2,LOW);
    digitalWrite(in3,HIGH);
    digitalWrite(in4,LOW);
    analogWrite (enA, carspeedA);
    analogWrite (enB, carspeedB);
   
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
    analogWrite (enA,rightspeedA);
    analogWrite (enB, rightspeedB);
}

void left(){
      //Tilt robot towards left by stopping the left wheel and moving the right one
    digitalWrite(in1,HIGH);     
    digitalWrite(in2,LOW);
    digitalWrite(in3,LOW);
    digitalWrite(in4,LOW);
    analogWrite (enA, leftspeedA);
    analogWrite (enB, leftspeedB);
}
