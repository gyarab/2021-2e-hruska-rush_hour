import pygame
from textures import bot_texture, texture1, texture2, texture3, texture4, texture5

pygame.init()
pygame.display.set_caption("rush hours")

oknoX,oknoY = 600,500
win = pygame.display.set_mode((oknoX,oknoY))
tile = pygame.image.load("tile.jpg")
marioTile = pygame.image.load("marioTile.jpg")
hintTile = pygame.image.load("otaznik.png")

#obdelníky potřebné pro metodu collidepoint
mainRect1 = pygame.draw.rect(win, (100,0,0), pygame.Rect(oknoX//2 - 125,oknoY//3*1 - 85,250,150),2) 
mainRect2 = pygame.draw.rect(win, (100,0,0), pygame.Rect(oknoX//2 - 125,oknoY//3*2 - 70,250,150),2)
hint_rect = pygame.draw.rect(win, (0,0,0), pygame.Rect(500,25,50,50),2)
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

        elif self.height < self.width:
            self.stoji = False

#jde o třídu s veškerými metodami potřebnými na spuštění a chod hry
class Game():
    def __init__(self):
        self.gamemode = "Main"
        self.radioactive = None
        self.mapa, self.obdelniky, self.tracker = [], [], []
        self.tracker.append(["#","#","#","#","#","#","#","#","#","#"])
        for i in range(7):
            self.tracker.append(["#"," "," "," "," "," "," "," "," ","#"])
        self.tracker.append(["#","#","#","#","#","#","#","#","#","#"])
        self.frajer = None
        self.index = 0
        self.container = []
        self.levels = [[0],[0],[0],[0],[0]]
        self.playingMap = 0

    #pomocí této metody se vytvoří objekty typu obdelnik a následně se nahrají do pole obdelniky
    #metoda funguje na bázi průchodu vstupního pole po řádcích (více v dokumentaci)
    def readMap_createObj(self, mapInput):
        self.tracker = []
        self.tracker.append(["#","#","#","#","#","#","#","#","#","#"])
        for i in range(7):
            self.tracker.append(["#"," "," "," "," "," "," "," "," ","#"])
        self.tracker.append(["#","#","#","#","#","#","#","#","#","#"])

        self.container = []
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

        #pomocí tohoto kusu kódu se jeden z obdélníku identifikuje jako hlavní
        for i in self.obdelniky:
            if i.x == 50 and i.y == 200:
                self.frajer = i
                self.radioactive = self.frajer

    #metoda pro pohyb obdélníků po deskce
    #metoda funguje pomocí kontrolování zmáčknutých kláves a poté v daném směru přepisuje koordinace obdélníku,
    # které zpracuje metoda draw
    def move_objects(self, eventy):
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
                                self.levels[int(self.playingMap) - 1] = 1

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
            self.podminkaBot(self.tracker)

    #reset pole tracker je důležitý v opakovaném používání metody createObj..., jelikož po neresetování pole vznikají chyby a chybné hlášky
    def reset_tracker(self):
        self.tracker = []
        self.tracker.append(["#","#","#","#","#","#","#","#","#","#"])
        for i in range(7):
            self.tracker.append(["#"," "," "," "," "," "," "," "," ","#"])
        self.tracker.append(["#","#","#","#","#","#","#","#","#","#"])

    #jde o metodu, která vrací aktuální kombinaci obdélníků na hrací ploše (str)
    def return_case(self, map):
        s = ""
        for y in range(1,7):
            for x in range(1,8):
                if map[y][x] == " ":
                    s = s + "0"
                else:
                    s = s + str(map[y][x])
        return s

    #metody move_xxx jsou potřebné pro fungování bota a zajišťují posouvání obdélníku při volném prostoru před ním
    def move_right(self, rect):
        width_rect = rect.width//50
        if not rect.stoji:
            if self.tracker[rect.y//50][rect.x//50 + width_rect] == " ":
                self.tracker[rect.y//50][rect.x//50 + width_rect] = self.tracker[rect.y//50][rect.x//50]
                self.tracker[rect.y//50][rect.x//50] = " "
                rect.x += 50

            elif rect.collidepoint([9*50,5*50]):
                self.gamemode = "End"

    def move_left(self, rect):
        width_rect = rect.width//50
        if not rect.stoji:
            if self.tracker[rect.y//50][rect.x//50 - 1] == " ":
                self.tracker[rect.y//50][rect.x//50 - 1] = self.tracker[rect.y//50][rect.x//50]
                self.tracker[rect.y//50][rect.x//50 + width_rect-1] = " "
                rect.x -= 50

    def move_up(self, rect):
        height_rect = rect.height//50
        if rect.stoji:
            if self.tracker[rect.y//50 - 1][rect.x//50] == " ":
                self.tracker[rect.y//50 - 1][rect.x//50] = self.tracker[rect.y//50][rect.x//50]
                self.tracker[rect.y//50 + (height_rect-1)][rect.x//50] = " "
                rect.y -= 50
            
    def move_down(self, rect):
        height_rect = rect.height//50
        if rect.stoji:
            if self.tracker[rect.y//50 + height_rect][rect.x//50] == " ":
                self.tracker[rect.y//50 + height_rect][rect.x//50] = self.tracker[rect.y//50][rect.x//50]
                self.tracker[rect.y//50][rect.x//50] = " "
                rect.y += 50

    #metoda zajišťuje chod bota pomocí rekurze a závoreň dokáže vykreslovat obdélníky i při zanořování rekurze
    def podminkaBot(self, lol):
        self.draw()
        #pokud vrátí True, tak se hlavní obdélník dostal do cíle
        if self.tracker[4][8] == "H":
            self.gamemode = "End"
            self.timer = 1 
        else:
            self.timer = 200

        #tento blok kódu zjišťuje jestli se kombinace vrácená předchozí metodou neshoduje s jinou kombinací již zapsanou v poli
        s = self.return_case(lol)
        if s in self.container:
            return False
        else:
            self.container.append(s)

        #zeptá se rect jestli může jet doprava, pokud ano, tak jede
        #pokud ne, tak se kód posouvá na další možnosti pohybu
        #po pohnutí se zavolá rekurze a nahraje se kombinace trackeru
        for rect in self.obdelniky:
            if not rect.stoji: #horizontal
                
                self.move_right(rect)
                if self.gamemode != "End":    
                    if self.podminkaBot(self.tracker):
                        return True
                
                self.move_left(rect)
                if self.gamemode != "End":
                    if self.podminkaBot(self.tracker):
                        return True

            else: #vertical
                self.move_down(rect)                                                      
                if self.gamemode != "End":
                    if self.podminkaBot(self.tracker):
                        return True

                self.move_up(rect) 
                if self.gamemode != "End":                                                       
                    if self.podminkaBot(self.tracker):
                        return True
        
        pygame.time.delay(50)

 
    #metoda zajišťující veškeré vykreslování
    def draw(self):

        if self.gamemode == "Game":
            win.fill((35,30,30))
            win.blit(marioTile,(450,200))
            color,selectColor,frajerColor,frajerSelectColor = (150,0,0),(0,150,0),(0,0,220),(255,0,255)
            
            for y in range(len(self.mapa)):
                for x in range(len(self.mapa[0])):
                    if self.mapa[y][x] == "#":
                        win.blit(tile,(x * 50,y * 50))
                    
            #barvy obdélníků se mění při zvolení nebo pokud je obdélník hlavní
            for obdelnik in self.obdelniky:
                if obdelnik == self.radioactive:
                    if self.frajer == self.radioactive:
                        pygame.draw.rect(win, frajerSelectColor, (obdelnik.x+3 , obdelnik.y+3, obdelnik.width-6, obdelnik.height-6))
                    else:
                        pygame.draw.rect(win, selectColor, (obdelnik.x+3 , obdelnik.y+3, obdelnik.width-6, obdelnik.height-6))
                elif obdelnik == self.frajer:
                    pygame.draw.rect(win, frajerColor, (obdelnik.x+3 , obdelnik.y+3, obdelnik.width-6, obdelnik.height-6))
                else: 
                    pygame.draw.rect(win, color, (obdelnik.x+3 , obdelnik.y+3, obdelnik.width-6, obdelnik.height-6))
            #šedý obdélník za hrací plochou
            pygame.draw.rect(win,(60,60,60),(500,0,250,450))
            pygame.display.update()

        #vykreslování všech textů/obdélníků v hlavním menu
        elif self.gamemode == "Main":
            win.fill((35,30,30))
            win.blit(hintTile,(500, 25))
            mainRect1 = pygame.draw.rect(win, (100,0,0), pygame.Rect(oknoX//2 - 125,oknoY//3*1 - 85,250,150),2) 
            mainRect2 = pygame.draw.rect(win, (100,0,0), pygame.Rect(oknoX//2 - 125,oknoY//3*2 - 70,250,150),2) 
            font = pygame.font.SysFont("Arial", 45)
            text1 = font.render("SinglePlayer", True,(230,230,230))
            text2 = font.render("Solver", True,(230,230,230))
            pygame.draw.rect(win, (70,70,70), pygame.Rect(mainRect1))
            pygame.draw.rect(win, (70,70,70), pygame.Rect(mainRect2))
            win.blit(text1,(oknoX//2 - 104,oknoY//3*2 - 200))
            win.blit(text2,(oknoX//2 - 55,oknoY//3*1 + 145))
            pygame.display.update()

        #vykreslování všech textů/obdélníků v koncové obrazovce
        elif self.gamemode == "End":
            win.fill((0,0,0))
            font2 = pygame.font.SysFont("Arial", 100)
            font3 = pygame.font.SysFont("javanesetext", 40)
            text3 = font2.render("GAME OVER", True,(230,230,230))
            text4 = font3.render("click to get to the main menu", True,(230,230,230))
            win.blit(text3,(oknoX//2 - 240, oknoY//3))
            win.blit(text4,(oknoX//2 - 250, oknoY//3*2))
            pygame.display.update()

        #vykreslování všech textů/obdélníků při volení levelů v módu pro jednoho hráče
        elif self.gamemode == "Levels":
            doneColor, defaultColor = (0,150,0), (70,70,70)
            font4 = pygame.font.SysFont("Arial", 100)
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
            if self.levels[0] == 1:
                pygame.draw.rect(win,doneColor,pygame.Rect(l1))
            else:
                pygame.draw.rect(win,defaultColor,pygame.Rect(l1))

            if self.levels[1] == 1:
                pygame.draw.rect(win,doneColor,pygame.Rect(l2))
            else:
                pygame.draw.rect(win,defaultColor,pygame.Rect(l2))

            if self.levels[2] == 1:
                pygame.draw.rect(win,doneColor,pygame.Rect(l3))
            else:
                pygame.draw.rect(win,defaultColor,pygame.Rect(l3))
            
            if self.levels[3] == 1:
                pygame.draw.rect(win,doneColor,pygame.Rect(l4))
            else:
                pygame.draw.rect(win,defaultColor,pygame.Rect(l4))
            
            if self.levels[4] == 1:
                pygame.draw.rect(win,doneColor,pygame.Rect(l5))
            else:
                pygame.draw.rect(win,defaultColor,pygame.Rect(l5))

            win.blit(text5, (oknoX//2 - 150, oknoY//3 - 130))
            win.blit(text6, (oknoX//5 * 1 - 85, oknoY//3 + 100))
            win.blit(text7, (oknoX//5 * 2 - 85, oknoY//3 + 100))
            win.blit(text8, (oknoX//5 * 3 - 85, oknoY//3 + 100))
            win.blit(text9, (oknoX//5 * 4 - 85, oknoY//3 + 100))
            win.blit(text10,(oknoX//5 * 5 - 85, oknoY//3 + 100))
            win.blit(marioTile,(oknoX//2 - 25, oknoY//3))
            
            pygame.display.update()

        #vykreslení bariér, obdélníků při spuštění bota
        elif self.gamemode == "Bot":
            win.fill((0,0,0))
            for y in range(len(self.tracker)):
                for x in range(len(self.tracker[0])):
                    if self.tracker[y][x] == "#":
                        win.blit(tile,(x * 50,y * 50))

            for obdelnik in self.obdelniky:
                if obdelnik == self.frajer:
                    pygame.draw.rect(win, (255, 0, 255), (obdelnik.x+3 , obdelnik.y+3, obdelnik.width-6, obdelnik.height-6))
                else: 
                    pygame.draw.rect(win, (150,0,0), (obdelnik.x+3 , obdelnik.y+3, obdelnik.width-6, obdelnik.height-6))
            pygame.draw.rect(win,(60,60,60),(500,0,250,450))
            win.blit(marioTile,(450,200))
            pygame.display.update()

        #vykreslení textu při zmáčknutí na otazník
        elif self.gamemode == "Hint":
            win.fill((35,30,30))
            win.blit(marioTile,(500, 25))
            font5 = pygame.font.SysFont("Arial", 40)
            text11 = font5.render("pro zvolení obdélníku použijte myš", True,(230,230,230))
            text12 = font5.render("pro pohyb obdélníkem použijte šipky", True,(230,230,230))
            text13 = font5.render("žlutý čtverec funguje jako tlačítko zpět", True,(230,230,230))
            text14 = font5.render("obdélník nelze pohybovat do boku", True,(230,230,230))
            win.blit(text11,(oknoX//2 - 240, oknoY//3-70))
            win.blit(text12,(oknoX//2 - 250, oknoY//3*2-130))
            win.blit(text13,(oknoX//2 - 270, oknoY//3*3-100))
            win.blit(text14,(oknoX//2 - 240, oknoY//3*3-230))
            pygame.display.update()

    #metoda, která obstarává všechny menu a obsahuje metodu pro překlikávání mezi rects
    def select(self):
        back_to_main_rect = pygame.Rect(oknoX//2 - 25, oknoY//3,50,50)
        back_to_main_rect2 = pygame.Rect(450,200,50,50)
        if self.gamemode == "Main":
            if mainRect1.collidepoint(pygame.mouse.get_pos()):
                self.obdelniky = []
                self.gamemode = "Levels"

            elif mainRect2.collidepoint(pygame.mouse.get_pos()):
                self.obdelniky, self.mapa = [], []
                self.readMap_createObj(bot_texture)
                self.gamemode = "Bot"
            
            elif hint_rect.collidepoint(pygame.mouse.get_pos()):
                self.gamemode = "Hint"
        
        elif self.gamemode == "Hint":
            if hint_rect.collidepoint(pygame.mouse.get_pos()):
                self.gamemode = "Main"
                
        elif self.gamemode == "Game":
            if back_to_main_rect2.collidepoint(pygame.mouse.get_pos()):
                self.mapa = []
                self.gamemode = "Levels"  

            for i in self.obdelniky:
                if i.collidepoint(pygame.mouse.get_pos()):
                    self.radioactive = i
            
        elif self.gamemode == "End":
            self.gamemode = "Main"
        
        elif self.gamemode == "Levels":
            self.level_select()
            if back_to_main_rect.collidepoint(pygame.mouse.get_pos()):
                self.mapa = []
                self.gamemode = "Main"
        
        elif self.gamemode == "Bot":
            if back_to_main_rect2.collidepoint(pygame.mouse.get_pos()):
                self.mapa = []
                self.gamemode = "Main"

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
            self.obdelniky = []
            self.readMap_createObj(map01)
            self.reset_tracker()
            self.gamemode = "Game"
            self.playingMap = 1

        elif l2.collidepoint(pygame.mouse.get_pos()):
            self.obdelniky = []
            self.readMap_createObj(map02)
            self.reset_tracker()
            self.gamemode = "Game"
            self.playingMap = 2

        elif l3.collidepoint(pygame.mouse.get_pos()):
            self.obdelniky = []
            self.readMap_createObj(map03)
            self.reset_tracker()
            self.gamemode = "Game"
            self.playingMap = 3

        elif l4.collidepoint(pygame.mouse.get_pos()):
            self.obdelniky = []            
            self.readMap_createObj(map04)
            self.reset_tracker()
            self.gamemode = "Game"
            self.playingMap = 4

        elif l5.collidepoint(pygame.mouse.get_pos()):
            self.obdelniky = []                    
            self.readMap_createObj(map05)
            self.reset_tracker()
            self.gamemode = "Game"
            self.playingMap = 5