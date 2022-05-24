import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SpaceBattle")

#Colors!
SPACEPURPLE = (251,248,253)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)



BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)
FPS = 60
SHIPWIDTH = 70
SHIPLENGTH = 70
BULLET_VEL = 7
MAX_BULLETS = 3
VEL = 5

#weird events that are made when something is hit
ALIEN_HIT = pygame.USEREVENT + 1
HUMAN_HIT = pygame.USEREVENT + 2

#bullet hit sounds
BULLET_HIT = pygame.mixer.Sound(os.path.join("SoundImage","Explosion.mp3"))
BULLET_FIRE = pygame.mixer.Sound(os.path.join("SoundImage","LazerShot.wav"))

#assigning fonts
HEALTHFONT = pygame.font.SysFont("comicsans", 40)
WINNERFONT = pygame.font.SysFont("comicsans", 100)


#image transformations and getting images from the SoundImaage folder 
ALIEN_SHIP = pygame.image.load(os.path.join("SoundImage", "AlienShip.png"))
ALIEN_SHIP = pygame.transform.rotate(pygame.transform.scale(ALIEN_SHIP, (SHIPWIDTH, SHIPLENGTH)), 90)
HUMAN_SHIP = pygame.image.load(os.path.join("SoundImage", "HumanShip.png"))
HUMAN_SHIP = pygame.transform.rotate(pygame.transform.scale(HUMAN_SHIP, (SHIPWIDTH, SHIPLENGTH)), 270)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join("SoundImage", "Space.png")), (WIDTH, HEIGHT))

def PurpleWindow(Alien, Human, Human_Bullets, Alien_Bullets, AlienHP, HumanHP):
    WINDOW.blit(SPACE, (0, 0))
    pygame.draw.rect(WINDOW, BLACK, BORDER)

    AlienHPTxt = HEALTHFONT.render("Health: " + str(AlienHP),1 , SPACEPURPLE)
    HumanHPTxt = HEALTHFONT.render("Health: " + str(HumanHP),1 , SPACEPURPLE)
    WINDOW.blit(AlienHPTxt, (WIDTH - AlienHPTxt.get_width()-10, 10))
    WINDOW.blit(HumanHPTxt, (10, 10))

    WINDOW.blit(ALIEN_SHIP, (Alien.x, Alien.y))
    WINDOW.blit(HUMAN_SHIP, (Human.x, Human.y))


#Drawing Bullets for both ships
    for Bullets in Alien_Bullets:
        pygame.draw.rect(WINDOW, RED, Bullets)
    for Bullets in Human_Bullets:
        pygame.draw.rect(WINDOW, YELLOW, Bullets)

    pygame.display.update()

def HumanMovementKeys(KeysPressed, Human):
    if KeysPressed[pygame.K_a] and Human.x - VEL > 0:
        Human.x -= VEL
    if KeysPressed[pygame.K_d] and Human.x + VEL + Human.width < BORDER.x:
        Human.x += VEL
    if KeysPressed[pygame.K_w] and Human.y - VEL > 0:
        Human.y -= VEL
    if KeysPressed[pygame.K_s] and Human.y + VEL + Human.height < HEIGHT:
        Human.y += VEL

def AlienMovementKeys(KeysPressed, Alien):
    if KeysPressed[pygame.K_LEFT] and Alien.x - VEL > BORDER.x + BORDER.width:
        Alien.x -= VEL
    if KeysPressed[pygame.K_RIGHT] and Alien.x + VEL + Alien.width < WIDTH:
        Alien.x += VEL
    if KeysPressed[pygame.K_UP] and Alien.y - VEL > 0:
        Alien.y -= VEL
    if KeysPressed[pygame.K_DOWN] and Alien.y + VEL + Alien.height < HEIGHT:
        Alien.y += VEL

def BulletsFunction(Alien_Bullets, Human_Bullets, Alien, Human):
    for Bullet in Alien_Bullets:
        Bullet.x -= BULLET_VEL
        if Human.colliderect(Bullet):
            pygame.event.post(pygame.event.Event(HUMAN_HIT))
            Alien_Bullets.remove(Bullet)
        elif Bullet.x < 0:
            Alien_Bullets.remove(Bullet)
    for Bullet in Human_Bullets:
        Bullet.x += BULLET_VEL
        if Alien.colliderect(Bullet):
            pygame.event.post(pygame.event.Event(ALIEN_HIT))
            Human_Bullets.remove(Bullet)
        elif Bullet.x > WIDTH:
            Human_Bullets.remove(Bullet)

def Winner(text):
    DrawText = WINNERFONT.render(text, 1, SPACEPURPLE)
    WINDOW.blit(DrawText, (WIDTH/2 - DrawText.get_width()/2, HEIGHT/2 - DrawText.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

def Main():
    Alien = pygame.Rect(700, 300, SHIPWIDTH, SHIPLENGTH)
    Human = pygame.Rect(100, 300, SHIPWIDTH, SHIPLENGTH)

    Alien_Bullets = []
    Human_Bullets = []
    AlienHP = 10
    HumanHP = 10

    Clock = pygame.time.Clock()
    Run = True
    while Run:
        Clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Run = False

#What Bullets are shot, when, how and size
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RCTRL and len(Alien_Bullets) < MAX_BULLETS:
                    Bullet = pygame.Rect(Alien.x, Alien.y + Alien.height//2 - 2, 10, 5)
                    Alien_Bullets.append(Bullet)
                    BULLET_FIRE.play()
                if event.key == pygame.K_LCTRL and len(Human_Bullets) < MAX_BULLETS:
                    Bullet = pygame.Rect(Human.x + ((SHIPLENGTH/7)*6), Human.y + Human.height//2 - 2, 10, 5)
                    Human_Bullets.append(Bullet)
                    BULLET_FIRE.play()
            if event.type == ALIEN_HIT:
                AlienHP -= 1
                BULLET_HIT.play()
            if event.type == HUMAN_HIT:
                HumanHP -= 1
                BULLET_HIT.play()
        
        WinnerText = ""
        if AlienHP <= 0:
            WinnerText = "Human Wins!"
        if HumanHP <= 0:
            WinnerText = "Alien Wins!"
        if WinnerText != "":
            Winner(WinnerText)
            break

        BulletsFunction(Alien_Bullets, Human_Bullets, Alien, Human)
        KeysPressed = pygame.key.get_pressed()
        HumanMovementKeys(KeysPressed, Human)
        AlienMovementKeys(KeysPressed, Alien)
        PurpleWindow(Alien, Human, Human_Bullets, Alien_Bullets, AlienHP, HumanHP)
        
    pygame.quit()

if __name__ == "__main__":
    Main()
