import pygame
import math
import sys
import serial

pygame.init()
screen = pygame.display.set_mode((800, 600))
ser = serial.Serial('')
clock = pygame.time.Clock()

while True:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                ser.write(b'L')
            if  event.key == pygame.K_right:
                ser.write(b'R')





