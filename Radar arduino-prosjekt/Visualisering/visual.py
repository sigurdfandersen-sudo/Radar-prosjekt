import pygame #Det visuelle grensesnittet, selve vinduet, 
import sys #Systemkommandoer, 
import serial #for hente data fra com3 arduino
import math #håndtere matte, trig og vinkel


#Setter opp pygame sine interne systemer, som vindu, variabel
pygame.init()
skjerm = pygame.display.set_mode((800, 600)) #lagre variabel for farger senere
ser = serial.Serial('COM3', 9600, timeout=1)

while True:
    for event in pygame.event.get(): #Pygame hendelser handler kun om hva brukeren gjør vinduet og tastatur
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if ser.in_waiting > 0: #sjekker om det har kommet ny data inn i bufferen
        linje = ser.readline().decode('utf-8').strip() #leser data frem til linjeskift. ser.readline henter den råe dataen, decode gjør det om til tekst, strip fjerner usynlig linjeskift
        try: 
            vinkel_str, distanse_str, melding = linje.split(',') #
            vinkel = int(vinkel_str)
            distanse = int(distanse_str)
            print(f"Vinkel: {vinkel}, Distanse:{distanse} cm, Status:{melding}")
        except ValueError:
            pass

        print(f"Vinkel: {vinkel}, Distanse:{distanse} cm, Status:{melding}") 

    skjerm.fill((10, 30, 10))
    pygame.display.flip()
