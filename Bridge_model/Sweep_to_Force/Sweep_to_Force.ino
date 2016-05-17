#include <Servo.h> 
 
Servo myservo;  // create servo object to control a servo 
                // twelve servo objects can be created on most boards
int Force_sensor=A0;
int servo_pos=9;
int servo_val = 1300;
 
void setup() 
{ 
  Serial.begin(115200);
  myservo.attach(servo_pos);  // attaches the servo on pin 9 to the servo object 
} 
 
void loop() 
{ 
  double val = 15.311 * exp(0.005199 * (analogRead(Force_sensor)))* 9.8 *0.001;
  if (Serial.available() != 0)
  { 
    servo_val = Serial.parseInt();
    if (servo_val != 0)
      {
        myservo.writeMicroseconds(servo_val);
      }
  }
  Serial.println(val);
  delay(30);
} 

