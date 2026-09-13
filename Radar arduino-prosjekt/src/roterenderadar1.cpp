#include <Arduino.h>
#include <Servo.h>

//pinner
const int servopinne = 11; //output
const int trigpinne = 10;  //output
const int ekkopinne = 3;   //input

Servo minServo;

//konstanter
const unsigned long radarintervall = 50;
const float lydhastighet = 0.0345;
int vinkelendring = 5;
int vinkel = 0;
unsigned long distanse = 0;
unsigned long sistmaaltid = 0;
unsigned long naatid = 0;

void radarFunksjon(){

    digitalWrite(trigpinne, LOW);
    delayMicroseconds(2);
    digitalWrite(trigpinne, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigpinne, LOW);

    unsigned long radartid = pulseIn(ekkopinne, HIGH, 25000);
    distanse = radartid * lydhastighet / 2;

}

void servokontroll(){
    vinkel = vinkel + vinkelendring;
    if (vinkel >= 180 || vinkel <= 0){
        vinkelendring = vinkelendring * -1;
    }
    minServo.write(vinkel);

}

void setup()
{
    pinMode(servopinne, OUTPUT);
    pinMode(trigpinne, OUTPUT);
    pinMode(ekkopinne, INPUT);
    Serial.begin(9600);
    minServo.attach(servopinne);
}

void loop(){
    naatid = millis();

    if (naatid - sistmaaltid > radarintervall) {
        servokontroll();
        delayMicroseconds(10);
        radarFunksjon();
        sistmaaltid = naatid;
        Serial.print(vinkel);
        Serial.print(",");
        Serial.println(distanse);
        
    }
}