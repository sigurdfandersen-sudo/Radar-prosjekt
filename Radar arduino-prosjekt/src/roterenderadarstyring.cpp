#include <Arduino.h>
#include <Servo.h>

// constants and pins
const int echoPin = 3;
const int trigPin = 10;
const int servoPin = 11;
const float soundSpeed = 0.0345;
Servo myServo;

unsigned long radarTime;
unsigned long radarDistance;
void setup() {

    pinMode(echoPin, INPUT);
    pinMode(trigPin, OUTPUT);
    pinMode(servoPin, OUTPUT);
    myServo.attach(servoPin);
    Serial.begin(9600);
}

void radarRead(){
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);

    radarTime = pulseIn(echoPin, HIGH, 25000);
    radarDistance = soundSpeed * radarTime / 2;
}

void loop(){
    if (Serial.available() > 0) {   //checks if there are any new messages from python
        String receivedText = Serial.readStringUntil('\n');
        int receivedAngle = receivedText.toInt();
        myServo.write(receivedAngle);
        radarRead();
        Serial.print(receivedAngle);
        Serial.print(",");
        Serial.println(radarDistance);



    }
}





