import pygame
import math
import sys
import serial

pygame.init()
screen = pygame.display.set_mode((800, 600))
ser = serial.Serial('COM3', 9600, timeout = 1) #tell which port to send info with Arduino
clock = pygame.time.Clock() #FPS

while True:
    clock.tick(30) #FPS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                ser.write(b'L')
                print("Kommando: Venstre")
            elif  event.key == pygame.K_RIGHT:
                ser.write(b'R')
                print("Kommando: Høyre")

    if ser.in_waiting > 0: #sjekker om det har kommet ny data inn i bufferen
        line = ser.readline().decode('utf_8').strip() #Reading data from Arduino, ser.readline gather raw bytes, decode makes it as text, strip deletes hidden text
        angle, distance, message = line.split(',')
        angle = int(angle)
        angle_rad = math.radians(angle)
        distance = int(distance)

        print(f"Angle:"{angle}, "Distance:"{distance}, "Message:"{message})


    pygame.display.flip() #Update the frame




