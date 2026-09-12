#include <Arduino.h>
#include <Servo.h>


//dette er bare øving for bruk av servomotor og koding og design er fra arduino-boken
Servo  myServo;

int const potPin = A0;
int potVal;
int angle;

void setup()
{
    myServo.attach(9);

    Serial.begin(9600);
}

void loop()
{
    potVal = analogRead(potPin);
    Serial.print("potval =");
    Serial.print(potVal);
    angle = map(potVal, 0, 1023, 0, 179);
    Serial.print(",angle:");
    Serial.print(angle);

    myServo.write(angle);
    delay(15);
}