
#include <Servo.h> 
 
Servo myservo;  // create servo object to control a servo 
                // twelve servo objects can be created on most boards
int Force_sensor=A0;
int servo_pos=9;
int servo_val = 80;
 
void setup() 
{ 
  Serial.begin(115200);
  myservo.attach(servo_pos);  // attaches the servo on pin 9 to the servo object 
} 
 
void loop() 
{ 
  double val = 15.311 * exp(0.005199 * (analogRead(Force_sensor)))* 9.8 *0.001;
        myservo.writeMicroseconds(1300);
        //Local minimum 800, Local Maximum 1500, safe as 850-1300
  delay(30);
} 

