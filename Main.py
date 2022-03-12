from sqlite3 import Row
from this import s
from Classes import *

#Init pygame
pygame.init()
pygame.mixer.init()

#Variables Globales
sprite_pokemons = pygame.sprite.Group()
sprite_botones = pygame.sprite.Group()
sonido_fondo = pygame.mixer.Sound("sonidos_ambientales/MusicaFondo.mp3")
Mouse = Cursor()

#Reproducir
#pygame.mixer.Sound.play(sonido_fondo)

#Funciones

## Funcion que carga los datos de los pokemons
def LoadData():
    global sprite_pokemons
    with open("dex.txt", encoding="utf8", errors='ignore') as Data:
        Data = Data.read().split("\n")
        Data.pop(0)
        for pokemon in Data:
            poke = pokemon.split("-")
            sprite_pokemons.add(Pokemon(poke[0],poke[1],poke[3],poke[4],poke[5],poke[6]))
    with open("pokedex.txt", encoding="utf8", errors='ignore') as DataKnow:
        DataKnow = DataKnow.read().split(",")
        for know in DataKnow:
            for pokemon in sprite_pokemons:
                if(know==pokemon.numero):
                    pokemon.descubierto = True
## Ventana de juego
def GameWindow():
    global sprite_pokemons,sprite_botones,Mouse
    #Reloj
    clock = pygame.time.Clock()

    #Grupo de Sprites
    LoadData()

    #Fuente a utilizar
    Font = pygame.font.SysFont(None, 21)

    #Texto
    # text = Font.render("Lado o Radio", True, (255,255,255))

    #Botones
    #sprite_botones.add(Boton("B_cen","sprites/B_Cen.png","sprites/B_Cen_S.png",100,300,0,0))
    sprite_botones.add(Boton("B_Down","sprites/B_Down.png","sprites/B_Down_S.png",100,350,0,0))
    sprite_botones.add(Boton("B_Up","sprites/B_Up.png","sprites/B_Up_S.png",100,250,0,0))
    sprite_botones.add(Boton("B_Right","sprites/B_Right.png","sprites/B_Right_S.png",150,300,0,0))
    sprite_botones.add(Boton("B_Left","sprites/B_Left.png","sprites/B_Left_S.png",50,300,0,0))
    sprite_botones.add(Boton("B_Start","sprites/btn.png","sprites/btn_S.png",200,250,0,0))
    sprite_botones.add(Boton("B_Menu","sprites/btn.png","sprites/btn_S.png",250,250,0,0))
    sprite_botones.add(Boton("B_Info","sprites/Info.png","sprites/Info_S.png",200,410,0,0))
    sprite_botones.add(Boton("B_On","sprites/Off.png","sprites/On.png",41,130,20,20))
    sprite_botones.add(Boton("B_Rowr","sprites/Rowr.png","sprites/Rowr_S.png",280,300,0,0))
    sprite_botones.add(Boton("B_Sound","sprites/Sonido_A.png","sprites/Sonido_D.png",41,400,0,0))

    #Ajustes de ventana
    pygame.display.set_caption("Proyecto Pokedex")
    screen = pygame.display.set_mode([350,500])

    fondo = pygame.image.load("sprites/Fondo.png")
    consolaOn = pygame.image.load("sprites/Consola_E.png")
    consolaOff = pygame.image.load("sprites/Consola.png")

    # Posicion de pokemon
    posicion = 1

    # Boolean para cuando el boton derecho esta precionado
    mouseI = False
    mouseD = False
    isConsolaOn = False
    Rowr = False
    Intro = False
    Info = False
    info = ""
    Wait = 0
    #Ciclo que corre la ventana principal
    run = True
    while run:
        #Eventos
        events_list = pygame.event.get()
        for eventos in events_list:
            if eventos.type == pygame.QUIT:
                run = False
            # Cuando un boton del mause se preiona
            if eventos.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0] == True:
                    mouseI = True
                elif pygame.mouse.get_pressed()[1] == True:
                    pass
                elif pygame.mouse.get_pressed()[2] == True:
                    mouseD = True
            # Cuando un boton del mause se levanta
            if eventos.type == pygame.MOUSEBUTTONUP:
                mouseI = False
                mouseD = False
        #Elementos Fijos
        screen.blit(fondo, (0,0))
        if(mouseI):
            for boton in sprite_botones:
                if(Mouse.colliderect(boton.rect)):
                    if(boton.accion == "B_On"):
                        if(not isConsolaOn):
                            Intro = True

                        isConsolaOn = not isConsolaOn
                        pygame.time.wait(100)
                    if(boton.accion == "B_Right" and not Intro and  not Info and isConsolaOn):
                        posicion+=1
                        if(posicion>151):
                            posicion=1
                        pygame.time.wait(100)
                    if(boton.accion == "B_Left" and not Intro and  not Info and isConsolaOn):
                        posicion-=1
                        if(posicion<1):
                            posicion=151
                        pygame.time.wait(100)
                    if(boton.accion == "B_Rowr"):
                        if(isConsolaOn):
                            Rowr = True
                    if(boton.accion == "B_Info"):
                        Info = not Info
                        pygame.time.wait(100)
        if(isConsolaOn):
            screen.blit(consolaOn, (0,0))
            if(Intro):
                text = pygame.font.Font("Pokemon Solid.ttf", 45).render("PokeDex",False,(0,0,0))
                screen.blit(text,(screen.get_rect().width/2-text.get_rect().width/2,120))
                Wait = 1500
                Intro = False
            elif(Info):
                Info_ = info.split("\n")
                y = 75
                for line in Info_:
                    screen.blit(Font.render(line,False,(0,0,0)),(70,y))
                    y+=17
            else:
                for pokemon in sprite_pokemons:
                    if(pokemon.posicion == posicion):
                        pokemon.draw(screen,125,100,100,100)
                        info = pokemon.get_info()
                        if(Rowr and pokemon.descubierto):
                            pokemon.play_sound()
                            Rowr = False
                        else:
                            Rowr = False
            
        else:
            screen.blit(consolaOff, (0,0))
        #Dibujo de los botones
        for sprite in sprite_botones:
            sprite.draw(screen,Mouse)
        
        #Valor de actualizacion
        pygame.display.update()
        Mouse.update()
        pygame.time.wait(Wait)
        Wait = 0
        clock.tick(60)
       
    pygame.quit()

# Ejecucion de la Ventana
if __name__ == '__main__':
    GameWindow()