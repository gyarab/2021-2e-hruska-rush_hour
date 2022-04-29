import pygame, sys
from rushhours import* 
pygame.init()

oknoX,oknoY = 600,500
win = pygame.display.set_mode((oknoX,oknoY))

FPS = 60
clock = pygame.time.Clock()

g = Game()

while True:
    pyEventy = []
    clock.tick(FPS)
    for event in pygame.event.get():
        pyEventy.append(event)
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            g.select()
    
    g.move_objects(pyEventy)
    g.draw()