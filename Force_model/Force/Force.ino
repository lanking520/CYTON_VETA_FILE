/* Sweep
 by BARRAGAN <http://barraganstudio.com> 
 This example code is in the public domain.

 modified 8 Nov 2013
 by Scott Fitzgerald
 http://arduino.cc/en/Tutorial/Sweep
*/ 

int force_sensor=A0;
double previous_val = 0.0;
double a = 0;
void setup() 
{ 
  force_sensor=A0;
  Serial.begin(115200);
} 
 
void loop() 
{ 
  a = 15.311 * exp(0.005199 * (analogRead(force_sensor)))* 9.8 *0.001;
    Serial.println(a);
  delay(30);
}


