import pygame
import math
import sys
import serial

pygame.init()
screen = pygame.display.set_mode((800, 600))
ser = serial.Serial('COM6', 9600, timeout = 1) #tell which port to send info with Arduino
clock = pygame.time.Clock() #FPS
angle_send = 0
d_angle_send = 0

while True:
    clock.tick(30) #FPS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                if angle_send >= 3:
                    d_angle_send = -3
                    angle_send += d_angle_send
                    angle_str = str(angle_send)
                    angle_text = angle_str + "\n"
                    angle_bytes = angle_text.encode("ascii")
                    ser.write(angle_bytes)
                    print("Kommando: Venstre")


            elif  event.key == pygame.K_RIGHT:
                if angle_send <= 177:
                    d_angle_send = 3
                    angle_send += d_angle_send
                    angle_str = str(angle_send)
                    angle_text = angle_str + "\n"
                    angle_bytes = angle_text.encode("ascii")
                    ser.write(angle_bytes)
                    print("Kommando: Høyre")
                    


            

    if ser.in_waiting > 0: #sjekker om det har kommet ny data inn i bufferen
        line = ser.readline().decode('utf_8').strip() #Reading data from Arduino, ser.readline gather raw bytes, decode makes it as text, strip deletes hidden text
        angle, distance = line.split(',')
        angle = int(angle)
        angle_rad = math.radians(angle)
        distance = int(distance)
        print(f"Angle: {angle}, Distance: {distance}")  #{} means put the value of the variable here


    pygame.display.flip() #Update the frame





