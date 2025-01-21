import os
import pygame
import random
import sys
import time

pygame.init()
pygame.mixer.init()

# Colour 
white = (255,255,255)
black = (0,0,0)
red = (255, 0, 0)
yellow = (255,244,20)
seaGreen = (46, 139, 87)

# Specifying Game Variables
HEIGHT = 750
WIDTH = 1200
clock = pygame.time.Clock()
Dir = os.getcwd()
Score = 0
HiScore = 0
level_Up_Score = 0
gameOver = False
exitGame = False
level = 1
fps = 30
word_List = []
init_Velocity = 3

# Creating Game window
gameWindow = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Type Shooter !")

# Background image of welcome page
wlcm_bgimg = pygame.image.load(f"{Dir}\\Data\\image\\wlcm.jpg")
wlcm_bgimg = pygame.transform.scale(wlcm_bgimg, (WIDTH, HEIGHT)).convert_alpha()

# Background Image of game
bgimg = pygame.image.load(f"{Dir}\\Data\\image\\Back.jpeg")
bgimg = pygame.transform.scale(bgimg, (WIDTH,HEIGHT)).convert_alpha()

# Text Function
def Text_screen(text, colour,fontSize, x, y):
    """ Function to write text on the screen """
    font = pygame.font.SysFont(None, fontSize)
    screen_text = font.render(text, True, colour)
    gameWindow.blit(screen_text, [x,y])

# Function to create a list of words        
def wordList(lst):
    """ This function creates a list of words """
    with open(f"{Dir}\\data\\files\\level{str(level)}.txt", "r") as f:
        read = f.read()
        read = read.split(" ")
        for i in read:
            lst.append(i)

# Function to choose word randomly from list
def randomWord(lst):
    """ This function choose a random word from the list"""
    wordIndice = random.randint(0,len(lst)-1)
    word = lst[wordIndice]
    return word

# Music Function
def gameMusic(fileName):
        """ This function Loads the music and plays it """
        pygame.mixer.music.load(f"{Dir}\\data\\music\\{fileName}.mp3")
        pygame.mixer.music.play()

# Checker Function
def checker(user_text, txt, block_position):
    """ This function checks user input text with the random word chosen from the list 
        and also increement or decreement the score """
    global Score, HiScore, gameOver, level_Up_Score,level, word_List, init_Velocity
    if user_text == txt:
        gameMusic("correct")
        Score +=1
        if block_position >= (HEIGHT-175):
                level_Up_Score = 0
        else:
            level_Up_Score += 1
            if level_Up_Score == 20:
                gameMusic("LevelUp")

                if level<3:
                    level_Up_Score = 0
                    level += 1
                    word_List = []
                    wordList(word_List)
                    text = randomWord(word_List)
                    levelUP("Level Up!",(WIDTH/3)+50, HEIGHT/2)
                else:
                    init_Velocity += 0.5
                    levelUP("You're a fast Typist!", (WIDTH/4)+30, HEIGHT/2)

        if Score>HiScore:
            with open(f"{Dir}\\data\\files\\HiScore.txt", "w") as f:
                HiScore = Score
                f.write(str(Score))
    else:
        gameMusic("incorrect")
        Score -= 1
        level_Up_Score =0
        if Score <= 0:
            gameMusic("gameOver")
            Score = 0
            gameOver=True

def levelUP(txt, x, y):
    """ Shows text on the screen when the player level ups """
    Text_screen(txt, yellow, 80, x, y)
    pygame.display.update()
    time.sleep(1)

def blockSize(txt):
    """ Changes the size of the falling block """
    text_length = len(txt)
    size = 16 * text_length
    return size

def rulesAndInstructions():
    """ Rules and Instruction of the games """
    r1 = "1. Score Consecutive 20 points without letting the block cross white line to level up"
    r2 = "2. if the word block crosses the red line it's Game Over "
    r3 = "3. Hit \"Space bar\" to get a new word"
    r4 = "4. You get +1 for every correct word and -1 for every negative word "
    r5 = "5. If your score ever become 0, the Game will end"
    r6 = "6. Press \"F1\" to pause and replay"
    while True:
        gameWindow.fill(white)
        Text_screen("Rules : ", black,80, 30, 100 )
        Text_screen( r1, black, 30, 60, 200 )
        Text_screen( r2, black, 30, 60, 250 )
        Text_screen( r3, black, 30, 60, 300 )
        Text_screen( r4, black, 30, 60, 350 )
        Text_screen( r5, black, 30, 60, 400 )
        Text_screen( r6, black, 30, 60, 450 )
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main()
        pygame.display.update()

# Game Loop
def gameLoop():
    """ This is the game loop where the game begins """
    global Score, gameOver, HiScore, exitGame, word_List

    # Header Dimension
    Header_Width = WIDTH
    Header_Height = 130

    # Checking for High Score 
    with open(f"{Dir}\\data\\files\\HiScore.txt", "r") as f:
        read = f.read()
        HiScore = int(read)

    # creating a list of words 
    wordList(word_List)
    # Choosing random word from the list
    text = randomWord(word_List)

    # Falling Block Dimensions
    block_size_x = blockSize(text)
    block_size_y = 30
    block_x = random.randint(5, WIDTH-(block_size_x-15))
    block_y = Header_Height
    # Velocity of falling block

    # Dimension of Input Box
    box_left = 50
    box_top = HEIGHT-50
    box_width = WIDTH-100
    box_height = 32
	
	# basic font for user typed 
    base_font = pygame.font.Font(None, 32) 
    user_text = '' 
	# create rectangle
    input_rect = pygame.Rect(box_left, box_top, box_width, box_height) 
    color = pygame.Color('lightskyblue3') 

    while not exitGame:
        pause = False
        if gameOver:
            gameWindow.fill(white)
            Text_screen("Game Over !", red, 80, (WIDTH/2)-180, 250)
            Text_screen(f"Score : {Score}    High Score : {HiScore}", black, 60, (WIDTH/2)-280 ,350)
            Text_screen("Press enter to play again", black, 30, (WIDTH/2)-150, 450)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exitGame=True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        Score = 0
                        gameOver=False
                        gameLoop()
        else:
            block_y += init_Velocity
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exitGame=True                    
                
                if event.type== pygame.KEYDOWN:

                    if event.key == pygame.K_SPACE:
                        checker(user_text, text,block_y)
                        text = randomWord(word_List)
                        block_size_x = blockSize(text)
                        block_y = Header_Height
                        block_x = random.randint(5, WIDTH-(block_size_x-20))

                    if event.key == pygame.K_BACKSPACE: 
                        # get text input from 0 to -1 i.e. end. 
                        user_text = user_text[:-1] 
                    # Unicode standard is used for string formation 
                    else: 
                        user_text += event.unicode
                        if event.key == pygame.K_SPACE:
                            user_text = ''
                    if event.key == pygame.K_F1:
                        while not pause:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    sys.exit()
                                    
                                if event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_F1:
                                        pause = True
                            gameWindow.fill('lightskyblue3')
                            Text_screen("Game Paused", red, 80,(WIDTH/2)-180, (HEIGHT/2)-50)
                            Text_screen("Press \"F1\" to continue", black, 30, (WIDTH/3)+100, (HEIGHT/2)+30)
                            pygame.display.update()
            if block_y >= (HEIGHT-75):
                gameMusic("gameOver")
                gameOver = True 

            # Gives background image
            gameWindow.blit(bgimg,(0,0))

            # Random block with random words
            pygame.draw.rect(gameWindow, white, [block_x, block_y, block_size_x, block_size_y])
            Text_screen(text, black , 30, block_x+10, block_y+5)

            # level up line :- score 10 points without crossing it to level up
            pygame.draw.rect(gameWindow,white,[0, (HEIGHT-175), WIDTH, 1])

            # End line
            pygame.draw.rect(gameWindow,red,[0, (HEIGHT-75), WIDTH, 1])

            # Header of the Game window
            pygame.draw.rect(gameWindow, white,[0, 0, Header_Width,Header_Height])
            Text_screen("Falling Words", black, 80,30, 50)
            Text_screen(f"Score : {Score}   High Score : {HiScore}", black, 60, WIDTH-600, 30)
            Text_screen(f"Score neended to level up : {20 - level_Up_Score}", black, 30, WIDTH-500, 85 )
            
            # draw rectangle and argument passed which should be on screen 
            pygame.draw.rect(gameWindow, color, input_rect) 
            text_surface = base_font.render(user_text, True, black) 
            
            # render at position stated in arguments 
            gameWindow.blit(text_surface, (input_rect.x+5, input_rect.y+5)) 
            
            # set width of textfield so that text cannot get outside of user's text input 
            input_rect.w = max(WIDTH-100, text_surface.get_width()+10) 

            # display.flip() will update only a portion of the screen to updated, not full area 
            pygame.display.flip() 
        
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    sys.exit()

#__main__
def main():
    """ Main function i.e., welcome page"""
    # Welcome Page
    global exitGame
    while not exitGame:
        gameWindow.blit(wlcm_bgimg,(0,0))
        Text_screen("Welcome to world of Falling Words!", black, 80, (WIDTH/10), HEIGHT-130 )
        Text_screen("Press \"Enter\" or \"Spacebar\" to play", black, 30, (WIDTH/3)-20, HEIGHT-60 )
        Text_screen("Press \"R\" for rules ", black, 30, (WIDTH/3)+50, HEIGHT-30 )
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exitGame= True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key==pygame.K_RETURN:
                    gameWindow.blit(bgimg,(0,0))
                    gameLoop()
                if event.key == pygame.K_r:
                    rulesAndInstructions()
                    
        pygame.display.update()
        clock.tick(fps)

main()