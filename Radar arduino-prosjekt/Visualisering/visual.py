import pygame #Det visuelle grensesnittet, selve vinduet, 
import sys #Systemkommandoer, 
import serial #for hente data fra com3 arduino
import math #håndtere matte, trig og vinkel


#Setter opp pygame sine interne systemer, som vindu, variabel
pygame.init()
skjerm = pygame.display.set_mode((800, 600)) #lagre variabel for farger senere
ser = serial.Serial('COM3', 9600, timeout=1)
font = pygame.font.SysFont('Arial', 20)
font2 = pygame.font.SysFont('Arial', 50)
sentrum_x = 400
sentrum_y = 500
skalering_pil = 1
skalering_ruter = 1
x_kordinat = 400
y_kordinat = 500

x_sweep = 0
y_sweep = 0
#Farger
mørk_grønn = (0, 255, 0)
rød = (255, 0, 0)
hvit = (255, 255, 255)

maks_distanse = 400
hindring_liste = {}
while True:
    for event in pygame.event.get(): #Pygame hendelser handler kun om hva brukeren gjør vinduet og tastatur
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    

    if ser.in_waiting > 0: #sjekker om det har kommet ny data inn i bufferen
        linje = ser.readline().decode('utf-8').strip() #leser data frem til linjeskift. ser.readline henter den råe dataen, decode gjør det om til tekst, strip fjerner usynlig linjeskift
        try: #Håndterer kun mottak og omregning av data
            vinkel_str, distanse_str, melding = linje.split(',') #Splitter opp linjen ved hvert komma, og lager en liste med bitene
            vinkel = int(vinkel_str) #Gjør om fra tekst til heltall
            distanse = int(distanse_str)

            vinkel_rad = math.radians(vinkel) #Gjør om grader til radianer
            
            x_kordinat = sentrum_x + skalering_pil * distanse * math.cos(vinkel_rad) #skalering brukes for at 1cm skal bli 3 pixler
            y_kordinat = sentrum_y - skalering_pil * distanse * math.sin(vinkel_rad) #Er minus siden origo er øverst til venstre, og vi skal nedover
            x_sweep = sentrum_x + skalering_pil * maks_distanse * math.cos(vinkel_rad)
            y_sweep = sentrum_y - skalering_pil * maks_distanse * math.sin(vinkel_rad)




            print(f"Vinkel: {vinkel}, Distanse:{distanse} cm, Status:{melding}")
            print(f"X-kordinat: {x_kordinat}, Y-kordinat: {y_kordinat} ")
            hindring_liste[vinkel] = (x_kordinat, y_kordinat)



            

        except ValueError:
            pass


    skjerm.fill((10, 30, 10))

    pygame.draw.line(skjerm, mørk_grønn, (sentrum_x, sentrum_y), (x_kordinat, y_kordinat), 3) #må være plassert her for den skal oppdateres hver eneste runde, uavhengig av data
    pygame.draw.line(skjerm, (150,0,150), (sentrum_x, sentrum_y), (x_sweep, y_sweep), 2)
    pygame.draw.line(skjerm, mørk_grønn, ((sentrum_x - 400, sentrum_y)), (sentrum_x + 400, sentrum_y), 2)
    pygame.draw.line(skjerm, mørk_grønn, (sentrum_x, sentrum_y), (sentrum_x + math.cos(3.14/2) * maks_distanse * skalering_pil, sentrum_y - math.sin(3.14/2) * maks_distanse * skalering_pil), 1)
    
    pygame.draw.circle(skjerm, mørk_grønn, (400, 500), 400 * skalering_ruter, 1)
    pygame.draw.circle(skjerm, mørk_grønn, (400, 500), 300 * skalering_ruter , 1)
    pygame.draw.circle(skjerm, mørk_grønn, (400, 500), 200 * skalering_ruter, 1)
    pygame.draw.circle(skjerm, mørk_grønn, (400, 500), 100 * skalering_ruter, 1)
    pygame.draw.circle(skjerm, rød, (x_kordinat, y_kordinat), 5, 5) 
    tekst_100cm = font.render("100cm", True, hvit)
    tekst_200cm = font.render("200cm", True, hvit)
    tekst_300cm = font.render("300cm", True, hvit)
    tekst_400cm = font.render("400cm", True, hvit)
    overskrift = font2.render("Radarmåling", True, hvit)

    skjerm.blit(tekst_100cm, (sentrum_x - 100, sentrum_y))
    skjerm.blit(tekst_200cm, (sentrum_x - 200, sentrum_y))
    skjerm.blit(tekst_300cm, (sentrum_x - 300, sentrum_y))
    skjerm.blit(tekst_400cm, (sentrum_x - 400, sentrum_y))
    skjerm.blit(overskrift, (sentrum_x - 100, 0))

    for punkt in hindring_liste.values():
        pygame.draw.circle(skjerm, rød, (int(punkt[0]),int(punkt[1])), 2, 2)

    vinkler = sorted(hindring_liste.keys())
    forrige_kordinat = None

    for vinkel in vinkler:
        ny_kordinat = hindring_liste[vinkel]

        if forrige_kordinat is not None:
            start_punkt = (int(ny_kordinat[0]), int(ny_kordinat[1]))
            slutt_punkt = (int(forrige_kordinat[0]), int(forrige_kordinat[1]))


            pygame.draw.line(skjerm, rød, start_punkt, slutt_punkt, 1)
        forrige_kordinat = ny_kordinat   

    pygame.display.flip()