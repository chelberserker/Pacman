"""
Program Author: chelberserker
Commented by: carlossantana3279
"""
import sys
import pygame
from pygame.locals import *
from math import floor
import random


def init_window():
        """
        Initialize the Window settings for the game. Setting the
        windows title and window size.
        """
        pygame.init()
        pygame.display.set_mode((512, 512))
        pygame.display.set_caption('Packman')


def draw_background(scr, img=None):
        """
        Drawing the background for the Pacman Game
        """
        if img:
                scr.blit(img, (0, 0))
        else:
                bg = pygame.Surface(scr.get_size())
                bg.fill((0, 0, 0))
                scr.blit(bg, (0, 0))


class GameObject(pygame.sprite.Sprite):
        """
        A Parent class from which our game elements such as Ghosts and 
        the player(pacman) will inherate from. Has methods for setting
        the objects position, drawing the opject, and having a "tick"(updating
        the game logic). 
        """

        def __init__(self, img, x, y, tile_size, map_size):
                pygame.sprite.Sprite.__init__(self)
                self.image = pygame.image.load(img)
                self.screen_rect = None
                self.x = 0
                self.y = 0
                self.tick = 0
                self.tile_size = tile_size
                self.map_size = map_size
                self.set_coord(x, y)

        #set the coordinates of the game object
        def set_coord(self, x, y):
                self.x = x
                self.y = y
                self.screen_rect = Rect(floor(x) * self.tile_size, floor(y) * self.tile_size, self.tile_size, self.tile_size )

        #increase the gameobjects internal game logic time
        def game_tick(self):
                self.tick += 1

        #draw the object
        def draw(self, scr):
                scr.blit(self.image, (self.screen_rect.x, self.screen_rect.y))



class Ghost(GameObject):
        """"
        Ghost class is used for creating the ghost enemies
        in the game. 
        """

        def __init__(self, x, y, tile_size, map_size):
                GameObject.__init__(self, './resources/ghost.bmp', x, y, tile_size, map_size)
                self.direction = 0                # 0 - неподвижно, 1 - вправо, 2 = вниз, 3 - влево, 4 - вверх
                self.velocity = 4.0 / 10.0        # Скорость в клетках / игровой тик

        #increase the gameobjects internal game logic time
        def game_tick(self):
                super(Ghost, self).game_tick()


                #if block for moving pacman in different directions
                #directoin 0 = choose a direction to go in
                #direction 1 = moving right
                #direction 2 = moving up
                #direction 3 = moving left
                #direction 4 - moving down
                if self.tick % 20 == 0 or self.direction == 0: # Каждые 20 тиков случайно выбираем направление движения. Вариант self.direction == 0 соотвествует моменту первого вызова метода game_tick() у обьекта
                        self.direction = random.randint(1, 4)

                if self.direction == 1:                        # Для каждого направления движения увеличиваем координату до тех пор пока не достгнем стены. Далее случайно меняем напрвление движения
                        self.x += self.velocity
                        if self.x >= self.map_size-1:
                                self.x = self.map_size-1
                                self.direction = random.randint(1, 4)
                elif self.direction == 2:
                        self.y += self.velocity
                        if self.y >= self.map_size-1:
                                self.y = self.map_size-1
                                self.direction = random.randint(1, 4)
                elif self.direction == 3:
                        self.x -= self.velocity
                        if self.x <= 0:
                                self.x = 0
                                self.direction = random.randint(1, 4)
                elif self.direction == 4:
                        self.y -= self.velocity
                        if self.y <= 0:
                                self.y = 0
                                self.direction = random.randint(1, 4)
                
                #update the ghosts position
                self.set_coord(self.x, self.y)


class Pacman(GameObject):
    """
    The Pacman class is for the pacman character that
    our player will be playing. Has methods for eating
    ghosts(swallow) and updating the game tick (updating 
    the game logic).
    """

    def __init__(self, x, y, tile_size, map_size):
        GameObject.__init__(self, './resources/timofey.bmp', x, y, tile_size, map_size)
        self.direction = 0              #at 0 pacman is not moving (nuetral state)
        self.velocity = 1               #pacmans speed
        self.bonus = 0

    #method for when you eat ghosts!
    def swallow(self):
        super(Pacman, self).game_tick()
        """
        if self.x >= Wall.x-1:
            self.velocity = 0
        if self.y >= Wall.y-1:
            self.velocity = 0
        """
        if self.bonus != 10:
            for i in range(len(food)):
                if (self.x == food[i].x)and(self.y == food[i].y):
                    food[i].x = food[i].y = 30
                    self.bonus += 1
                    print(i, food[i].x, self.bonus)
        else:
            exit(0)

    #method for updating the game logic each tick
    def game_tick(self):
        super(Pacman, self).game_tick()
        x1 = self.x
        y1 = self.y

        #if block for moving pacman in different directions
        #direction 1 = moving right
        #direction 2 = moving up
        #direction 3 = moving left
        #direction 4 - moving down
        if self.direction == 1:
            self.x += self.velocity
            if self.x >= self.map_size-1:
                self.x = self.map_size-1
        elif self.direction == 2:
            self.y += self.velocity
            if self.y >= self.map_size-1:
                self.y = self.map_size-1
        elif self.direction == 3:
            self.x -= self.velocity
            if self.x <= 0:
                self.x = 0
        elif self.direction == 4:
            self.y -= self.velocity
            if self.y <= 0:
                self.y = 0

        #for keeping pacman within bounds and not able to move through walls        
        for wall in thewall:
            if self.x == wall.x and self.y == wall.y:
                self.x = x1
                self.y = y1

        #check if you can eat a ghost
        self.swallow()

        #update pacmans coordinates
        self.set_coord(self.x, self.y)



def process_events(events, packman):
    """ 
    This method handles all the input from the user.
    Includes the arrow keys and exiting the program.
    """

    for event in events:    

        #if the player presses certain keys to quit the program
        if (event.type == QUIT) or (event.type == KEYDOWN and event.key == K_ESCAPE):
            sys.exit(0)

        #handling all the input for moving pacman
        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                packman.direction = 3
            elif event.key == K_RIGHT:
                packman.direction = 1
            elif event.key == K_UP:
                packman.direction = 4
            elif event.key == K_DOWN:
                packman.direction = 2
            elif event.key == K_SPACE:
                packman.direction = 0


class Food(GameObject):
    """
    Food objects for the pacman to eat
    """
    def __init__(self, x, y, tile_size, map_size):
        GameObject.__init__(self, './resources/food.bmp', x, y, tile_size, map_size)


class Map:
        """
        Class that creates and holds the map information
        """
        def __init__(self, w, h):
                self.map = [[list()]*x for i in range(y)]

        # Функция возвращает список обьектов в данной точке карты
        def get(self, x, y):
                return self.map[x][y]

class Wall(GameObject):
    """
    Wall object that is used for drawing the walls in 
    the game.
    """
    def __init__(self, x, y, tile_size, map_size):
        GameObject.__init__(self, './resources/wall.bmp', x, y, tile_size, map_size)

"""
def process_events(events):
        for event in events:
                if (event.type == QUIT) or (event.type == KEYDOWN and event.key == K_ESCAPE):
                        sys.exit(0)
"""

"""
* THE MAIN PROGRAM *
"""
if __name__ == '__main__':
        #Open the window for the prgram
        init_window()

        #set up all the information for the map
        tile_size = 32
        map_size = 16
        map_file = open('map.txt', 'r')
        food_file = open('food.txt', 'r')

        #Variable and chracters for our game
        pacman = Pacman(1, 1, tile_size, map_size)
        thewall = []
        ghost = []                              #Array for our enemies
        food = []
        number_of_ghosts = 2                

        #variables used for setting up the game and map
        A = map_file.readlines()
        B = food_file.readlines()

        #Setting the walls in our map
        for i in range(len(A)-1):
            A[i] = list(map(int, A[i].split()))
            thewall.append(Wall(A[i][0], A[i][1], tile_size, map_size))
        
        #setting up the ghosts
        for i in range(number_of_ghosts):
            ghost.append(Ghost(random.randint(1, 15), random.randint(1, 15), tile_size, map_size))
        
        #setting the food in the game
        for i in range(len(B)):
            B[i] = list(map(int, B[i].split()))
            food.append(Food(B[i][0], B[i][1], tile_size, map_size))
        
        #draw the background
        background = pygame.image.load("./resources/background.bmp")
        screen = pygame.display.get_surface()

        """Where all the realtime logic and playing of the game
        happens. Keeps runnnig forever until the user exits the 
        program.
        """
        while 1:
                process_events(pygame.event.get(), pacman)
                pygame.time.delay(100)

                #manage all of the ghosts, update their game logic
                for i in range(len(ghost)):
                    ghost[i].game_tick()
                
                #update the logic for the pacman
                pacman.game_tick()
               
                #draw the background first
                draw_background(screen, background)
               
                #draw the all walls in our map
                for i in range(len(thewall)):
                    thewall[i].draw(screen)

                #draw the all the food in our game
                for i in range(len(food)):
                   # if food[i].existance == 1:
                    food[i].draw(screen)

                #draw all the ghosts in our game
                for i in range(len(ghost)):
                    ghost[i].draw(screen)
                
                #draw pacman last (on top of all the other objects in our scence)
                pacman.draw(screen)
                
                #update the screen
                pygame.display.update()
