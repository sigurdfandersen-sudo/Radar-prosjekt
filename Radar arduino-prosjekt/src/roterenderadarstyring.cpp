#include <Arduino.h>
#include <Servo.h>

// constants and pins
const int echoPin = 3;
const int trigPin = 10;
const int servoPin = 11;

Servo myServo;

void setup() {

    pinMode(echoPin, INPUT);
    pinMode(trigPin, OUTPUT);
    pinMode(servoPin, OUTPUT);
    myServo.attach(servoPin);

}




