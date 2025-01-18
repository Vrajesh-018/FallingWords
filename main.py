import asyncio
import os
import pygame
import random
import sys 

pygame.init()
pygame.mixer.init()

# Colour 
white = (255,255,255)
black = (0,0,0)
red = (255, 0, 0)

# Specifying Game Variables
HEIGHT = 700
WIDTH = 1100
font = pygame.font.SysFont(None, 60)
blockFont = pygame.font.SysFont(None, 30)
# headerFont = pygame.font.SysFont(None, 60)
clock = pygame.time.Clock()
Dir = os.getcwd()
Score = 0
HiScore = 0
gameOver = False
fps = 60

# Creating Game window
gameWindow = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Type Shooter !")
pygame.display.update()

# Background image of welcome page
wlcm_bgimg = pygame.image.load(f"{Dir}\\Data\\image\\wlcm.jpg")
wlcm_bgimg = pygame.transform.scale(wlcm_bgimg, (WIDTH, HEIGHT)).convert_alpha()

# Background Image of game
bgimg = pygame.image.load(f"{Dir}\\Data\\image\\Back.jpeg")
bgimg = pygame.transform.scale(bgimg, (WIDTH,HEIGHT)).convert_alpha()


# Text Functions
def Text_screen(text, colour, x, y):
    """ Function to write text on the screen """
    screen_text = font.render(text, True, colour)
    gameWindow.blit(screen_text, [x,y])
def Text_block(text, colour, x, y):
    """ Function to write text on the block """
    screen_text = blockFont.render(text, True, colour)
    gameWindow.blit(screen_text, [x,y])

# Function to create a list of words        
def wordList(lst):
    """ This function creates a list of words """
    Dir = os.getcwd()
    with open(f"{Dir}\\Data\\levels\\level1.txt", "r") as f:
        read = f.read()
        read = read.split(" ")
        for i in read:
            lst.append(i)

# Function to choose word randomly from list
def randomWord(lst):
    """ This function choose a random word from the list"""
    wordIndice = random.randint(0,len(lst)-2)
    word = lst[wordIndice]
    return word

# Checker Function
def checker(user_text, text):
    """ This function checks user input text with the random word chosen from the list """
    pass

    

# Game Loop
def gameLoop():
    """This is the game loop where the game begins"""
    # Game specific variables
    Header_Width = WIDTH
    Header_Height = 100
    exitGame = False
    block_x = random.randint(5, WIDTH-80)
    block_y = Header_Height
    block_size_x = 80
    block_size_y = 30
    init_Velocity = 1.5
    word_List = []
    global Score
    global Dir
    global gameOver
    global HEIGHT

    # Checking for High Score 
    global HiScore
    with open(f"{Dir}\\Data\\levels\\HiScore.txt", "r") as f:
        read = f.read()
        HiScore = int(read)

    # creating a list of words 
    wordList(word_List)
    # Choosing random word from the list
    text = randomWord(word_List)

    # Variables:-
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

        if gameOver:
            gameWindow.fill(white)
            Text_screen("Game Over !", red,(WIDTH/2)-150, 250)
            Text_screen(f"Score : {Score}    High Score : {HiScore}", black,(WIDTH/2)-280 ,350)
            Text_block("Press enter to play again", black, (WIDTH/2)-150, 450)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exitGame=True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        gameOver=False
                        gameLoop()
        else:
            block_y += init_Velocity
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exitGame=True
                
                if event.type== pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if user_text == text:
                            Score +=1
                            if Score>HiScore:
                                with open(f"{Dir}\\Data\\levels\\HiScore.txt", "r+") as f:
                                    read = f.read()
                                    HiScore = int(read)
                                    HiScore = Score
                                    f.truncate(0)
                                    f.seek(0)
                                    f.write(str(Score))
                        else:
                            Score -= 1
                            if Score <= 0:
                                Score = 0
                                gameOver=True
                        # checker(user_text, text)
                        block_y = 0
                        block_x = random.randint(Header_Height,WIDTH-80)
                        text = randomWord(word_List)

                    if event.key == pygame.K_BACKSPACE: 
                        # get text input from 0 to -1 i.e. end. 
                        user_text = user_text[:-1] 
                    # Unicode standard is used for string formation 
                    else: 
                        user_text += event.unicode
                        if event.key == pygame.K_SPACE:
                            user_text = ''
            if block_y == (HEIGHT-75):
                gameOver = True 

            # Gives background image
            gameWindow.blit(bgimg,(0,0))

            # Random block with random words
            pygame.draw.rect(gameWindow, white, [block_x, block_y, block_size_x, block_size_y])
            Text_block(text, black, block_x+15, block_y+5)

            # level up line :- score 10 points without crossing it to level up
            pygame.draw.rect(gameWindow,white,[0, (HEIGHT-175), WIDTH, 1])

            # end line
            pygame.draw.rect(gameWindow,red,[0, (HEIGHT-75), WIDTH, 1])

            # Header of the Game window
            pygame.draw.rect(gameWindow, white,[0, 0, Header_Width,Header_Height])
            Text_screen("Falling Words", black,30, 50)
            Text_screen(f"Score : {Score}   High Score : {HiScore}", black, 460, 50)
            
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
async def main():
    """ Main function i.e., welcome page"""
    # Welcome Page
    exitGame = False
    while not exitGame:
        gameWindow.blit(wlcm_bgimg,(0,0))
        Text_screen("Welcome to world of Falling Words!", black, WIDTH/7, HEIGHT-100 )
        Text_block("Press \"Enter\" or \"Spacebar\" to play", black, (WIDTH/3)-50, HEIGHT-50 )
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exitGame= True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key==pygame.K_RETURN:
                    gameWindow.blit(bgimg,(0,0))
                    gameLoop()
                    
        pygame.display.update()
        await asyncio.sleep(0)
        clock.tick(fps)

asyncio.run(main())