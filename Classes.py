import pygame

#Clase Pokemon
class Pokemon(pygame.sprite.Sprite):
    def __init__(self, numero, nombre,tipo1,tipo2,habilidad,habilidad_O):
        pygame.sprite.Sprite.__init__(self)
        # Caracteristicas Generales
        self.numero = numero
        self.nombre = nombre
        self.tipo_primario = tipo1
        self.tipo_secundario = tipo2
        self.habilidad = habilidad.split("_")
        self.habilidad_oculta = habilidad_O.split("_")
        self.descubierto = False

        # Elementos practicos
        self.imagen = "sprites_pokemon/"+self.nombre+".png"
        self.sonido = "sonidos_pokemon/"+self.numero+".wav"
        self.img_tipoP = "sprites_tipos/"+self.tipo_primario
        self.img_desconocido = "sprites/Desconocido.png"
        self.img_tipoS = None
        if(self.tipo_secundario!=" "):
            self.img_tipoS = "sprites_tipos/"+self.tipo_secundario
        self.posicion = int(self.numero)

        #Elementos graficos
        self.image = pygame.image.load(self.imagen)
        self.img_tipoP = pygame.image.load(self.img_tipoP)
        if(self.img_tipoS!=None):
            self.img_tipoS = pygame.image.load(self.img_tipoS)
        self.img_desconocido = pygame.image.load(self.img_desconocido)
        self.img_desconocido = pygame.transform.scale(self.img_desconocido, (100, 100))
        self.font =  pygame.font.Font("Pokemon Solid.ttf", 24)
        #Elementos sonoros
        self.sonido = pygame.mixer.Sound(self.sonido)

        #Recta
        self.rect = self.image.get_rect()
        
    def draw(self,screen,posx,posy,weight,height):
        self.rect.x = posx
        self.rect.y = posy
        self.image = pygame.transform.scale(self.image, (weight, height))
        text = self.font.render(self.nombre,True,(0,0,0))
        text_pos = (screen.get_rect().width/2-text.get_rect().width/2,posy-25)
        image_pos = (screen.get_rect().width/2-self.image.get_rect().width/2,posy)
        if(self.descubierto):
            screen.blit(text, text_pos)
            screen.blit(self.image,image_pos)
            screen.blit(self.img_tipoP,(posx-50,posy+40))
            if(self.img_tipoS!=None):
                screen.blit(self.img_tipoS,(posx-50,posy+60))
        else:
            screen.blit(self.img_desconocido,image_pos)
        screen.blit(pygame.font.SysFont(None, 25).render(self.numero,False,(0,0,0)),(255,200))

    def play_sound(self):
        pygame.mixer.Sound.play(self.sonido)

    def get_info(self):
        info = ""
        
        if(self.descubierto):
            info += "Numero: " + self.numero + "\n"
            info += "Nombre: " + self.nombre + "\n"
            info += "Tipo Primario: " + self.tipo_primario + "\n"
            if(self.tipo_secundario != " "):
                info += "Tipo Secundario: " + self.tipo_secundario + "\n"
            info += "Habilidad: " + "\n"
            for habilidades in self.habilidad:
                info += "       " + habilidades + "\n"
            info += "Habilidad Oculta: " + "\n"
            for habilidades in self.habilidad_oculta:
                info += "       " + habilidades + "\n"

        else:
            info = "El pokemon es desconocido. \n"
        info = info.replace(".png","")
        info = info.replace("_"," ")
        return info
#Clase Boton
class Boton(pygame.sprite.Sprite):
    def __init__(self,accion,imagenA,imagenB,posx,posy,weight,height):
        pygame.sprite.Sprite.__init__(self)
        self.imageA = pygame.image.load(imagenA)
        self.imageB = pygame.image.load(imagenB)
        self.accion = accion
        if(weight>0 and height>0):
            self.imageA = pygame.transform.scale(self.imageA, (weight, height))
            self.imageB = pygame.transform.scale(self.imageB, (weight, height))
        self.rect = self.imageA.get_rect()
        self.rect.x = posx
        self.rect.y = posy
        self.sonido = pygame.mixer.Sound("sonidos_ambientales/Button.mp3")
        self.play = True

    def draw(self,screen,Mouse):
        if(Mouse.colliderect(self.rect)):
            screen.blit(self.imageB,(self.rect.x,self.rect.y))
            if(self.play):
                self.sonido.play()
                self.play = False
        else:   
            screen.blit(self.imageA,(self.rect.x,self.rect.y))
            self.play = True
#Clase Cursor el tipo Rect para utilizar el mouse
class Cursor(pygame.Rect):
    # Funcion constructura de la clase
    def __init__(self):
        pygame.Rect.__init__(self,0,0,1,1)
        self.left,self.top = pygame.mouse.get_pos()
    # Actualiza la posicion del mouse
    def update(self):
        self.left,self.top = pygame.mouse.get_pos()

#Clase Menu o Ajustes
class Menu(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((200,150),pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.tipos = []
        self.pos = 0
        self.numero = ""

        self.menuI = ""
        self.cTipo = ""
        self.aPokemon = ""
        self.show = ""
        self.part = "MenuI"

        self.font = pygame.font.SysFont('arial', 15,True)

    def do_menu(self,list_pokemons):
        self.aPokemon = ""
        if(self.menuI == ""):
            self.menuI += "Agregar Pokemon" + "\n"
            self.menuI += "Consultar Tipo" + "\n"
            self.menuI = self.menuI.split("\n")
        if(self.cTipo == ""):
            self.tipos.append("Todos.")
            for pokemon in list_pokemons:
                tipo = pokemon.tipo_primario
                tipo = tipo.replace("_"," ")
                tipo = tipo.replace(".png",".")
                self.tipos.append(tipo)

                tipo = pokemon.tipo_secundario
                tipo = tipo.replace("_"," ")
                tipo = tipo.replace(".png",".")
                self.tipos.append(tipo)

            for tipo in self.tipos:
                if(self.cTipo.find(tipo) == -1):
                    self.cTipo += tipo + "\n"

            self.cTipo = self.cTipo.split("\n")
            self.tipos.clear()
        
        #Cargar los pokemons que se puden agregar
        for pokemon in list_pokemons:
            if(not pokemon.descubierto):
                self.aPokemon += pokemon.numero +" "+ pokemon.nombre + "\n"
        
        self.aPokemon = self.aPokemon.split("\n")

    def do_action(self):
        pass
    
    def update(self, list_pokemons):
        self.image.fill(pygame.SRCALPHA)
        if(self.part == "MenuI"):
            self.show = self.menuI
        if(self.part == "cTipo"):
            self.show= self.cTipo
        if(self.part == "aPokemon"):
            self.show = self.aPokemon
        y = self.rect.height/5
        posy = y/2

        for line in range(self.pos,self.pos+9):
            if(line<len(self.show)):
                if(line==self.pos):
                    self.image.blit(self.font.render(self.show[line],False,(0,0,0),(156,156,156)),(0, posy/2))
                else:
                    self.image.blit(self.font.render(self.show[line],False,(0,0,0)),(0, posy/2))
                posy+=y
        self.do_menu(list_pokemons)

    def draw(self,screen):
        screen.blit(self.image,(self.rect.x,self.rect.y))