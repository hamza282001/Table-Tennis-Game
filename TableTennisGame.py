import pygame, sys, random, time
from pygame.locals import *
import matplotlib.pyplot as plt 


#----------------------------------------------------------------------------------| GameBox |-----------------------------------------------------------------------------------------------
# ------------------------------------------------------ This class conatins all of the major game logic and game animation. ----------------------------------------------------------------

class GameBox:

    def __init__(self):

        pygame.init()
        self.mainClock = pygame.time.Clock()

        # Screen window Resolution. 
        self.screen_width = 835
        self.screen_height = 550

        # Court Table Dimensions.
        self.table_width = 600
        self.table_height = 350

        # Setting up Screen Window.
        self.screen = pygame.display.set_mode((self.screen_width,self.screen_height))
        pygame.display.set_caption('Pong')

        # Images.
        self.image = pygame.image.load('tt1.jpg')
        self.image1 = pygame.image.load('Group.png')

        # Colours.
        self.green = (0,128,0)
        self.light_grey = (200,200,200)
        self.orange = (255,50,0)

        # Fonts.
        self.font = pygame.font.SysFont(None,20)
        self.game_font = pygame.font.Font("freesansbold.ttf",32)

        # Every Game Object Dimensions. 
        self.table = pygame.Rect(self.screen_width/2 - self.table_width/2,self.screen_height/2 - self.table_height/2,600,350)
        self.tableBorder = pygame.Rect((self.screen_width/2 - self.table_width/2)-5,(self.screen_height/2 - self.table_height/2)-5,610,360)
        self.ball = pygame.Rect(self.screen_width/2 - 7.5,self.screen_height/2 - 7.5, 15, 15)
        self.player = pygame.Rect(self.screen_width - 135, self.screen_height/2 - 15 ,10,90)
        self.opponent = pygame.Rect(self.screen_width - 710, self.screen_height/2 - 15 ,10,90)

        # Speed of Objects.
        self.ball_speed_x = 7 * random.choice((1,-1))
        self.ball_speed_y = 2 * random.choice((1,-1))
        self.player_speed = 0
        self.opponent_speed = 7

        # Score Initialization.
        self.player_score = 0
        self.opponent_score = 0

        # Game Sounds.
        self.pong_sound = pygame.mixer.Sound("Hello42.ogg")
        self.score_sound = pygame.mixer.Sound("Hello32.ogg")
        self.bat_sound = pygame.mixer.Sound("Hello52.ogg")
        self.click_sound = pygame.mixer.Sound("Hello100.ogg")
        self.game_sound = pygame.mixer.Sound("Hello500.ogg")

        # Boolean Initializations.
        self.ball_moving = False
        self.score_time = True
        self.click = False
        self.click2 = False
        self.click3 = False
        

    # This function moves the ball.

    def ball_animation(self):

        # Here in this code we are applying speed to the ball when the function is called in the game by defining both x and y axis of the ball.
        
        self.ball.x += self.ball_speed_x
        self.ball.y += self.ball_speed_y

        # This checks if the ball hits the top of the table so, the direction of ball gets inverted. 

        if self.ball.top <= ((self.screen_height - self.table_height)/2) or self.ball.bottom >= 450:
            pygame.mixer.Sound.play(self.pong_sound)
            self.ball_speed_y *= -1

        # This checks if the ball hits the left side of the table so, the player gets the point.

        if self.ball.left <= ((self.screen_width - self.table_width)/2):
            self.score_time = pygame.time.get_ticks()
            pygame.mixer.Sound.play(self.score_sound)
            self.player_score += 1
            self.count += 1
            self.opponent_list.append(self.opponent_score)
            self.player_list.append(self.player_score)
            self.point_list.append(self.count)

        # This checks if the ball hits the right side of the table so, the opponent gets the point.
     
        if self.ball.right >= 713:
            self.score_time = pygame.time.get_ticks()
            pygame.mixer.Sound.play(self.score_sound)
            self.opponent_score += 1
            self.count += 1
            self.opponent_list.append(self.opponent_score)
            self.player_list.append(self.player_score)
            self.point_list.append(self.count)

        # This checks if the ball collides with the player paddle and reverses the direction of ball.
        # abs() gives absolute value. i.e  ( x = -45 )  =>  ( abs(x) = 45 )

        if self.ball.colliderect(self.player) and self.ball_speed_x > 0:
            pygame.mixer.Sound.play(self.pong_sound)
            pygame.mixer.Sound.play(self.bat_sound)
            if abs(self.ball.right - self.player.left) < 10:
                self.ball_speed_x *= -1

            elif abs(self.ball.bottom - self.player.top) < 10 and self.ball_speed_y > 0:
                self.ball_speed_y *= -1

            elif abs(self.ball.top - self.player.bottom) < 10 and self.ball_speed_y < 0:
                self.ball_speed_y *= -1

        # This checks if the ball collides with the opponent paddle and reverses the direction of ball.
        # abs() gives absolute value. i.e  ( x = -45 )  =>  ( abs(x) = 45 )

        if self.ball.colliderect(self.opponent) and self.ball_speed_x < 0:
            pygame.mixer.Sound.play(self.pong_sound)
            pygame.mixer.Sound.play(self.bat_sound)
            if abs(self.ball.left - self.opponent.right) < 10:
                self.ball_speed_x *= -1
            
            elif abs(self.ball.bottom - self.opponent.top) < 10 and self.ball_speed_y > 0:
                self.ball_speed_y *= -1

            elif abs(self.ball.top - self.opponent.bottom) < 10 and self.ball_speed_y < 0:
                self.ball_speed_y *= -1


    # This functoin moves player paddle.

    def player_animation(self):

        # In this code player paddle is given speed controlled by the player itself.
        # The paadles are also given limits.

        self.player.y += self.player_speed
        if self.player.top <= ((self.screen_height - self.table_height)/2):
            self.player.top = ((self.screen_height - self.table_height)/2)
        if self.player.bottom >= 450:
            self.player.bottom = 450
            

    # This function moves opponent paddle.

    def opponent_ai(self):

        # This code contains the AI logic. The paddle moves with the ball. if the ball goes up, the paddle moves up by itself. Similarly, it follows the ball in the downward motion too.

        if self.opponent.top <= self.ball.y:
            self.opponent.top += self.opponent_speed
        if self.opponent.bottom >= self.ball.y:
            self.opponent.bottom -= self.opponent_speed
        if self.opponent.top <= ((self.screen_height - self.table_height)/2):
            self.opponent.top = ((self.screen_height - self.table_height)/2)
        if self.opponent.bottom >= 450:
            self.opponent.bottom = 450
            

    # This function refreshes the game after a point and throws the ball in a random court.
    # It also generates a countdown.

    def ball_restart(self):

        self.opponent.center = (self.screen_width - 700, self.screen_height/2)
        self.player.center = (self.screen_width - 135, self.screen_height/2)
        self.ball.center = (self.screen_width/2 - 1,self.screen_height/2)
        self.current_time = pygame.time.get_ticks()
        
        if self.current_time - self.score_time < 700:
            number_three = self.game_font.render("3",False,self.light_grey)
            self.screen.blit(number_three,(self.screen_width/2 - 7,self.screen_height/2 - 10))

        if 700 < self.current_time - self.score_time < 1400:
            number_two = self.game_font.render("2",False,self.light_grey)
            self.screen.blit(number_two,(self.screen_width/2 - 7,self.screen_height/2 - 10))

        if 1400 < self.current_time - self.score_time < 2100:
            number_one = self.game_font.render("1",False,self.light_grey)
            self.screen.blit(number_one,(self.screen_width/2 - 7,self.screen_height/2 - 10))
        
        if self.current_time - self.score_time < 2100:
            self.ball_speed_y, self.ball_speed_x = 0,0
        else:
            self.ball_speed_x = 4 * random.choice((1,-1))
            self.ball_speed_y = 4 * random.choice((1,-1))
            self.score_time = None


#-----------------------------------------------------------------------------------| Menus |------------------------------------------------------------------------------------------------
# -------------------------------------------------------- This class conatins the game interface and all of the game menus. ----------------------------------------------------------------

#T his class inherits from GameBox class.

class Menus(GameBox):

    def __init__(self):

        super().__init__()


    # This function is overrided later in the code to draw text on the screen and buttons.
        
    def draw_text(self,text, font, color, surface, x, y):
        self.textobj = self.font.render(text,1,color)
        self.textrect = self.textobj.get_rect()
        self.textrect.topleft = (x,y)
        surface.blit(self.textobj, self.textrect)
        

    # This function holds the openning menu of the game.

    def main_menu(self): 
            
        while True:
            self.screen.fill((0,0,0))
            self.screen.blit(self.image1,(0,0))
            self.draw_text('MAIN MENU', self.font,(255,255,255), self.screen, 20, 20)
            mx, my = pygame.mouse.get_pos()
            button_1 = pygame.Rect(300,100,200,50)
            button_2 = pygame.Rect(300,200,200,50)

            if button_1.collidepoint((mx,my)):
                if self.click:
                    pygame.mixer.Sound.play(self.click_sound)
                    self.gameSelection_menu()
                    break
                
            if button_2.collidepoint((mx,my)):
                if self.click:
                    pygame.mixer.Sound.play(self.click_sound)
                    self.instructions()
                    break
            
            pygame.draw.rect(self.screen,(0,200,100),button_1)
            pygame.draw.rect(self.screen,(0,200,100),button_2)
            self.draw_text('Play Game',self.font,(255,255,255),self.screen,367,118)
            self.draw_text('Instructions',self.font,(255,255,255),self.screen,360,220)
            self.click = False

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                if event.type ==  MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.click = True

            pygame.display.update()
            self.mainClock.tick(60)


    # This function can be accessed in the game to understand the instructions of the game.

    def instructions(self):
        
        running = True
        while running:
            self.screen.fill((0,0,0))
            self.screen.blit(self.image1,(0,0))
            self.draw_text('INSTRUCTIONS',self.font,(255,255,255),self.screen,20,20)
            self.draw_text('1) ESC KEY  = Back.',self.font,(255,255,255),self.screen,20,100)
            self.draw_text('2) UP ARROW KEY = Move Paddle Upwards.',self.font,(255,255,255),self.screen,20,150)
            self.draw_text('3) DOWN ARROW KEY = Move Paddle Downwards.',self.font,(255,255,255),self.screen,20,200)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                             
            pygame.display.update()
            self.mainClock.tick(60)


    # This function appears before the game to select the points play.

    def gameSelection_menu(self):
        
        running = True
        while running:
            self.screen.fill((0,0,0))
            self.screen.blit(self.image1,(0,0))
            self.draw_text('SELECT GAME', self.font,(255,255,255), self.screen, 20, 20)
            mx, my = pygame.mouse.get_pos()
            button_3 = pygame.Rect(300,100,200,50)
            button_4 = pygame.Rect(300,200,200,50)
            button_5 = pygame.Rect(300,300,200,50)

            if button_3.collidepoint((mx,my)):
                self.break_point = 5
                if self.click2:
                    pygame.mixer.Sound.play(self.click_sound)
                    self.game_interface()
                    running = False
                    
            if button_4.collidepoint((mx,my)):
                self.break_point = 10
                if self.click2:
                    pygame.mixer.Sound.play(self.click_sound)
                    self.game_interface()
                    running = False
                    
            if button_5.collidepoint((mx,my)):
                if self.click2:
                    pygame.mixer.Sound.play(self.click_sound)
                    self.game_interface()
                    running = False
            
            pygame.draw.rect(self.screen,(0,100,100),button_3)
            pygame.draw.rect(self.screen,(0,100,100),button_4)
            pygame.draw.rect(self.screen,(0,100,100),button_5)
            self.draw_text('5 Point',self.font,(255,255,255),self.screen,375,120)
            self.draw_text('10 Point',self.font,(255,255,255),self.screen,375,220)
            self.draw_text('Practice',self.font,(255,255,255),self.screen,375,318)
            self.click2 = False

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                if event.type ==  MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.click2 = True

            pygame.display.update()
            self.mainClock.tick(60)


    # This function appears at when the game is over!  

    def gameEnd_menu(self):

        running = True
        while running:
            self.screen.fill((0,0,0))
            self.screen.blit(self.image1,(0,0))
            self.draw_text('GAME OVER!', self.font,(255,255,255), self.screen, 20, 20)
            mx, my = pygame.mouse.get_pos()
            button_6 = pygame.Rect(300,100,200,50)
            button_7 = pygame.Rect(300,200,200,50)
            button_8 = pygame.Rect(300,300,200,50)

            if button_6.collidepoint((mx,my)):
                if self.click3:
                    pygame.mixer.Sound.play(self.click_sound)
                    self.display_stats()
                    
            if button_7.collidepoint((mx,my)):
                if self.click3:
                    pygame.mixer.Sound.play(self.click_sound)
                    running = False
                    
            if button_8.collidepoint((mx,my)):
                if self.click3:
                    pygame.mixer.Sound.play(self.click_sound)
                    exit()
            
            pygame.draw.rect(self.screen,(0,50,100),button_6)
            pygame.draw.rect(self.screen,(0,50,100),button_7)
            pygame.draw.rect(self.screen,(255,0,0),button_8)
            self.draw_text('Statistics',self.font,(255,255,255),self.screen,370,117)
            self.draw_text('Play Again',self.font,(255,255,255),self.screen,368,218)
            self.draw_text('Exit',self.font,(255,255,255),self.screen,387,318)
            self.click3 = False

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                        
                if event.type ==  MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.click3 = True
  
            pygame.display.update()
            self.mainClock.tick(60)


    # This function shows game statistics.
    
    def display_stats(self):
  
        plt.plot( self.point_list,self.player_list , label = "Player")
        plt.plot( self.point_list,self.opponent_list, label = "Opponent")
        plt.xlabel('POINT TIME') 
        plt.ylabel('POINTS') 
        plt.title('GAME STATISTICS') 
        plt.legend() 
        plt.show()


    # This function draws the game and store points.

    def game_interface(self):

        self.player_list = []
        self.opponent_list = []
        self.count = 0
        self.point_list = []

        running = True
        while running:
            self.screen.fill((0,0,0))
            self.screen.blit(self.image,(0,0))
            self.draw_text('TABLE TENNIS',self.font,(255,255,255),self.screen,20,20)
            self.draw_text('OPPONENT',self.font,(255,255,255),self.screen,130,500)
            self.draw_text('PLAYER',self.font,(255,255,255),self.screen,640,500)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.player_speed += 7
                    if event.key == pygame.K_UP:
                        self.player_speed -= 7
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                        self.player_speed -= 7
                    if event.key == pygame.K_UP:
                        self.player_speed += 7

            
            self.ball_animation()
            self.player_animation()
            self.opponent_ai()

            pygame.draw.rect(self.screen,self.light_grey,self.tableBorder)       
            pygame.draw.rect(self.screen,self.green,self.table)
            pygame.draw.rect(self.screen,self.light_grey,self.player)
            pygame.draw.rect(self.screen,self.light_grey,self.opponent)
            pygame.draw.aaline(self.screen,self.light_grey,(115,(self.screen_height/2)),(720,(self.screen_height/2)))
            pygame.draw.aaline(self.screen,self.light_grey,((self.screen_width/2),100),(self.screen_width/2,450))
            pygame.draw.aaline(self.screen,self.light_grey,((self.screen_width/2)+1,100),((self.screen_width/2)+1,450))
            pygame.draw.aaline(self.screen,self.light_grey,((self.screen_width/2)-1,100),((self.screen_width/2)-1,450))
            pygame.draw.ellipse(self.screen,self.orange,self.ball)


            if self.score_time:
                if self.player_score == self.break_point or self.opponent_score == self.break_point:
                    running = False
                    pygame.mixer.Sound.play(self.game_sound)
                    self.gameEnd_menu()
                else:
                    self.ball_restart()

                
            self.player_text = self.game_font.render(f"{self.player_score}",False,self.light_grey)
            self.screen.blit(self.player_text,(660,470))

            self.opponent_text = self.game_font.render(f"{self.opponent_score}",False,self.light_grey)
            self.screen.blit(self.opponent_text,(160,470))
            
            pygame.display.update()
            self.mainClock.tick(60)


#-----------------------------------------------------------------------------------| Game Loop |--------------------------------------------------------------------------------------------
# ------------------------------- This code is the outer game loop. The application doesn't stops until the game is the exited by the user itself. ------------------------------------------

# This is the game loop.

Gameall = True
pygame.init()
game_sound = pygame.mixer.Sound("Hello500.ogg")
pygame.mixer.Sound.play(game_sound)

while Gameall:
    Menus().main_menu()








