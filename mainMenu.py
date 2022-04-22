import pygame, sys
pygame.init()
pygame.display.set_caption("rush hours")

oknoX,oknoY = 600,500
win = pygame.display.set_mode((oknoX,oknoY))
tile = pygame.image.load("C:/Users/fifah/Desktop/1E-školní dokumenty/programko/python/programy/tile.jpg")
marioTile = pygame.image.load("C:/Users/fifah/Desktop/1E-školní dokumenty/programko/python/programy/mariotile.jpg")
#herní pole, které se vytvoří podle různých znaků vepsaných do str

texture = """##########
#TTTTTT  #
#KKKMMM O#
#   UU LO#
#HH jG LDF
#XLLjG LD#
#X   G AA#
#XPPP II #
##########"""

botTexture = """##########
#LLLLLLLL#
#        #
#    kp  #
#HH  kpOs F 
#    kpO #
#      O #
#        #
##########"""
#potřebné proměnné na vytvoření menu
font = pygame.font.SysFont('Arial', 45)
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
        self.mapa, self.obdelniky = [], []
        self.frajer = None
        self.index = 0
        self.zasobnik = []

    def push(self,rect):
        self.zasobnik.append(rect)
        self.index += 1

    def popOut(self):
        self.index -= 1
        return self.zasobnik.remove((self.index) + 1)

    def getIndex(self):
        if len(self.zasobnik) == 0:
            return len(self.zasobnik)
        else:
            return len(self.zasobnik) - 1
        #1x rect -> poslední je na indexu 0, 0x rect -> index posledního je stále 0, proto tento if 
    
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
                    
                    if self.mapa[y][x] == self.mapa[y][x+1]: # sirokej
                        i = 2
                        while True:
                            if self.mapa[y][x] == self.mapa[y][x+i]:
                                i += 1
                            else: #mazání kvůli následnému problému s průchodem
                                self.obdelniky.append(Obdelnik(x,y,i,1))
                                #print("first "+ str(x) + str(y) + str(i))
                                for sirka in range(i):
                                    self.mapa[y][x + sirka] = " "
                                break
                            
                    elif self.mapa[y][x] ==  self.mapa[y+1][x]: # vysokej
                        i = 2
                        while True:
                            if self.mapa[y][x] == self.mapa[y+i][x]:
                                i += 1
                                
                            else:  #mazání kvůli následnému problému s průchodem
                                self.obdelniky.append(Obdelnik(x,y,1,i))
                                #print("second "+ str(x) + str(y) + str(i))
                                for vyska in range(i):
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
    
    #metoda, ve které vše potřebné, aby se bot pohyboval
    def podminkaBot(self):
        pass
        
#třída, ve které jsou vščechny potřebné metody na vykreslování rects atd   
class Draw():
    def __init__(self,game):
        self.game = game

    def draw(self):

        if self.game.gamemode == "Game" or self.game.gamemode == "Bot":
            win.fill((35,30,30))
            win.blit(marioTile,(450,200))
            color,selectColor,frajerColor,frajerSelectColor = (150,0,0),(0,150,0),(0,0,220),(255, 0, 255)
            
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
            text1 = font.render("SinglePlayer", True,(230,230,230))
            text2 = font.render("Bottares", True,(230,230,230))
            pygame.draw.rect(win, (70,70,70), pygame.Rect(mainRect1))
            pygame.draw.rect(win, (70,70,70), pygame.Rect(mainRect2))
            win.blit(text1,(oknoX//2 - 100,oknoY//3*2 - 200))
            win.blit(text2,(oknoX//2 - 70,oknoY//3*1 + 145))
            pygame.display.update()

        elif self.game.gamemode == "End":
            win.fill((35,30,30))
            text3 = font.render("You win", True,(230,230,230))
            text4 = font.render("Main menu", True,(230,230,230))
            pygame.draw.rect(win, (70,70,70), pygame.Rect(mainRect1))
            pygame.draw.rect(win, (70,70,70), pygame.Rect(mainRect2))
            win.blit(text3,(oknoX//2 - 65,oknoY//3*2 - 200))
            win.blit(text4,(oknoX//2 - 95,oknoY//3*1 + 145))
            pygame.display.update()

#metoda, která obstarává všechny menu a obsahuje metodu pro překlikávání mezi rects
class Select():
    def __init__(self,game):
        self.game = game

    def select(self):
        
        if self.game.gamemode == "Main":
            if mainRect1.collidepoint(pygame.mouse.get_pos()) and self.game.gamemode == "Main":
                self.game.obdelniky = []
                self.game.readMap_createObj(texture)
                self.game.gamemode = "Game"

            elif mainRect2.collidepoint(pygame.mouse.get_pos()) and self.game.gamemode == "Main":
                self.game.obdelniky = []
                self.game.readMap_createObj(botTexture)
                self.game.gamemode = "Bot"
        
        elif self.game.gamemode == "Game":
            for i in self.game.obdelniky:
                if i.collidepoint(pygame.mouse.get_pos()):
                    self.game.radioactive = i
                    
        elif self.game.gamemode == "End":
            endRect = pygame.draw.rect(win, (100,0,0), pygame.Rect(oknoX//2 - 125,oknoY//3*2 - 70,250,150),2)
            if endRect.collidepoint(pygame.mouse.get_pos()) and self.game.gamemode == "End":
                self.game.gamemode = "Main"