#Manic Mansion

#importerer nødvendige biblioteker
import pygame as pg
import random 
import sys


# Konstanter
WIDTH = 800  # Bredden til vinduet
HEIGHT = 600 # Høyden til vinduet

# Størrelsen til vinduet
SIZE = (WIDTH, HEIGHT)

#Frames per sekund (bilder per sekund)
FPS = 60


#Farger (RGB)
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
GREY = (152,152,152)
LIGHTBLUE = (140,160,255)



# Initiere pygame
pg.init()

# Lager en overflate (surface) vi kan tegne på
surface = pg.display.set_mode(SIZE)

# Lager en klokke
clock = pg.time.Clock()

# Variabel som styrer om spillet skal kjøres
run = True




#Startposisjon
x = WIDTH/2
y = HEIGHT- 40

# Henter font
font = pg.font.SysFont('Arial', 22)


poeng = 0 

# Funksjon som viser antall poeng
def skrivPoeng():
    tekst = font.render(f"Antall poeng: {poeng}", True, BLACK)
    #metode som putter bilde oppå bilde, klistremerke
    surface.blit(tekst, (20,20))

def gameOver():
    tekstGameOver = font.render("GAME OVER", True, BLACK)
    surface.blit(tekstGameOver, (300,300))
    


class Objekt:
    # konstruktør
    def __init__(self):
        self.w = 40 #bredde
        self.h = 40 #høyde
        self.x = 60 #x-posisjon
        self.y = 280 #y-posisjon
        self.farge = LIGHTBLUE
    def tegn(self):
        pg.draw.rect(surface, self.farge, (self.x,self.y,self.w, self.h))
        
class Menneske(Objekt):
    def __init__(self):
        super().__init__()
        self.farge = BLUE
    
    def oppdater(self):
        self.x += vx
        self.y += vy
        
class Spokelse(Objekt):
    def __init__(self):
        super().__init__()
        self.x = random.randint(190,610)
        self.y = random.randint(70,530)
        self.farge = GREY
        
        
    def oppdater(self):
        self.x += vx2
        self.y += vy2

class Hindring(Objekt):
    def __init__(self):
        super().__init__()
        self.x = random.randint(190,610)
        self.y = random.randint(70,530)
        self.farge = GREEN
        
class Sau(Objekt):
    def __init__(self):
        super().__init__()
        self.x = random.randint(690,750)
        self.y = random.randint(70,530)
        
   
        
        
# Lager et objekt
objekt = Objekt()

#Lager et menneske
menneske = Menneske()

spokelse = Spokelse()

hindringer = [Hindring(), Hindring(), Hindring()]

sauer = [Sau(), Sau(), Sau()]

#Hastighet spøkelse
vx2 = 1
vy2 = 1

#Spill-løkken
while run:
    #Sørger for at løkken kjører i korrekt hastighet
    clock.tick(FPS)
    
    #Går gjennom hendelser (events)
    for event in pg.event.get():
        #Sjekker om vi ønsker å lukke vinduet
        if event.type==pg.QUIT:
            run = False # Spillet skal avsluttes
    
    
    
    surface.fill(WHITE)
    
    #Hastigheten til spilleren
    vx = 0
    vy = 0
    
    #Henter knappene fra tastaturet som trykkes på
    keys = pg.key.get_pressed()
    
    # Sjekker om ulike taster trykkes på og endrer posisjon på mennesket
    if keys[pg.K_LEFT]:
        vx -= 5
       
    elif keys[pg.K_RIGHT]:
        vx += 5
    
    elif keys[pg.K_UP]:
        vy -= 5
        
    elif keys[pg.K_DOWN]:
        vy += 5
    
    #Oppdaterer posisjonen til mennesket
    menneske.oppdater()
    
    
    spokelse.x += vx2
    spokelse.y += vy2
    
   
    
    #Sjekker spøkelse kollisjon med frisone venstre 
    if  spokelse.x <= 150 :
        vx2 *= -1
        spokelse.x= 150
       
        
    #Sjekker spøkelse kollisjon med frisone høyre
    if spokelse.x + spokelse.w >= 650:
        vx2 *= -1
        spokelse.x = 650 - spokelse.w
        
    
    # Sjekker kollisjon med toppen
    if spokelse.y + spokelse.h >= HEIGHT:
        vy2 *= -1 #snur hastigheten
        spokelse.y = HEIGHT - spokelse.h
        
    # Sjekker kollisjonen med bunnen
    if spokelse.y <= 0:
        vy2 *= -1 #snur hastigheten
        spokelse.y = 0
        
    
    #oppdaterer posisjonen til spøkelset 
    spokelse.oppdater()
    
    
    #sjekker menneske kollisjon med høyre side
    if menneske.x <= 0 :
        menneske.x = 0
    
    #sjekker menneske kollisjon med høyre side 
    if menneske.x + menneske.w >= WIDTH:
        menneske.x = WIDTH - 40
        
    #sjekker menneske kollisjon med topp
    if menneske.y <= 0:
        menneske.y = 0
    
    if menneske.y + menneske.h >= HEIGHT:
        menneske.y = HEIGHT - menneske.h
    
    
    
    #MÅ FIKSE
    #sjekker menneske kollisjon med hindringer
    for hindring in hindringer:
        if hindring.x < menneske.x < hindring.x + hindring.w and hindring.y < menneske.y < hindring.y + hindring.h:
           run = False
           gameOver()
           
            
    
    
    #Sjekker kollisjon med sau
    for sau in sauer: 
        if sau.x < menneske.x < sau.x + sau.w and sau.y < menneske.y < sau.y + sau.h:
            sauer.remove(sau)
            
    if len(sauer) < 3 and menneske.x < 150:
        poeng += 1
        sauer.append(Sau())
        
                
                    
            
    
    
    #sjekker kollisjon med spøkelse 
    if spokelse.x < menneske.x < spokelse.x + spokelse.w and spokelse.y <menneske.y < spokelse.y + spokelse.h:
        run = False
        gameOver()
        
            
    
   
    
        
    menneske.tegn()
    
    spokelse.tegn()
    
    for hindring in hindringer:
        hindring.tegn()
        
    for sau in sauer:
        sau.tegn()
    
    #Lager fri sone linjer 
    pg.draw.rect(surface, BLACK, (150, 0, 1, 600))
    pg.draw.rect(surface, BLACK, (650, 0, 1, 600))
    
    
    skrivPoeng()
    
    
    # "Flipper" displayet for å vise hva vi har tegnet
    pg.display.flip()
    


# Avslutter pygame
pg.quit()
sys.exit() # Dersom det ikke er tilstrekkelig med pg.quit()


    







