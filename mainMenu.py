import pygame
from textures import bot_texture, texture1, texture2, texture3, texture4, texture5

pygame.init()
pygame.display.set_caption("rush hours")

oknoX,oknoY = 600,500
win = pygame.display.set_mode((oknoX,oknoY))
tile = pygame.image.load("C:/Users/fifah/Desktop/ročníkovka/tile.jpg")
marioTile = pygame.image.load("C:/Users/fifah/Desktop/ročníkovka/mariotile.jpg")

#obdelníky potřebné pro metodu collidepoint
mainRect1 = pygame.draw.rect(win, (100,0,0), pygame.Rect(oknoX//2 - 125,oknoY//3*1 - 85,250,150),2) 
mainRect2 = pygame.draw.rect(win, (100,0,0), pygame.Rect(oknoX//2 - 125,oknoY//3*2 - 70,250,150),2)

####################################################################################

#class pro vytvoření rects v metodě readMap_createObj, leva/prava/hore/dole - bool pro pohyb v botovi
class Obdelnik(pygame.Rect):
    def __init__(self,x,y,width,height):
        super().__init__(x,y,width,height)   
        self.x = x*50
        self.y = y*50
        self.width = width*50
        self.height = height*50
        
        if self.height > self.width:
            self.stoji = True
            self.hore = True
            self.dole = True
            self.prava = False
            self.leva = False

        elif self.height < self.width:
            self.stoji = False
            self.prava = True
            self.leva = True
            self.hore = False
            self.dole = False
            
class Game():
    def __init__(self):
        self.gamemode = "Main"
        self.radioactive = None
        self.mapa, self.obdelniky, self.tracker = [], [], []
        for i in range(1,9):
            self.tracker.append([" "," "," "," "," "," "," "," ",])
        self.frajer = None
        self.index = 0
        self.zasobnik = []
    
    def readMap_createObj(self,mapInput):
        radek = []
        for i in mapInput:                                           
            if i == "\n":
                if len(radek) != 0:
                    self.mapa.append(radek)
                    radek = []
            else: 
                radek.append(i)
        self.mapa.append(radek)

        for y in range(len(self.mapa)):
            for x in range(len(radek)):
                if self.mapa[y][x] == "#":
                    win.blit(tile,(x * 50, y * 50))
                    
                if self.mapa[y][x] != " " and self.mapa[y][x] != "#" and self.mapa[y][x] != "F":
                    self.tracker[y][x] = self.mapa[y][x]
                    if self.mapa[y][x] == self.mapa[y][x+1]: # sirokej
                        i = 2
                        while True:
                            if self.mapa[y][x] == self.mapa[y][x+i]:
                                i += 1
                                self.tracker[y][x] = self.mapa[y][x]
                                
                            else: #mazání kvůli následnému problému s průchodem
                                self.obdelniky.append(Obdelnik(x,y,i,1))

                                for sirka in range(i):
                                    self.tracker[y][x + sirka] = self.mapa[y][x + sirka]
                                    self.mapa[y][x + sirka] = " "
                                break
                            
                    elif self.mapa[y][x] ==  self.mapa[y+1][x]: # vysokej
                        i = 2
                        while True:
                            if self.mapa[y][x] == self.mapa[y+i][x]:
                                i += 1
                                self.tracker[y][x] = self.mapa[y][x]

                            else:  #mazání kvůli následnému problému s průchodem
                                self.obdelniky.append(Obdelnik(x,y,1,i))
                                for vyska in range(i):
                                    self.tracker[y + vyska][x] = self.mapa[y + vyska][x]
                                    self.mapa[y + vyska][x] = " "
                                break

        #zjištění bloku, který je hlavní
        for i in self.obdelniky:
            if i.x == 50 and i.y == 200:
                self.frajer = i
                self.radioactive = self.frajer

    #metoda pro pohyb(podle inputu z klávesnice
    def podminka(self,eventy):
        if self.gamemode == "Game":
            for event in eventy:
                if event.type == pygame.KEYDOWN:
                    
                    if event.key == pygame.K_UP and self.radioactive.stoji:
                        if self.mapa[self.radioactive.y//50 - 1][self.radioactive.x//50] != "#":
                            self.radioactive.y -= 50
                            for i in self.obdelniky:
                                if i.colliderect(self.radioactive) and i != self.radioactive:
                                    self.radioactive.y += 50

                    elif event.key == pygame.K_DOWN and self.radioactive.stoji:
                        if self.mapa[self.radioactive.y//50 + self.radioactive.height//50][self.radioactive.x//50] != "#":
                            self.radioactive.y += 50
                            for i in self.obdelniky:
                                if i.colliderect(self.radioactive) and i != self.radioactive:
                                    self.radioactive.y -= 50
                                    
                    elif event.key == pygame.K_RIGHT and not self.radioactive.stoji: 
                        if self.mapa[self.radioactive.y//50][self.radioactive.x//50 + self.radioactive.width//50] != "#":
                            self.radioactive.x += 50
                            if self.radioactive == self.frajer and self.mapa[self.radioactive.y // 50][self.radioactive.x//50 + self.radioactive.width//50 - 1] == "F":
                                self.radioactive.x -= 50
                                self.gamemode = "End"
                                self.mapa = []
                            for i in self.obdelniky:
                                if i.colliderect(self.radioactive) and i != self.radioactive:
                                    self.radioactive.x -= 50
                    
                    elif event.key == pygame.K_LEFT and not self.radioactive.stoji:
                        if self.mapa[self.radioactive.y//50][self.radioactive.x//50 - 1] != "#":
                            self.radioactive.x -= 50
                            for i in self.obdelniky:
                                if i.colliderect(self.radioactive) and i != self.radioactive:
                                    self.radioactive.x += 50
                                    
        elif self.gamemode == "Bot":
            self.podminkaBot()

    def return_case(self, poloha):
        s = ""
        for y in range(1,7):
            for x in range(1,7):
                s = s + str(poloha[y][x])
        return s
    
    #metoda, ve které vše potřebné, aby se bot pohyboval
    def podminkaBot(self):
        #check jestli se už tato možnost stala
        #projede pole a zapise string ve kterem jsou napsany moznosti
        s = self.return_case(self.mapa)
        if s in self.zasobnik:
            return False
        else:
            self.zasobnik.append(s)

        #for rect in self.obdelniky:
            #if not rect.stoji:
        print(self.tracker)

        
        
#třída, ve které jsou vščechny potřebné metody na vykreslování rects atd   
class Draw():
    def __init__(self,game):
        self.game = game

    def draw(self):

        if self.game.gamemode == "Game" or self.game.gamemode == "Bot":
            win.fill((35,30,30))
            win.blit(marioTile,(450,200))
            color,selectColor,frajerColor,frajerSelectColor = (150,0,0),(0,150,0),(0,0,220),(255, 0, 255)
            default_color, complete_color = (70,70,70), (0,230,0)
            
            for y in range(len(self.game.mapa)):
                for x in range(len(self.game.mapa[0])):
                    if self.game.mapa[y][x] == "#":
                        win.blit(tile,(x * 50,y * 50))
                  
            #barva se mění podle toho, jaký rect je zvolený
            for obdelnik in self.game.obdelniky:
                if obdelnik == self.game.radioactive:
                    if self.game.frajer == self.game.radioactive:
                        pygame.draw.rect(win, frajerSelectColor, (obdelnik.x+3 , obdelnik.y+3, obdelnik.width-6, obdelnik.height-6))
                    else:
                        pygame.draw.rect(win, selectColor, (obdelnik.x+3 , obdelnik.y+3, obdelnik.width-6, obdelnik.height-6))
                elif obdelnik == self.game.frajer:
                    pygame.draw.rect(win, frajerColor, (obdelnik.x+3 , obdelnik.y+3, obdelnik.width-6, obdelnik.height-6))
                else: 
                    pygame.draw.rect(win, color, (obdelnik.x+3 , obdelnik.y+3, obdelnik.width-6, obdelnik.height-6))
            pygame.draw.rect(win,(60,60,60),(500,0,250,450))
            pygame.display.update()

        elif self.game.gamemode == "Main":
            win.fill((35,30,30))
            mainRect1 = pygame.draw.rect(win, (100,0,0), pygame.Rect(oknoX//2 - 125,oknoY//3*1 - 85,250,150),2) 
            mainRect2 = pygame.draw.rect(win, (100,0,0), pygame.Rect(oknoX//2 - 125,oknoY//3*2 - 70,250,150),2) 
            font = pygame.font.SysFont("Arial", 45)
            text1 = font.render("SinglePlayer", True,(230,230,230))
            text2 = font.render("Bottares", True,(230,230,230))
            pygame.draw.rect(win, (70,70,70), pygame.Rect(mainRect1))
            pygame.draw.rect(win, (70,70,70), pygame.Rect(mainRect2))
            win.blit(text1,(oknoX//2 - 100,oknoY//3*2 - 200))
            win.blit(text2,(oknoX//2 - 70,oknoY//3*1 + 145))
            pygame.display.update()

        elif self.game.gamemode == "End":
            win.fill((0,0,0))
            font2 = pygame.font.SysFont("comicsans", 100)
            font3 = pygame.font.SysFont("javanesetext", 40)
            text3 = font2.render("GAME OVER", True,(230,230,230))
            text4 = font3.render("click to get to the main menu", True,(230,230,230))
            win.blit(text3,(oknoX//2 - 220, oknoY//3))
            win.blit(text4,(oknoX//2 - 250, oknoY//3*2))
            pygame.display.update()

        elif self.game.gamemode == "Levels":
            font4 = pygame.font.SysFont("comicsans", 100)
            text5 = font4.render("LEVELS", True,(230,230,230))
            text6 = font4.render("1", True,(230,230,230))
            text7 = font4.render("2", True,(230,230,230))
            text8 = font4.render("3", True,(230,230,230))
            text9 = font4.render("4", True,(230,230,230))
            text10 = font4.render("5", True,(230,230,230))

            l1 = pygame.Rect(oknoX//5*1 - 110, oknoY//3 + 80,100,150)
            l2 = pygame.Rect(oknoX//5*2 - 110, oknoY//3 + 80,100,150)
            l3 = pygame.Rect(oknoX//5*3 - 110, oknoY//3 + 80,100,150)
            l4 = pygame.Rect(oknoX//5*4 - 110, oknoY//3 + 80,100,150)
            l5 = pygame.Rect(oknoX//5*5 - 110, oknoY//3 + 80,100,150)

            maps = []
            maps.append(l1)
            maps.append(l2)
            maps.append(l3)
            maps.append(l4)
            maps.append(l5)

            win.fill((0,0,0))
            for i in maps:
                pygame.draw.rect(win,(70,70,70),pygame.Rect(i))

            win.blit(text5, (oknoX//2 - 125, oknoY//3 - 85))
            win.blit(text6, (oknoX//5 * 1 - 78, oknoY//3 + 115))
            win.blit(text7, (oknoX//5 * 2 - 78, oknoY//3 + 115))
            win.blit(text8, (oknoX//5 * 3 - 78, oknoY//3 + 115))
            win.blit(text9, (oknoX//5 * 4 - 78, oknoY//3 + 115))
            win.blit(text10,(oknoX//5 * 5 - 78, oknoY//3 + 115))
            win.blit(marioTile,(oknoX//2 - 25, oknoY//3))
            
            pygame.display.update()

#metoda, která obstarává všechny menu a obsahuje metodu pro překlikávání mezi rects
class Select():
    def __init__(self,game):
        self.game = game
        self.level = None

    def select(self):
        back_to_main_rect = pygame.Rect(oknoX//2 - 25, oknoY//3,50,50)
        back_to_main_rect2 = pygame.Rect(450,200,50,50)
        if self.game.gamemode == "Main":
            if mainRect1.collidepoint(pygame.mouse.get_pos()):
                self.game.obdelniky = []
                self.game.gamemode = "Levels"

            elif mainRect2.collidepoint(pygame.mouse.get_pos()):
                self.game.obdelniky = []
                self.game.readMap_createObj(bot_texture)
                self.game.gamemode = "Bot"

        elif self.game.gamemode == "Game":
            if back_to_main_rect2.collidepoint(pygame.mouse.get_pos()):
                self.game.gamemode = "Levels"
                self.game.mapa = []
            for i in self.game.obdelniky:
                if i.collidepoint(pygame.mouse.get_pos()):
                    self.game.radioactive = i
            
        elif self.game.gamemode == "End":
            self.game.gamemode = "Main"
        
        elif self.game.gamemode == "Levels":
            self.level_select()
            if back_to_main_rect.collidepoint(pygame.mouse.get_pos()):
                self.game.gamemode = "Main"
                self.game.mapa = []
        
        elif self.game.gamemode == "Bot":
            if back_to_main_rect2.collidepoint(pygame.mouse.get_pos()):
                self.game.gamemode = "Main"
                self.game.mapa = []
    
    def level_select(self):
        l1 = pygame.Rect(oknoX//5*1 - 110, oknoY//3 + 80,100,150)
        l2 = pygame.Rect(oknoX//5*2 - 110, oknoY//3 + 80,100,150)
        l3 = pygame.Rect(oknoX//5*3 - 110, oknoY//3 + 80,100,150)
        l4 = pygame.Rect(oknoX//5*4 - 110, oknoY//3 + 80,100,150)
        l5 = pygame.Rect(oknoX//5*5 - 110, oknoY//3 + 80,100,150)
        map01 = texture1
        map02 = texture2
        map03 = texture3
        map04 = texture4
        map05 = texture5
        if l1.collidepoint(pygame.mouse.get_pos()):
            self.game.obdelniky = []
            self.game.readMap_createObj(map01)
            self.game.gamemode = "Game"

        elif l2.collidepoint(pygame.mouse.get_pos()):
            self.game.obdelniky = []
            self.game.readMap_createObj(map02)
            self.game.gamemode = "Game"

        elif l3.collidepoint(pygame.mouse.get_pos()):
            self.game.obdelniky = []
            self.game.readMap_createObj(map03)
            self.game.gamemode = "Game"

        elif l4.collidepoint(pygame.mouse.get_pos()):
            self.game.obdelniky = []            
            self.game.readMap_createObj(map04)
            self.game.gamemode = "Game"

        elif l5.collidepoint(pygame.mouse.get_pos()):
            self.game.obdelniky = []                    
            self.game.readMap_createObj(map05)
            self.game.gamemode = "Game"
