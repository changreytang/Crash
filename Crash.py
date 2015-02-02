import pygame
import time
import random
import cImage

display_width = 800
display_height = 600

white = (255,255,255) #RGB
black = (0,0,0)
red = (200,0,0)
green = (0,200,0)
blue = (0,0,200)
bright_red = (255,0,0)
bright_green = (0,255,0)
gray = (72,72,72)

pygame.init() #make a racing game
gameDisplay = pygame.display.set_mode((display_width,display_height)) #window size 800x600
pygame.display.set_caption("Crash") #window title
clock = pygame.time.Clock() #game clock (fps)

carImg = pygame.image.load("racecarB.gif") #load image of car you are controlling
Image = cImage.FileImage("racecarB.gif")
car2Img = pygame.image.load("racecarR.gif") #load image of car you are trying not to hit
Image2 = cImage.FileImage("racecarR.gif")
car_width = Image.getWidth() #width of car you drive
car_height = Image.getHeight() #height of car you drive

highscore = {"highscore":0}

def things(thingx, thingy, thingw, thingh, color): #draws the rectangles for the streets
    pygame.draw.rect(gameDisplay, color, [thingx,thingy,thingw,thingh])             

def car(x,y):
    gameDisplay.blit(carImg,(x,y)) #drawing the your car at (x,y)

def car2(x,y):
    gameDisplay.blit(car2Img,(x,y)) #drawing enemy car at (x,y)

def text_objects(text,font,color):
    textSurface = font.render(text, True, color) #first parameter: text, second parameter: anti-aliasing, third parameter: color
    return textSurface, textSurface.get_rect()

def score_objects(text,font): 
    scoreSurface = font.render(text, True, green)
    return scoreSurface, scoreSurface.get_rect()

def hscore_objects(text,font):
    hscoreSurface = font.render(text, True, blue)
    return hscoreSurface, hscoreSurface.get_rect()

def hscore_display(text):
    hscoreText = pygame.font.Font("freesansbold.ttf",20)
    hscoreSurf, hscoreRect = hscore_objects(text,hscoreText)
    hscoreRect.center = (70,display_height-20)
    gameDisplay.blit(hscoreSurf,hscoreRect)

def score_display(text): #displays the score in the top, middle of the screen
    scoreText = pygame.font.Font("freesansbold.ttf",45)
    scoreSurf, scoreRect = score_objects(text, scoreText)
    scoreRect.center = ((display_width/2),30)
    gameDisplay.blit(scoreSurf,scoreRect)

def message_display(text):
    largeText = pygame.font.Font("freesansbold.ttf",115) #pick the font and size of the text
    TextSurf, TextRect = text_objects(text,largeText,red)
    TextRect.center = ((display_width/2),(display_height/2)) #place the text box in the middle of the screen
    gameDisplay.blit(TextSurf,TextRect) #draws the text and text-rectangle onto screen (runs in the background)

    pygame.display.update() #update the screen

    time.sleep(2) #2 seconds to respond

    game_loop() #restarts the game

def button(msg,x,y,w,h,i,a,action=None):
    pygame.draw.rect(gameDisplay,i,(x,y,w,h))

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay,a,(x,y,w,h))
        if click[0] == 1 and action != None:
            action()

    smallText = pygame.font.Font("freesansbold.ttf",40)
    textSurf, textRect = text_objects(msg, smallText, white)
    textRect.center = ((x+(w//2)),(y+(h//2)))
    gameDisplay.blit(textSurf,textRect)

def game_exit():
    pygame.quit()
    quit()

def crash():
    message_display("You Crashed") #display this message when you crash

def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit()
        gameDisplay.fill(white)
        largeText = pygame.font.Font("freesansbold.ttf",115)
        TextSurf, TextRect = text_objects("Crash",largeText,black)
        TextRect.center = ((display_width/2),(display_height/2))
        gameDisplay.blit(TextSurf,TextRect)

        button("Play",display_width//5,display_height//10*8,display_width//5,display_height//10,green,bright_green,game_loop)
        button("Quit",display_width//5*3,display_height//10*8,display_width//5,display_height//10,red,bright_red,game_exit)
        
        pygame.display.update()
        clock.tick(60)

def game_loop():
    x = (display_width/2-car_width/2) #where the car is gonna be drawn in the beginning
    y = (display_height-car_height)

    x_change = 0
    y_change = 0

    step1 = 0 #where the road starts
    step2 = display_height/10*2
    step3 = display_height/10*4
    step4 = display_height/10*6
    step5 = display_height/10*8
    
    car2_width = Image2.getWidth() #enemy car width
    car2_height = Image2.getHeight() #enemy car height
    car2_startx = random.randrange(0,(display_width-car2_width)) #thing object starts at anypoint within the width of the screen
    car2_starty = -600 #thing object starts 600 pixels above the screen
    car2_speed = 7

    score = 0 #starting score

    speed = 5 #start speed of the road

    gameExit = False

    while not gameExit:

        for event in pygame.event.get(): #takes in each user event per frame
            if event.type == pygame.QUIT: #pygame.QUIT is the "X" button on window
                game_exit()

            if event.type == pygame.KEYDOWN: #if you push down a key
                if event.key == pygame.K_LEFT: #if you push down left arrow key
                    x_change = -5
                elif event.key == pygame.K_RIGHT: #if you push down right arrow key
                    x_change = 5
                elif event.key == pygame.K_UP:
                    y_change = -5
                elif event.key == pygame.K_DOWN:
                    y_change = 5

            if event.type == pygame.KEYUP: #if you let go of key
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y_change = 0
                
        x += x_change #updates the left and right movement of the car
        y += y_change
        
        gameDisplay.fill(white) #fills the bg with white

        #def things(thingx, thingy, thingw, thingh, color)
        things(display_width/4,0,5,display_height,gray) #the road
        things(display_width/4*3,0,5,display_height,gray)
        things(display_width/4*2,step1,5,display_height/10,gray)
        step1 += speed
        things(display_width/4*2,step2,5,display_height/10,gray)
        step2 += speed
        things(display_width/4*2,step3,5,display_height/10,gray)
        step3 += speed
        things(display_width/4*2,step4,5,display_height/10,gray)
        step4 += speed
        things(display_width/4*2,step5,5,display_height/10,gray)
        step5 += speed

        car2(car2_startx,car2_starty)
        car2_starty += car2_speed #moves the block down
        car(x,y) #draws the car
        score_display(str(score))
        hscore_display("Highscore:"+str(highscore["highscore"]))

        if score > highscore["highscore"]:
            highscore["highscore"] = score

        if x > (display_width-car_width) or x < 0: #if you hit the side of the window
            crash() #run crash function
            score = 0

        if y < -100 or y > display_height:
            crash()
            score = 0

        if step1 > display_height: #the moving part of the road is reset everytime it hits the bottom of the screen
            step1 = -15
        if step2 > display_height:
            step2 = -15
        if step3 > display_height:
            step3 = -15
        if step4 > display_height:
            step4 = -15
        if step5 > display_height:
            step5 = -15

        if car2_starty > display_height: #if enemy car hits the end of the screen
            if score < 25: 
                car2_starty = 0 - car2_height #redraw the block at top of screen
                car2_startx = random.randrange(0,(display_width-car2_width)) #redraw block at a point within the width of the window
                car2_speed = random.randint(5,7) #cars are slow
                score += 1 #score increases by 1 each time a car passes
                speed = 7 #the road moves slowly
            elif score >= 25 and score < 50:
                car2_starty = 0 - car2_height #redraw the block at top of screen
                car2_startx = random.randrange(0,(display_width-car2_width)) #redraw block at a point within the width of the window
                car2_speed = random.randint(7,8) #cars are medium speed
                score += 1
                speed = 8 #the road moves faster
            elif score >= 50 and score < 75:
                car2_starty = 0 - car2_height #redraw the block at top of screen
                car2_startx = random.randrange(0,(display_width-car2_width)) #redraw block at a point within the width of the window
                car2_speed = random.randint(8,10) #cars are fast
                score += 1
                speed = 9
            elif score >= 75 and score < 100:
                car2_starty = 0 - car2_height #redraw the block at top of screen
                car2_startx = random.randrange(0,(display_width-car2_width)) #redraw block at a point within the width of the window
                car2_speed = random.randint(10,12) #cars are godly speed
                score += 1
                speed = 10
            elif score >= 100:
                car2_starty = 0 - car2_height #redraw the block at top of screen
                car2_startx = random.randrange(0,(display_width-car2_width)) #redraw block at a point within the width of the window
                car2_speed = random.randint(12,16) #cars be impossible to dodge
                score += 1
                speed = 11
            

        if (y < car2_starty+car2_height and y > car2_starty) or (y+car_height < car2_starty+car2_height and y+car_height > car2_starty) :
            print("y crossover")

            if (x > car2_startx and x < car2_startx+car2_width) or (x+car_width > car2_startx and x+car_width < car2_startx+car2_width):
                print("x crossover")
                crash()
                score = 0

        pygame.display.update() #updates the frame
        clock.tick(120) #120 frames per second

game_intro()
game_loop()
game_exit()


            
    
