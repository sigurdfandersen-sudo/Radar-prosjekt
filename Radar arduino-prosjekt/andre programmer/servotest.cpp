#include <Arduino.h>
#include <Servo.h>

Servo myServo;
int vinkel = 0;
int vinkelendring = 6;
unsigned long dt = 300;
unsigned long naatid = 0;
unsigned long sistmalttid = 0;

void setup()
{
    pinMode(9, OUTPUT);
    Serial.begin(9600);
    myServo.attach(9);
}
void loop()
{
    naatid = millis();

    if (naatid - sistmalttid > dt){
        vinkel = vinkel + vinkelendring;
        if (vinkel > 175 || vinkel < 5) {
            vinkelendring = vinkelendring * -1;
        }
        myServo.write(vinkel);
        sistmalttid = naatid;
        Serial.println(vinkel);
    }
}
