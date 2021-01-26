import pygame
import random
import os
import json
import xml.etree.ElementTree as ET
import time

'''Notes:
'''

##functions for finding strings from XML: one using index location,
##another one using XPATH + word or REGEX + ISO lang code
source = 'game_strings.xml'


def string_extract(xml):
    tree = ET.parse(xml)
    root = tree.getroot()
    a = []
    b = []
    c = []
    phrases = [a, b, c]
    for elem in root:
        for sub in elem:
            if sub.attrib['lang'] == "en-US":
                eng = sub.text
                a.append(eng)
                ##sub.attrib is a dictionary!

            elif sub.attrib['lang'] == "es-419":
                span = sub.text
                b.append(span)

            elif sub.attrib['lang'] == "pt-BR":
                port = sub.text
                c.append(port)

    return phrases

##Put the strings into lists so that the game will function properly
game_strings = string_extract(source)
print(game_strings)

##Create the abiity to chose user language using these snippets:
lang_select_txt = "Select your language * Por favor elige el idioma * Selecione seu idioma"

##Button class --
class Button:

    def __init__(self, color, x, y, width, height, text='', opt=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.opt = opt

    def draw(self,win,outline=None):
        #Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)

        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', 60)
            text = font.render(self.text, 1, black)
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False

    def isClicked(self, action=None):
        global option
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if self.x + self.width > mouse[0] > self.x and self.y + self.height > mouse[1] > self.y:
            if click[0] == 1:
                option = self.opt
                action(option)

### Settings:
display_width = 800
display_height = 700

black = (0,0,0)
white = (255,255,255)
green = (0,255,0)
red = (255,0,0)
blue = (0,0,255)
grey = (128,128,128)

## Game loop! ##
pygame.init()

game_display = pygame.display.set_mode((display_width,display_height))
game_display.fill(white)

pygame.display.set_caption("SMOKE OR FIRE")
clock = pygame.time.Clock()
#pygame.display.update()

###Load images:
smoke_img = pygame.image.load("smoke.png")
fire_img = pygame.image.load("fire.png")

##Game functions:
def show_result(img, x,y):
    if img == "smoke":
        image = smoke_img
    elif img == "fire":
        image = fire_img
    game_display.blit(image, (x,y))
    pygame.display.update()
    time.sleep(1)


def text_objects(text, font):
    text_surface = font.render(text, True, black)
    return text_surface, text_surface.get_rect()


def result():
    message_display(game_strings[lang_var][a])


def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',60)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    game_display.blit(TextSurf, TextRect)
    pygame.display.update()
    time.sleep(2)


def play(option):
    chosen = option
    final = random.choice(["smoke", "fire"])
    global a

    if final == chosen:
        a = 3
        show_result(final, x, y)
        result()

    elif final != chosen:
        a = 4
        show_result(final, x, y)
        result()


##Other settings needed
x = (display_width * 0.45)
y = (display_width * 0.25)

def game_intro():

    intro = True

    while intro:
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

        if event.type == pygame.QUIT:
            intro = False
            pygame.quit()
            quit()

        game_display.fill(white)
        #Don't delete this:
        largeText = pygame.font.Font('freesansbold.ttf',20)
        TextSurf, TextRect = text_objects(lang_select_txt, largeText)
        TextRect.center = ((display_width/2),(display_height/2))
        game_display.blit(TextSurf, TextRect)


        en_button = Button(green, 180,500,125,100, "EN", "eng")
        es_button = Button(green, 360,500,125,100, "ES", "span")
        br_button = Button(green, 540,500,125,100, "BR", "port")
        en_button.draw(game_display, black)
        es_button.draw(game_display, black)
        br_button.draw(game_display, black)

        en_button.isClicked(gameloop)
        es_button.isClicked(gameloop)
        br_button.isClicked(gameloop)

        pygame.display.update()
        clock.tick(15)


def gameloop(option):
    #
    def lang_select(option):
        global lang_var
        lang_var = 0
        if option == "eng":
            lang_var = 0
            #print("Language code" + str(lang_var))
        elif option == "span":
            lang_var = 1
            #print("Language code" + str(lang_var))
        elif option == "port":
            lang_var = 2
            ###use this lang_var as an example.  Name it 'lang' and see why you are getting EN strings##
            #print("Language code" + str(lang_var))
        return lang_var

    lang_var = lang_select(option)
    #print(lang_var)

    run = True
    while run:
        #pygame.time.delay(5)

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

            #if event.type == pygame.MOUSEBUTTONDOWN:
                #print(event)

        game_display.fill(white)

        smokebutton = Button(grey,180,500,200,150, game_strings[lang_var][1], "smoke")
        firebutton = Button(red, 450,500,200,150, game_strings[lang_var][2], "fire")
        smokebutton.draw(game_display, black)
        firebutton.draw(game_display, black)

        smokebutton.isClicked(play)
        firebutton.isClicked(play)

        pygame.display.update()
        clock.tick(60)


###delete later
#print(game_strings[1][3])
#print(type(game_strings[1][3]))

game_intro()
gameloop()
pygame.quit()
quit()


### For vidd:
#1: add in "exit" button with localized strings asking for an exit confirmation
#   or a simple 'goodbye / thanks' before exiting the progrma
#2: add in a scoring feature: Correct anSwers ___
#
#
