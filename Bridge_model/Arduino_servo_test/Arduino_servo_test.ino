#include <VarSpeedServo.h>
 
VarSpeedServo myservo;  // create servo object to control a servo 
//Servo myservo_2;               
int servo_pos=9;
 
void setup() 
{ 
  Serial.begin(115200);
  myservo.attach(servo_pos);  // attaches the servo on pin 9 to the servo object 
} 
 
void loop() 
{ 
  for (int j = 40;  j <= 255; j +=20)
  {
    Serial.print("Now Step to Velocity");
    Serial.println(j);
    for (int i = 30; i <= 80; i+=10)
    {
      myservo.write(i,j,true);
      delay(30);
    }
  }
  delay(3000);
  
} 

