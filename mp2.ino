#include <Servo.h>
 
Servo tilt_servo;
Servo pan_servo;
 
int inputPin = A0;  
int pan_interval = 50;
int tilt_interval = 50;
int pan_increment = 1;
int tilt_increment = 1;
int pan_angle = 0;   
int tilt_angle = 0;  
bool pan_direction = true;
bool tilt_direction = true;
bool tilt_changed = false;
int min_pan_angle = 60;
int min_tilt_angle = 50;
int max_pan_angle = 120; 
int max_tilt_angle = 120;
bool set_start_pos = true;
bool done = false;
 
void setup() {
  tilt_servo.attach(9);  
  pan_servo.attach(10); 
  Serial.begin(9600);
}
 
void loop() {
  if (set_start_pos){
    tilt_servo.write(min_tilt_angle);
    pan_servo.write(min_pan_angle);
    set_start_pos = false;
  }else if (not done){
    tilt_changed = false;
    if (pan_angle >= max_pan_angle){
      pan_angle = max_pan_angle;
      pan_direction = false;
      check_tilt();
    }else if (pan_angle <= min_pan_angle) {
      pan_angle = min_pan_angle;
      pan_direction = true;
	    check_tilt();
    }
    
    if (tilt_changed) {
      tilt_angle += tilt_increment;
      tilt_servo.write(tilt_angle);  
      delay(tilt_interval);
      read_IR();
    }
 
    if (pan_direction) {
      pan_angle += pan_increment;
    } else {
      pan_angle -= pan_increment;
    }
    pan_servo.write(pan_angle); 
    delay(pan_interval);
    read_IR();
  }
}
 
void check_tilt() {
  if (tilt_angle >= max_tilt_angle){
    tilt_angle = max_tilt_angle;
    tilt_direction = false;
    done = true; // exit because scan is finished
  }else if (tilt_angle <= min_tilt_angle) {
    tilt_angle = min_tilt_angle;
    tilt_direction = true;
  }
  if (tilt_direction) {
    tilt_changed = true;
  }
}
 
void read_IR(){
  int sum = analogRead(inputPin);
  Serial.print(pan_angle);
  Serial.print(",");
  Serial.print(tilt_angle);
  Serial.print(",");
  Serial.println(sum);
}
