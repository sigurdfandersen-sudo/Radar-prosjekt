import pygame
import math
import sys
import serial

# Colors: RGB values range from 0 to 255.
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
orange = (255, 165, 0)
purple = (128, 0, 128)
cyan = (0, 255, 255)
gray = (128, 128, 128)
dark_green = (10, 30, 10)

pygame.init()
screen = pygame.display.set_mode((1000, 775))
ser = serial.Serial('COM6', 9600, timeout = 1) #tell which port to send info with Arduino
clock = pygame.time.Clock() #FPS
angle_send = 0
d_angle_send = 0

font = pygame.font.SysFont('Arial', 20)
rectangel_info = (0, 0, 200, 100)

angle = 0
distance = 0


while True:
    clock.tick(30) #FPS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                if angle_send >= 5:
                    d_angle_send = -5
                    angle_send += d_angle_send
                    angle_str = str(angle_send)
                    angle_text = angle_str + "\n"
                    angle_bytes = angle_text.encode("ascii")
                    ser.write(angle_bytes)
                    print("Kommando: Venstre")


            elif  event.key == pygame.K_RIGHT:
                if angle_send <= 175:
                    d_angle_send = 5
                    angle_send += d_angle_send
                    angle_str = str(angle_send)
                    angle_text = angle_str + "\n"
                    angle_bytes = angle_text.encode("ascii")
                    ser.write(angle_bytes)
                    print("Kommando: Høyre")
                    


            

    if ser.in_waiting > 0: #sjekker om det har kommet ny data inn i bufferen
        line = ser.readline().decode('utf_8').strip() #Reading data from Arduino, ser.readline gather raw bytes, decode makes it as text, strip deletes hidden text
        try:
            angle, distance = line.split(',')
            angle = int(angle)
            angle_rad = math.radians(angle)
            distance = int(distance)

            print(f"Angle: {angle}, Distance: {distance}")  #{} means put the value of the variable here


        except ValueError:
            pass

        


    screen.fill((10, 30, 10))
    pygame.draw.rect(screen, black, rectangel_info)

    angle_text = str(angle)
    distance_text = str(distance)
    angle_distance_screen = ("Angle: " + angle_text + "   Distance: " + distance_text) 
    text_info_screen = font.render(angle_distance_screen, True, white)
    screen.blit(text_info_screen, (0, 0))






    pygame.display.flip() #Update the frame
    
    





