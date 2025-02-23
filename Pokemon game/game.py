#-----------------------------------------------------------------------------------------------
# Program: OOP assignment - Trading Card Game
# Author: Philip Terrigno and Carol Xu
# Date: May 2024
# Description: This is a pokemon imitation game.
# Players engage in battles between Fire, Water, and Grass type monsters. Players 
# start by selecting their monster typ.The game features turn-based battles, 
# allowing players and the computer-controlled opponent to take alternating turns. During 
# battles, players can choose from various actions including strong attacks, weak attacks, 
# and using healing potions. The game ends when either the player's or the opponent's monster's 
# health points reach zero, with a game over screen displaying the outcome of the battle.
# Input: User inputs the name of their pokemon and clicks buttons to switch between screens
# and to play the game and perfrom moves such as choosing their pokemon, attacking and healing.
#-----------------------------------------------------------------------------------------------

#Imports pygame, time, random and math.
import pygame, sys
import time
from pygame.locals import *
import random
import math

#Creates list of the button coordinates and names.
back_button = [(50,50)]

player_options = [[(206,490,160,80), 'START'],
               [(421,490,160,80), 'QUIT'],
               [(630,490,160,80),'INSTRUCTIONS']]

#Initializing colours.
GREY = (100,100,100)
BLUE = (30,144,255)
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)
BEIGE = (207,185,151)

#Initilize the message to be displayed when the programs asks the user to enter pokemon name.
#Initialize the player name.
nametxt= 'Please enter your Pokemon name'
playerName = ''

#Creates the class that handles the main functionalities of the game.
class game: 

    #Initializes the game class.
    #Initializes the game window.
    #Initializes the pygame's clock to track time.
    def __init__(self):
        pygame.init() 
        self.screen_width = 1000 
        self.screen_height = 600
        self.win = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()

        #Initialize and sizes the images to be used throughout the game.
        self.battle = pygame.transform.scale(pygame.image.load('pokeback.png'), (1000,600))
        self.main_screen1 = pygame.transform.scale(pygame.image.load('POKE.png'), (1000,600))
        self.instructions = pygame.transform.scale(pygame.image.load('instructions.png'), (1000,600))
        self.choose = pygame.transform.scale(pygame.image.load('CHOOSE.png'), (1000,200))
        self.starter = pygame.transform.scale(pygame.image.load('starters.png'), (1000,600))
        self.bulbasaur_png = pygame.transform.scale(pygame.image.load('bulbasaur.png'),(120,120))
        self.charmander_png = pygame.transform.scale(pygame.image.load('charmander.png'),(120,120))
        self.squirtle_png =pygame.transform.scale(pygame.image.load('squirtle.png'),(150,150))
        self.bulbasaurback_png = pygame.transform.scale(pygame.image.load('bulbasaurback.png'),(175,175))
        self.charmanderback_png = pygame.transform.scale(pygame.image.load('charmanderback.png'),(300,300))
        self.squirtleback_png =pygame.transform.scale(pygame.image.load('squirtleback.png'),(300,300))
        self.ending = pygame.transform.scale(pygame.image.load('pokemon_ending.png'),(1000,600))
        self.player= pygame.image.load('T1.png')

        #Initialize fonts.
        self.btn_font = pygame.font.SysFont("monospace", 20)
        self.end_font = pygame.font.SysFont("monospace", 100)

    #Function that redraws the game window based on the current screen.
    def redraw_game_window(self):
        #Creates the corresponding backgrounds for each of the screens including any buttons.
        if game_status == 'intro page':                  
            self.win.blit(self.main_screen1,(0,0))        
            self.drawCatagoryButtons(player_options)
        elif game_status == 'select pokemon':
            self.win.blit(self.starter,(0,0))
            self.drawButton(back_button)
            self.win.blit(self.choose,(50,-40))
        elif game_status == 'instructions':
            self.win.blit(self.instructions,(0,0))
            self.drawButton(back_button)
        elif game_status == 'name pokemon':
            self.win.fill(BEIGE)
            self.render_multi_line(nametxt, 50, 50, 20)
        elif game_status == 'start battle' or game_status =='player turn' or game_status =='rival turn' or game_status=='player move'  :
            self.win.blit(self.battle,(0,0))
            self.drawButton(back_button)
            self.win.blit(game.player,(1,350))
        elif game_status == 'gameover':
            self.win.blit(self.ending,(0,0))           

    #Draws all the buttons on the intro page screen using the button data (found at top) and changes the colour when moused over or clicked.
    def drawCatagoryButtons(self, player_options):
        opt_click = pygame.mouse.get_pos()
        for i in player_options:
            if pygame.Rect(i[0]).collidepoint(opt_click):
                Btn_colour = GREY
            else:
                Btn_colour = BLUE
            pygame.draw.rect(self.win,Btn_colour,i[0],0)
            pygame.draw.rect(self.win,BLACK,i[0],3)
            txtSurface = self.btn_font.render(i[1],True,BLACK)
            x = i[0][0] + (i[0][2] - txtSurface.get_width())//2
            y = i[0][1] + (i[0][3] - txtSurface.get_height())//2
            self.win.blit(txtSurface,(x,y))

    #Draws the circular "back" button on the corresonding pages using the button data (found at top) and changes the colour when moused over or clicked.
    def drawButton(self, coordinate):
        mousePos = pygame.mouse.get_pos()
        for i, xy in enumerate(coordinate):
            a = mousePos[0] - xy[0]
            b = mousePos[1] - xy[1]
            c = (a**2 + b**2) ** 0.5
            if c <= 15:
                btn_colour = GREY
            else:
                btn_colour = BLUE
            pygame.draw.circle(self.win, btn_colour, xy, 30, 0)
            pygame.draw.circle(self.win, BLACK, xy, 30, 3)
            
            ltrToRender = 'BACK'
            ltrSurface = self.btn_font.render(ltrToRender, True, BLACK)
            self.win.blit(ltrSurface, (xy[0] - ltrSurface.get_width() // 2, xy[1] - ltrSurface.get_height() // 2))

    #Draws the buttons for the attacks and changes the colour when moused over or clicked.
    #The button labels change depending on which pokemon has been chosen by the user.
    def create_button(self, width, height, left, top, text_cx, text_cy, label):
        mouse_cursor = pygame.mouse.get_pos()
        button = Rect(left, top, width, height)
        if button.collidepoint(mouse_cursor):
            pygame.draw.rect(self.win, GREY, button)
        else:
            pygame.draw.rect(self.win,WHITE , button)
            
        font = pygame.font.Font(pygame.font.get_default_font(), 16)
        text = font.render(f'{label}', True, BLACK)
        text_rect = text.get_rect(center=(text_cx, text_cy))
        self.win.blit(text, text_rect)
        
        return button
    
    #Displays the name of the pokemon and the attack it used ot if it used a potion.
    #Display the pokemons names and health.
    def display_message(self,message):
        game.redraw_game_window()
        pygame.draw.rect(self.win, BEIGE, (30, 120, 480, 140))
        pygame.draw.rect(self.win, BLACK, (30, 120, 480, 140), 3)

        font = pygame.font.Font(pygame.font.get_default_font(), 30)
        text = font.render(message, True, BLACK)
        text_rect = text.get_rect(center=(250, 200))
        
        self.win.blit(text, text_rect)
        rival_pokemon.draw_hp()
        rival_pokemon.draw(rival_pokemon.front)
        player_pokemon.draw_hp()
        player_pokemon.draw(player_pokemon.back)
    
        pygame.display.update()
        time.sleep(1)

    #Checks if the buttons have been clicked.
    @staticmethod
    def clickBtn (mp, button) :
        for i,xy in enumerate (button):
            a = mp[0] - xy[0]
            b = mp[1] - xy[1]
            c = (a**2 + b**2) **.5
            if c <= 15:
                return i
        return -1

    #Checks if the buttons have been clicked
    @staticmethod
    def playerBtnClick(mp,buttons):
        for i,b in enumerate(buttons):
            if pygame.Rect(b[0]).collidepoint(mp):
                return i
        return -1

    #Puts text on screen.
    def render_multi_line(self, text, x, y, fsize):
        lines = text.splitlines()
        for i, l in enumerate(lines):
            self.win.blit(self.btn_font.render(l, True, BLACK), (x, y + fsize*i))

#Creates the class that creates each move including their type, name and power.
class Move:
    def __init__(self,name,types,power):
        self.name = name
        self.power = power
        self.types = types

#Creates the class that handles the pokemon's characteristics and placement on screen.
class Pokemon:
    def __init__(self, name, current_hp, max_hp,speed,attack,defense,front_png,back_png,x,y,level):
        self.name = name
        self.current_hp = current_hp
        self.max_hp = max_hp
        self.num_potions = 1
        self.speed = speed
        self.attack = attack 
        self.defense = defense
        self.front = front_png.convert_alpha()
        self.back =  back_png.convert_alpha()
        self.current_x = x
        self.current_y = y
        self.initial_x = x
        self.initial_y = y
        self.level = level
        self.win = game.win

    #Uses the determined health of the pokemons to draw their corresponding health bars.
    def draw_hp(self):
        bar_scale = 200 // self.max_hp
        for i in range(self.max_hp):
            bar = (self.hp_x + bar_scale * i, self.hp_y, bar_scale, 20)
            pygame.draw.rect(self.win, RED, bar)
            
        for i in range(self.current_hp):
            bar = (self.hp_x + bar_scale * i, self.hp_y, bar_scale, 20)
            pygame.draw.rect(self.win, GREEN, bar)

        font = pygame.font.Font(pygame.font.get_default_font(), 16)
        text = font.render(f'{self.name}      HP: {self.current_hp} / {self.max_hp}', True, WHITE)
        text_rect = text.get_rect()
        text_rect.x = self.hp_x
        text_rect.y = self.hp_y + 30
        self.win.blit(text, text_rect)

    #Updates the pokemon's health every time they take damage.
    #The HP will not go below zero.
    def take_damage(self, damage):
        self.current_hp -= damage
        if self.current_hp < 0:
            self.current_hp = 0

    #If there are potions left, when used they add 30 health but will not go over the max health allowed.
    #When used, they havbe 1 less potion left to use.
    def use_potion(self):
        if self.num_potions > 0:
            self.current_hp += 30
            if self.current_hp > self.max_hp:
                self.current_hp = self.max_hp
            self.num_potions -= 1

    #Displays the name of the pokemon and the attack they performed.
    #Calculates the damage done and removes it from the health of the attacked pokemon.
    def perform_attack(self, other, move):
        self.display_message(f'{self.name} used {move.name}')
        damage = (2 * self.level + 10) / 250 * self.attack / other.defense * move.power
        damage = math.floor(damage)
        other.take_damage(damage)

    #Draws pokemons on screen using their appropriate coordinates.
    def draw(self, face, alpha =255):
        sprite = face.copy()
        transparency = (255, 255, 255, alpha)
        sprite.fill(transparency, None, pygame.BLEND_RGBA_MULT)
        self.win.blit(sprite, (self.current_x, self.current_y))

    #Returns the pokemons position on the screen.
    def get_rect(self):
        return Rect(self.initial_x, self.initial_y, self.front.get_width(), self.front.get_height())

#Creates the fire pokemon class that inherits all the pokemon characteristics and initializes its specific attack names.
class Fire_mon(Pokemon,game):
    def __init__(self, name, current_hp, max_hp,speed,attack,defense,front_png,back_png,x,y,level):
        Pokemon.__init__(self, name, current_hp, max_hp,speed,attack,defense,front_png,back_png,x,y,level)
        self.moves = [Ember, Scratch, Burn,Tackle]

#Creates the water pokemon class that inherits all the pokemon characteristics and initializes its specific attack names.
class Water_mon(Pokemon,game):
    def __init__(self, name, current_hp, max_hp,speed,attack,defense,front_png,back_png,x,y,level,):
        Pokemon.__init__(self, name, current_hp, max_hp, speed, attack, defense, front_png,back_png,x,y,level)
        self.moves = [Watergun, Bubble, Scratch,Tackle]

#Creates the grass pokemon class that inherits all the pokemon characteristics and initializes its specific attack names.    
class Grass_mon(Pokemon,game):
    def __init__(self,name, current_hp, max_hp,speed,attack,defense,front_png,back_png,x,y,level):
        Pokemon.__init__(self, name, current_hp, max_hp,speed,attack,defense,front_png,back_png,x,y,level)
        self.moves = [Scratch, Razorleaf, Grassknot,Tackle]
        
#Initializes all the possible attacks and their corresponding damages.
Ember = Move('Ember','Fire',30)
Burn= Move('Burn','Fire',50)
Scratch = Move('Scratch','Normal',25)
Tackle = Move('Tackle','Normal',40)
Watergun = Move('Water Gun','Water',40)
Bubble = Move('Bubble','Water',30)
Razorleaf = Move('Razorleaf','Grass',60)
Grassknot = Move('Grassknot','Grass',40)

#Instantiates an object the game class.
game = game()

#Initializes the pokemon options, their placements and randomizes their characteristics.
bulbasaur = Grass_mon('Bulbasaur', 65,65,random.randint(30,40),random.randint(70,100),random.randint(70,100),game.bulbasaur_png,game.bulbasaurback_png, 200, 300,30)
charmander = Fire_mon('Charmander',65,65,random.randint(30,40),random.randint(70,100),random.randint(70,100), game.charmander_png, game.charmanderback_png, 472, 350,30)
squirtle = Water_mon('Squirtle', 65,65,random.randint(30,40),random.randint(70,100),random.randint(70,100),game.squirtle_png, game.squirtleback_png,675, 270,30)
pokemons = [bulbasaur, charmander, squirtle]
player_pokemon = None
rival_pokemon = None

#Initializes the text displayed on the gameover screen.
text = ''
Win_message = 'YOU WIN'
Lose_message = 'YOU LOSE '

#Sets the status to the intro screen.
#Sets a condition for the while loop.
game_status = 'intro page'
inPlay = True
move_buttons = []

#The main game loop that updates the screen accordingly.
while inPlay:
    #Checks for pygame events.
    for event in pygame.event.get():
        #If they click on the window x, pygame quits.
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        #Checks if keys are clicked.
        if event.type == pygame.KEYDOWN:
            #After hitting enter when done entering pokemon name brings the user to the battle screen.
            #Name updates on screen as it's being typed, also accounts for backspace.
            #Names the user's pokemon the name they entered.
            if game_status == 'name pokemon':
                if event.key == pygame.K_RETURN:
                    game_status = 'start battle'
                elif event.key == pygame.K_BACKSPACE:
                    playerName = playerName[:-1]
                else:
                    playerName += event.unicode
                    player_pokemon.name = playerName

        #Checks for mouse clicks
        if event.type == pygame.MOUSEBUTTONDOWN:   
            clickPos = pygame.mouse.get_pos()
            #Changes the screen appropriately based on the button clicked.
            if game_status == 'intro page':                
                option = game.playerBtnClick(clickPos, player_options) 
                if option != -1:                 
                    if option == 1:         
                        pygame.quit()       
                        sys.exit()
                    elif option == 2:
                        game_status = 'instructions'
                    else:
                        game_status = 'select pokemon'
            #If the back button has been clicked on the pokemon select page, the user returns to the intro page.      
            if game_status == 'select pokemon':
               back_click = game.clickBtn(clickPos, back_button)
               if back_click == 0:       
                    game_status = 'intro page'
               for i in range(len(pokemons)):
                    if pokemons[i].get_rect().collidepoint(clickPos):
                        #Assigns the user's and rival's pokemon
                        player_pokemon = pokemons[i]
                        player_pokemon_pos = player_pokemon.get_rect()
                        available_pokemons = [p for p in pokemons if p != player_pokemon]
                        rival_pokemon = random.choice(available_pokemons)
                        rival_pokemon_pos = rival_pokemon.get_rect()
                        
                        #Lowering the rival pokemon's level to make the battle easier.
                        rival_pokemon.level = int(rival_pokemon.level * 0.9)
                        
                        #Sets the coordinates of the health bars and their positions.
                        player_pokemon.hp_x = 100
                        player_pokemon.hp_y = 300
                        rival_pokemon.hp_x = 570
                        rival_pokemon.hp_y = 200
                        player_pokemon.current_x = 250
                        player_pokemon.current_y = 375
                        rival_pokemon.current_x = 704
                        rival_pokemon.current_y = 264     

                        #Goes to the next screen
                        game_status = 'name pokemon'
                        
            #If the back button has been clicked on the instructions page, the user returns to the intro page.                       
            if game_status == 'instructions':
                back_click = game.clickBtn(clickPos, back_button)
                if back_click == 0:
                    game_status = 'intro page'

            #If the back button has been clicked on the start battle page, the user returns to the pokemon select page.
            #The pokemons return to their initial position and their healths are reset.
            if game_status == 'start battle':
                back_click = game.clickBtn(clickPos, back_button)          
                if back_click == 0:
                  player_pokemon.current_x = player_pokemon.initial_x
                  player_pokemon.current_y = player_pokemon.initial_y
                  rival_pokemon.current_x = rival_pokemon.initial_x
                  rival_pokemon.current_y = rival_pokemon.initial_y
                  player_pokemon.current_hp = 65
                  rival_pokemon.current_hp = 65
                  game_status = 'select pokemon'
                
            #If the back button has been clicked on the player turn page, the user returns to the pokemon select page.
            #The pokemons return to their initial position and their healths are reset.
            elif game_status == 'player turn':
                back_click = game.clickBtn(clickPos, back_button)
                if back_click == 0:       
                    player_pokemon.current_hp = 65
                    rival_pokemon.current_hp =65
                    player_pokemon.current_x = player_pokemon.initial_x
                    player_pokemon.current_y= player_pokemon.initial_y
                    rival_pokemon.current_x = rival_pokemon.initial_x
                    rival_pokemon.current_y = rival_pokemon.initial_y
                    game_status = 'select pokemon'
                
                #Checks if fight button was clicked.
                if fight_button.collidepoint(clickPos):
                    game_status = 'player move'
                    
                #Checks if potion button was clicked.
                if potion_button.collidepoint(clickPos):
                    #Potion is used and health is updated accordingly.
                    #User must attack if there are no potions left.
                    #Switches to the rival's turn.
                    if player_pokemon.num_potions == 0:
                        game.display_message('No more potions left')
                        game_status = 'player move'
                    else:
                        player_pokemon.use_potion()
                        game.display_message(f'{player_pokemon.name} used potion')
                        game_status = 'rival turn'

            #Checks which button has been clicked on the player move page.
            elif game_status == 'player move':
                #If the back button has been clicked, the user returns to the pokemon select page.
                #The pokemons return to their initial position and their healths are reset.
                if back_click == 0:      
                    player_pokemon.current_x = player_pokemon.initial_x
                    player_pokemon.current_y= player_pokemon.initial_y
                    rival_pokemon.current_x = rival_pokemon.initial_x
                    rival_pokemon.current_y = rival_pokemon.initial_y 
                    player_pokemon.current_hp = 65
                    rival_pokemon.current_hp =65
                    game_status = 'select pokemon'

                for i in range(len(move_buttons)):
                    button = move_buttons[i]
                    #If an attack button was clicked, that attack is performed accordingly.
                    if button.collidepoint(clickPos):
                        move = player_pokemon.moves[i]
                        player_pokemon.perform_attack(rival_pokemon, move)
                 
                        #Checks if the rival's pokemon fainted (has no health left).
                        if rival_pokemon.current_hp == 0:
                            game_status = 'fainted'
                        else:
                            game_status = 'rival turn'

    #On the select pokemon page, the pokemon choices are drawn.
    #Draws box around pokemon when the mouse hovers over it.
    if game_status == 'select pokemon':
        bulbasaur.draw(bulbasaur.front)
        charmander.draw(charmander.front)
        squirtle.draw(squirtle.front)
        for pokemon in pokemons:
            mouse_cursor = pygame.mouse.get_pos()
            if pokemon.get_rect().collidepoint(mouse_cursor):
                pygame.draw.rect(game.win, WHITE, pokemon.get_rect(), 2)

    #Takes user to the screen to name their chosen pokemon.
    if game_status == 'name pokemon':
        name_surface = game.btn_font.render(playerName, True, WHITE)
        game.win.blit(name_surface, (50, 80))

    #On the battle screen the pokemons and their health bars are drawn.
    if game_status == 'start battle':
        game.redraw_game_window() 
        player_pokemon.draw(player_pokemon.back)
        rival_pokemon.draw(rival_pokemon.front)
        rival_pokemon.draw_hp()
        player_pokemon.draw_hp()

        #Depending on their speed attribute, the faster pokemon starts first.
        if rival_pokemon.speed > player_pokemon.speed:
            game_status = 'rival turn'
        else:
            game_status = 'player turn'

    #If it's the user's turn, the pokemons and their health bars are drawn.
    if game_status == 'player turn':
        game.redraw_game_window()
        player_pokemon.draw(player_pokemon.back)
        rival_pokemon.draw(rival_pokemon.front) 
        rival_pokemon.draw_hp()
        player_pokemon.draw_hp()
        #Creating the fight and potion buttons (includes number of potions left).
        fight_button = game.create_button(240, 140, 510, 450, 630, 512, 'Fight')
        potion_button = game.create_button(240, 140, 750, 450, 870, 512, f'Use Potion ({player_pokemon.num_potions})')
        pygame.draw.rect(game.win, BLACK, (510, 450, 480, 140), 3)

    #If the user has chosen to attack, the attack option buttons are created and drawn.
    if game_status == 'player move':
        game.redraw_game_window()
        player_pokemon.draw(player_pokemon.back)
        rival_pokemon.draw(rival_pokemon.front)
        rival_pokemon.draw_hp()
        player_pokemon.draw_hp()
        move_buttons = []
        for i in range(len(player_pokemon.moves)):
            move = player_pokemon.moves[i]
            button_width = 240
            button_height = 70
            left = 500 + i % 2 * button_width
            top = 450 + i // 2 * button_height
            text_center_x = left + 120
            text_center_y = top + 35
            button = game.create_button(button_width, button_height, left, top, text_center_x, text_center_y, move.name.capitalize())
            move_buttons.append(button)
        pygame.draw.rect(game.win, BLACK, (500, 450, 480, 140), 3)

    #If it is the rivals turn, the display clears and a random attack is selected.
    if game_status == 'rival turn':
        game.redraw_game_window()
        player_pokemon.draw(player_pokemon.back)
        rival_pokemon.draw(rival_pokemon.front)
        
        game.display_message('')

        move = random.choice(rival_pokemon.moves)
        rival_pokemon.perform_attack(player_pokemon, move)
        
        #Checks if the user's pokemon ran out of health.
        if player_pokemon.current_hp == 0:
            game_status = 'fainted'
            text = Lose_message
        else:
            game_status = 'player turn'

    #If either pokemon ran out of health the appropriate message is displayed.
    #The game status is set to gameover.
    if game_status == 'fainted':
        if rival_pokemon.current_hp == 0:
            game.redraw_game_window()
            player_pokemon.draw(player_pokemon.back)
            game.display_message(f'{rival_pokemon.name} fainted!')
            text = Win_message
        else:
            game.redraw_game_window
            rival_pokemon.draw(rival_pokemon.front)
            game.display_message(f'{player_pokemon.name} fainted!')

        game_status = 'gameover'
        time.sleep(1)
        
    #The gameover screen is shown with the win or loss message.
    if game_status == 'gameover':
        txt_surface = game.end_font.render(text, True, WHITE)
        game.win.blit(txt_surface, (300,100))
  
    #Updating the window/screen.
    pygame.display.flip()
    game.redraw_game_window()
    #Fps so the game doesn't lag.
    game.clock.tick(60)
#Quits pygame.
pygame.quit()

