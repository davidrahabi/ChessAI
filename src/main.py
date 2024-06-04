import pygame
import sys
from const import *
from game import Game

class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT)) #creates screen
        pygame.display.set_caption('Chess')
        self.game = Game()

    def mainloop(self):
        while True:
            self.game.show_bg(self.screen)  #this loop will keep running and continually update teh screen

            for event in pygame.event.get(): #looks through all possible game events (user actions)
                if event.type ==pygame.QUIT: #if event is a quit by the user, end game
                    pygame.quit()
                    sys.exit()
            pygame.display.update() #updates screen

main = Main()

main.mainloop()