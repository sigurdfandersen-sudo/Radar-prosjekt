#include <Arduino.h>

//definerer pinner
const int RETURPINNE = 3;
const int TRIGGERPINNE = 5;
const int LED_LANGT = 11;
const int LED_MIDDELS = 10;
const int LED_KORT = 9;
const int LYD_PINNE = 6;

float sistDistanse = -1; //Lagre siste distansen, -1 for å sjekke feil, ugyldig svar

//tidsstyring for radar-funksjonen
unsigned long sistmalttid = 0; //unsigned sier at det bare er positive tall, slik at vi kan nytte høyere tall
const long RADAR_INTERVALL  = 50;  //Måler ny distanse hver 50ms, tilsvarer 20 ganger i sekundet

//Tidsstyring for blinke-funksjonen
unsigned long sistBlinkTid = 0;
bool ledTilstand = LOW;  //holde styr på om aktiv LED er på eller av

//Radar-funksjonen
void kjarRadarMaaling()
{
    digitalWrite(TRIGGERPINNE, LOW);
    delayMicroseconds(2);
    digitalWrite(TRIGGERPINNE, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIGGERPINNE, LOW);

    long radarTid = pulseIn(RETURPINNE, HIGH, 25000);
    //Distanse måling
    if (radarTid == 0)
    {
        sistDistanse = -1; //fortelle om ugyldighet

    }
    else 
    {
        sistDistanse = radarTid * 0.0345 / 2.0; // S=V*T. Må dele på to siden lyden går frem og tilbake

    }

}

void blinkeFunksjon()
{
    int aktivPinne = -1;
    unsigned long blinkeIntervall = 0;
    int frekvens = 0;

    if (sistDistanse > 225)
    {
        aktivPinne = LED_LANGT;
        blinkeIntervall = 500;
        frekvens = 800;

    }
    else if (sistDistanse >= 114)
    {
        aktivPinne = LED_MIDDELS;
        blinkeIntervall = 250;
        frekvens = 1000;
    }
    else if (sistDistanse > 0)
    {
        aktivPinne = LED_KORT;
        blinkeIntervall = 80;
        frekvens = 1200;
    }

    if (aktivPinne == -1) //Skrur av alle lys hvis ingen av kravene blir oppfylt
    {
        digitalWrite(LED_LANGT, LOW);
        digitalWrite(LED_MIDDELS, LOW);
        digitalWrite(LED_KORT, LOW);
        noTone(LYD_PINNE);
        return; 
    }
    unsigned long naatid = millis(); //Teller millisekunder siden Arduinoen startet
    if (naatid - sistBlinkTid > blinkeIntervall) 
    {
        ledTilstand = !ledTilstand;
        sistBlinkTid = naatid;

        digitalWrite(LED_LANGT, LOW);
        digitalWrite(LED_MIDDELS, LOW);
        digitalWrite(LED_KORT, LOW);
        if (ledTilstand == HIGH)
        {
            digitalWrite(LYD_PINNE, HIGH);
            tone(LYD_PINNE, frekvens);
            digitalWrite(aktivPinne, ledTilstand);
        }
        else 
        {
            digitalWrite(aktivPinne, LOW);
            digitalWrite(LYD_PINNE, LOW);
            noTone(LYD_PINNE);
        }
    } 
}

void setup()
{
    pinMode(LED_LANGT, OUTPUT);
    pinMode(LED_MIDDELS, OUTPUT);
    pinMode(LED_KORT, OUTPUT);
    pinMode(TRIGGERPINNE, OUTPUT);
    pinMode(LYD_PINNE, OUTPUT);
    pinMode(RETURPINNE, INPUT);

    Serial.begin(9600);
}

//Total løkke
void loop()
{
    unsigned long naatid = millis();
    if (naatid - sistmalttid > RADAR_INTERVALL)
    {
        sistmalttid = naatid;
        kjarRadarMaaling();

        if (sistDistanse >= 10 && sistDistanse <= 250)
        {
            Serial.print("Distanse er ..");
            Serial.print(sistDistanse); 
            Serial.println("cm");
        }
        else 
        {
            Serial.print("FEIL. Ingen data returnet, ugdyldig data");
        }
    }
    blinkeFunksjon();
}
//dette er en sjekk