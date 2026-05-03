"""
╔══════════════════════════════════════════════════════════════════╗
║           GEOMETRIC PRO: TORA EDITION  v2.0 ULTRA              ║
║                                                                  ║
║  REQUISITOS:  pip install pygame                                 ║
║  EJECUTAR:    python geometric_pro_tora_v2.py                   ║
╚══════════════════════════════════════════════════════════════════╝
"""

import pygame
import random
import sys
import os
import json
import math
import time
import webbrowser

# ─────────────────────────────────────────────────────────────────
#  INIT
# ─────────────────────────────────────────────────────────────────
pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

ANCHO, ALTO = 700, 900
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("GEOMETRIC PRO: TORA EDITION v2.0")
reloj = pygame.time.Clock()
FPS = 60

# ─────────────────────────────────────────────────────────────────
#  COLORES
# ─────────────────────────────────────────────────────────────────
NEGRO      = (0,   0,   0)
BLANCO     = (255, 255, 255)
GRIS       = (150, 150, 150)
GRIS_OSC   = (40,  40,  40)
ROJO       = (255, 50,  50)
VERDE      = (0,   255, 100)
AMARILLO   = (255, 215, 0)
CIAN       = (0,   255, 200)
MAGENTA    = (255, 0,   255)
NARANJA    = (255, 140, 0)
PURPURA    = (148, 0,   211)
ROSA       = (255, 105, 180)
AZUL_NEÓN  = (0,   100, 255)
TURQUESA   = (64,  224, 208)
LIMA       = (50,  205, 50)
CORAL      = (255, 127, 80)
DORADO     = (255, 215, 0)
PLATINO    = (229, 228, 226)
ESMERALDA  = (0,   201, 87)
ZAFIRO     = (15,  82,  186)
RUBÍ       = (155, 17,  30)
WHATSAPP   = (37,  211, 102)

# ─────────────────────────────────────────────────────────────────
#  PALABROTAS PROHIBIDAS (filtro básico)
# ─────────────────────────────────────────────────────────────────
PALABROTAS = {
    "puta","puto","mierda","coño","cojon","cojones","culo","polla",
    "joder","hostia","pijo","hijoputa","cabrón","cabron","marica",
    "pendejo","chinga","verga","pinche","culero","carajo","concha",
    "fuck","shit","ass","bitch","cunt","dick","cock","nigga","damn"
}

def nombre_valido(nombre):
    if not nombre or len(nombre.strip()) < 2 or len(nombre.strip()) > 16:
        return False
    for p in PALABROTAS:
        if p in nombre.lower():
            return False
    return True

# ─────────────────────────────────────────────────────────────────
#  BASE DE DATOS / GUARDADO
# ─────────────────────────────────────────────────────────────────
ARCHIVO_GUARDADO = "tora_save_v2.json"

DATOS_DEFAULT = {
    "nombre_jugador": "",
    "pin_amigo": "",
    "record": 0,
    "bits": 500,          # bits de inicio para que puedan comprar algo
    "partidas_jugadas": 0,
    "tiempo_jugado": 0,   # en segundos
    "skin_actual": 0,
    "mundo_actual": 0,
    "arma_actual": 0,
    "skins_desbloqueadas": [True] + [False]*11,
    "mundos_desbloqueados": [True] + [False]*7,
    "armas_desbloqueadas": [True] + [False]*4,
    "controles": "FLECHAS",
    "volumen": 0.7,
    "imagen_skin_path": "",   # ruta a imagen custom
    "club_nombre": "",
    "club_miembros": [],
    "amigos": [],             # lista de pines de amigos (simulado local)
    "tutorial_visto": False,
    "ultimo_login": 0,
}

def cargar_datos():
    d = dict(DATOS_DEFAULT)
    if os.path.exists(ARCHIVO_GUARDADO):
        try:
            with open(ARCHIVO_GUARDADO, "r", encoding="utf-8") as f:
                cargado = json.load(f)
                d.update(cargado)
        except Exception:
            pass
    # Generar pin si no tiene
    if not d.get("pin_amigo"):
        import random as _r
        d["pin_amigo"] = "".join([str(_r.randint(0,9)) for _ in range(6)])
    return d

def guardar_datos(db):
    try:
        with open(ARCHIVO_GUARDADO, "w", encoding="utf-8") as f:
            json.dump(db, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error al guardar: {e}")

db = cargar_datos()

# ─────────────────────────────────────────────────────────────────
#  MUNDOS  (8 mundos)
# ─────────────────────────────────────────────────────────────────
MUNDOS = [
    {
        "nombre": "TIERRA",       "precio": 0,
        "bg": (10, 20, 40),       "vel_base": 5,   "frecuencia": 28,
        "estrella": (200,255,255),"color_enemigo": (220,50,50),
        "descripcion": "El punto de partida. Velocidad media, para aprender."
    },
    {
        "nombre": "LUNA",         "precio": 800,
        "bg": (20, 20, 28),       "vel_base": 3.5, "frecuencia": 14,
        "estrella": (255,255,255),"color_enemigo": (180,180,255),
        "descripcion": "Gravedad baja. Muchos enemigos pero lentos."
    },
    {
        "nombre": "MARTE",        "precio": 1500,
        "bg": (45, 10, 5),        "vel_base": 7,   "frecuencia": 32,
        "estrella": (255,150,100),"color_enemigo": (255,100,0),
        "descripcion": "¡Enemigos rápidos! Reflejos de acero."
    },
    {
        "nombre": "EL VACÍO",     "precio": 2500,
        "bg": (5, 0, 12),         "vel_base": 6,   "frecuencia": 22,
        "estrella": (150,0,255),  "color_enemigo": (180,0,255),
        "descripcion": "Oscuridad total. Enemigos invisibles a ratos."
    },
    {
        "nombre": "JÚPITER",      "precio": 4000,
        "bg": (40, 25, 5),        "vel_base": 8,   "frecuencia": 26,
        "estrella": (255,200,100),"color_enemigo": (255,165,0),
        "descripcion": "Tormenta constante. Todo va más rápido."
    },
    {
        "nombre": "SATURNO",      "precio": 6000,
        "bg": (30, 25, 10),       "vel_base": 5.5, "frecuencia": 18,
        "estrella": (200,200,100),"color_enemigo": (200,200,50),
        "descripcion": "Anillos de obstáculos. Patrón especial."
    },
    {
        "nombre": "NEBULOSA",     "precio": 9000,
        "bg": (5, 0, 25),         "vel_base": 9,   "frecuencia": 30,
        "estrella": (100,200,255),"color_enemigo": (0,200,255),
        "descripcion": "La pesadilla. Máxima velocidad posible."
    },
    {
        "nombre": "APOCALIPSIS",  "precio": 15000,
        "bg": (20, 0, 0),         "vel_base": 10,  "frecuencia": 20,
        "estrella": (255,50,0),   "color_enemigo": (255,0,0),
        "descripcion": "Solo para los mejores. Sin piedad."
    },
]

# ─────────────────────────────────────────────────────────────────
#  SKINS  (12 skins)
# ─────────────────────────────────────────────────────────────────
SKINS = [
    {"nombre": "CLÁSICO",       "color": CIAN,      "precio": 0,
     "forma": "cuadrado",       "brillo": False,    "descripcion": "El original."},
    {"nombre": "FUEGO AZUL",    "color": AZUL_NEÓN, "precio": 2000,
     "forma": "cuadrado",       "brillo": True,     "descripcion": "Llamas frías."},
    {"nombre": "ORO SÓLIDO",    "color": DORADO,    "precio": 4000,
     "forma": "cuadrado",       "brillo": True,     "descripcion": "Brilla en la oscuridad."},
    {"nombre": "CAOS NEÓN",     "color": MAGENTA,   "precio": 7000,
     "forma": "diamante",       "brillo": True,     "descripcion": "Caos puro."},
    {"nombre": "ESMERALDA",     "color": ESMERALDA, "precio": 10000,
     "forma": "diamante",       "brillo": True,     "descripcion": "Gema de élite."},
    {"nombre": "RUBÍ OSCURO",   "color": RUBÍ,      "precio": 12000,
     "forma": "cuadrado",       "brillo": True,     "descripcion": "Frío como la sangre."},
    {"nombre": "PLATINO",       "color": PLATINO,   "precio": 15000,
     "forma": "cuadrado",       "brillo": True,     "descripcion": "Exclusivo."},
    {"nombre": "ZAFIRO",        "color": ZAFIRO,    "precio": 18000,
     "forma": "diamante",       "brillo": True,     "descripcion": "Profundo como el mar."},
    {"nombre": "ARCOÍRIS",      "color": ROSA,      "precio": 22000,
     "forma": "cuadrado",       "brillo": True,     "descripcion": "¡Cambia de color!"},
    {"nombre": "SOMBRA",        "color": (80,80,80),"precio": 28000,
     "forma": "cuadrado",       "brillo": False,    "descripcion": "Casi invisible."},
    {"nombre": "NEÓN CAÓTICO",  "color": LIMA,      "precio": 35000,
     "forma": "diamante",       "brillo": True,     "descripcion": "Estela épica."},
    {"nombre": "PERSONALIZADA", "color": BLANCO,    "precio": 50000,
     "forma": "imagen",         "brillo": False,    "descripcion": "¡Tu propia imagen!"},
]

# ─────────────────────────────────────────────────────────────────
#  ARMAS  (5 tipos)
# ─────────────────────────────────────────────────────────────────
ARMAS = [
    {"nombre": "SIN ARMA",   "precio": 0,     "desc": "Solo esquiva.",
     "color": GRIS,          "tipo": "ninguna","velocidad_bala": 0,  "daño": 0},
    {"nombre": "PISTOLA",    "precio": 3000,  "desc": "3 balas por disparo.",
     "color": AMARILLO,      "tipo": "pistola","velocidad_bala": 12, "daño": 1},
    {"nombre": "LÁSER",      "precio": 7000,  "desc": "Rayo instantáneo.",
     "color": ROJO,          "tipo": "laser",  "velocidad_bala": 30, "daño": 2},
    {"nombre": "DISPERSIÓN", "precio": 12000, "desc": "5 balas en abanico.",
     "color": NARANJA,       "tipo": "spread", "velocidad_bala": 10, "daño": 1},
    {"nombre": "PLASMA",     "precio": 20000, "desc": "Destruye todo en su línea.",
     "color": PURPURA,       "tipo": "plasma", "velocidad_bala": 18, "daño": 3},
]

# ─────────────────────────────────────────────────────────────────
#  GENERACIÓN DE MÚSICA PROCEDURAL (sin archivos externos)
# ─────────────────────────────────────────────────────────────────
import numpy as np

def generar_tono(freq, duracion_ms, volumen=0.3, forma="sine"):
    """Genera un tono como array numpy."""
    tasa = 44100
    n = int(tasa * duracion_ms / 1000)
    t = np.linspace(0, duracion_ms/1000, n, endpoint=False)
    if forma == "sine":
        onda = np.sin(2 * np.pi * freq * t)
    elif forma == "square":
        onda = np.sign(np.sin(2 * np.pi * freq * t))
    elif forma == "saw":
        onda = 2 * (t * freq - np.floor(t * freq + 0.5))
    else:
        onda = np.sin(2 * np.pi * freq * t)
    # Envelope suave
    fade = min(200, n//4)
    onda[:fade] *= np.linspace(0, 1, fade)
    onda[-fade:] *= np.linspace(1, 0, fade)
    onda = (onda * volumen * 32767).astype(np.int16)
    stereo = np.column_stack([onda, onda])
    return stereo

def crear_sonido_pygame(freq, duracion_ms, volumen=0.25, forma="sine"):
    """Convierte array numpy a pygame.Sound."""
    try:
        arr = generar_tono(freq, duracion_ms, volumen, forma)
        sonido = pygame.sndarray.make_sound(arr)
        return sonido
    except Exception:
        return None

# Crear efectos de sonido
print("Generando sonidos...")
try:
    SND_DISPARO  = crear_sonido_pygame(880,  80,  0.15, "square")
    SND_MUERTE   = crear_sonido_pygame(200,  400, 0.3,  "saw")
    SND_COMPRA   = crear_sonido_pygame(523,  150, 0.2,  "sine")
    SND_DASH     = crear_sonido_pygame(1200, 60,  0.1,  "square")
    SND_NIVEL    = crear_sonido_pygame(660,  300, 0.2,  "sine")
    SND_BALA_HIT = crear_sonido_pygame(440,  100, 0.2,  "saw")
    SND_ERROR    = crear_sonido_pygame(150,  200, 0.2,  "square")
    SONIDOS_OK   = True
    print("¡Sonidos generados correctamente!")
except Exception as e:
    print(f"Sin sonido: {e}")
    SONIDOS_OK = False
    SND_DISPARO = SND_MUERTE = SND_COMPRA = SND_DASH = SND_NIVEL = SND_BALA_HIT = SND_ERROR = None

def play_snd(snd):
    if snd and SONIDOS_OK:
        try:
            snd.set_volume(db.get("volumen", 0.7))
            snd.play()
        except Exception:
            pass

# ─────────────────────────────────────────────────────────────────
#  MÚSICA DE FONDO  (tono drone ambiental generado)
# ─────────────────────────────────────────────────────────────────
def generar_musica_fondo():
    """Genera un loop de música chiptune ambiental."""
    try:
        tasa = 44100
        dur  = 4.0  # segundos
        n    = int(tasa * dur)
        t    = np.linspace(0, dur, n, endpoint=False)

        notas = [130.81, 164.81, 196.00, 220.00, 261.63, 329.63, 392.00, 440.00]
        pesos = [1.0, 0.7, 0.5, 0.3]

        onda = np.zeros(n)
        for i, (nota, peso) in enumerate(zip(notas[:4], pesos)):
            onda += np.sin(2*np.pi*nota*t) * peso * 0.08
            onda += np.sign(np.sin(2*np.pi*nota*2*t)) * peso * 0.03

        onda = np.clip(onda, -1, 1)
        onda_int = (onda * 32767 * 0.4).astype(np.int16)
        stereo = np.column_stack([onda_int, onda_int])

        snd = pygame.sndarray.make_sound(stereo)
        snd.set_volume(0.15)
        return snd
    except Exception as e:
        print(f"Sin música: {e}")
        return None

MUSICA_FONDO = generar_musica_fondo()
canal_musica = None

def iniciar_musica():
    global canal_musica
    if MUSICA_FONDO:
        try:
            canal_musica = MUSICA_FONDO.play(-1)  # loop infinito
            if canal_musica:
                canal_musica.set_volume(db.get("volumen", 0.7) * 0.3)
        except Exception:
            pass

def actualizar_vol_musica():
    if canal_musica:
        try:
            canal_musica.set_volume(db.get("volumen", 0.7) * 0.3)
        except Exception:
            pass

iniciar_musica()

# ─────────────────────────────────────────────────────────────────
#  FUENTES
# ─────────────────────────────────────────────────────────────────
F_TINY  = pygame.font.Font(None, 22)
F_SMALL = pygame.font.Font(None, 30)
F_MED   = pygame.font.Font(None, 46)
F_BIG   = pygame.font.Font(None, 80)
F_HUGE  = pygame.font.Font(None, 110)

# ─────────────────────────────────────────────────────────────────
#  UTILIDADES DE DIBUJADO
# ─────────────────────────────────────────────────────────────────
def txt(surface, texto, fuente, color, cx, cy, centrado=True, sombra=False):
    if sombra:
        img_s = fuente.render(texto, True, (0,0,0))
        r_s = img_s.get_rect(center=(cx+2, cy+2)) if centrado else img_s.get_rect(topleft=(cx+2, cy+2))
        surface.blit(img_s, r_s)
    img = fuente.render(texto, True, color)
    r = img.get_rect(center=(cx, cy)) if centrado else img.get_rect(topleft=(cx, cy))
    surface.blit(img, r)
    return r

def boton(surface, texto, fuente, rect, color_fondo, color_texto, radio=12, borde=None):
    """Dibuja botón redondeado y retorna True si el mouse está encima."""
    mx, my = pygame.mouse.get_pos()
    hover  = rect.collidepoint(mx, my)
    c_fondo = tuple(min(255, c+30) for c in color_fondo) if hover else color_fondo
    pygame.draw.rect(surface, c_fondo, rect, border_radius=radio)
    if borde:
        pygame.draw.rect(surface, borde, rect, 2, border_radius=radio)
    txt(surface, texto, fuente, color_texto, rect.centerx, rect.centery)
    return hover

def boton_click(surface, texto, fuente, rect, color_fondo, color_texto, radio=12, borde=None):
    """Igual que boton() pero retorna True si se hace clic."""
    hover = boton(surface, texto, fuente, rect, color_fondo, color_texto, radio, borde)
    if hover:
        for e in pygame.event.get(pygame.MOUSEBUTTONDOWN):
            if e.button == 1:
                return True
    return False

def panel(surface, rect, color=(20,20,35), alpha=220, radio=16, borde=None):
    """Panel semitransparente."""
    s = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
    pygame.draw.rect(s, (*color, alpha), (0, 0, rect.w, rect.h), border_radius=radio)
    if borde:
        pygame.draw.rect(s, (*borde, 255), (0, 0, rect.w, rect.h), 2, border_radius=radio)
    surface.blit(s, rect.topleft)

def dibujar_barra(surface, x, y, ancho, alto, valor, maximo, color_lleno, color_vacio=(40,40,40)):
    pygame.draw.rect(surface, color_vacio, (x, y, ancho, alto), border_radius=4)
    if maximo > 0:
        w = int(ancho * min(valor, maximo) / maximo)
        if w > 0:
            pygame.draw.rect(surface, color_lleno, (x, y, w, alto), border_radius=4)

# ─────────────────────────────────────────────────────────────────
#  EFECTOS VISUALES
# ─────────────────────────────────────────────────────────────────
class Estrella:
    def __init__(self, color=(255,255,255)):
        self.reset(color)
        self.y = random.randint(0, ALTO)  # posición inicial aleatoria

    def reset(self, color):
        self.x    = random.randint(0, ANCHO)
        self.y    = random.randint(-50, -5)
        self.vel  = random.uniform(1.5, 5)
        self.tam  = random.uniform(1, 3)
        self.color = color

    def update(self, surface, color_mundo):
        self.color = color_mundo
        self.y += self.vel
        if self.y > ALTO + 10:
            self.reset(color_mundo)
        alpha = int(180 + self.vel * 15)
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), max(1, int(self.tam)))

class Particula:
    def __init__(self, x, y, color, velocidad=8, vida_max=255):
        self.x, self.y = float(x), float(y)
        ang = random.uniform(0, math.tau)
        vel = random.uniform(2, velocidad)
        self.vx = math.cos(ang) * vel
        self.vy = math.sin(ang) * vel
        self.vida = vida_max
        self.vida_max = vida_max
        self.color = color
        self.tam = random.randint(3, 7)

    def update(self, surface):
        self.x  += self.vx
        self.y  += self.vy
        self.vx *= 0.94
        self.vy *= 0.94
        self.vida -= 8
        if self.vida <= 0:
            return False
        a = max(0, self.vida)
        c = (*self.color[:3], a)
        s = pygame.Surface((self.tam*2, self.tam*2), pygame.SRCALPHA)
        pygame.draw.circle(s, c, (self.tam, self.tam), self.tam)
        surface.blit(s, (int(self.x)-self.tam, int(self.y)-self.tam))
        return True

class NumeroFlotante:
    """Texto que sube y desaparece (p.ej. +10 bits)."""
    def __init__(self, x, y, texto, color=AMARILLO):
        self.x, self.y = float(x), float(y)
        self.texto = texto
        self.color = color
        self.vida  = 255
        self.vel_y = -1.5

    def update(self, surface):
        self.y    += self.vel_y
        self.vida -= 5
        if self.vida <= 0:
            return False
        a = max(0, self.vida)
        img = F_SMALL.render(self.texto, True, self.color)
        img.set_alpha(a)
        surface.blit(img, (int(self.x), int(self.y)))
        return True

class Bala:
    def __init__(self, x, y, vy, color, tipo="pistola", vx=0):
        self.x, self.y = float(x), float(y)
        self.vx = float(vx)
        self.vy = float(vy)
        self.color = color
        self.tipo  = tipo
        self.activa = True
        self.tam = 6 if tipo != "plasma" else 10

    def update(self, surface):
        self.x += self.vx
        self.y += self.vy
        if self.y < -20 or self.x < -20 or self.x > ANCHO+20:
            self.activa = False
            return
        if self.tipo == "laser":
            pygame.draw.rect(surface, self.color, (int(self.x)-2, int(self.y)-15, 4, 30))
        elif self.tipo == "plasma":
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.tam)
            glow = pygame.Surface((self.tam*4, self.tam*4), pygame.SRCALPHA)
            pygame.draw.circle(glow, (*self.color, 60), (self.tam*2, self.tam*2), self.tam*2)
            surface.blit(glow, (int(self.x)-self.tam*2, int(self.y)-self.tam*2))
        else:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.tam)

class Enemigo:
    def __init__(self, mundo, nivel):
        self.w = random.randint(38, 75)
        if mundo["nombre"] == "LUNA":
            self.w = random.randint(55, 95)
        elif mundo["nombre"] == "APOCALIPSIS":
            self.w = random.randint(30, 55)
        self.x = float(random.randint(10, ANCHO - self.w - 10))
        self.y = float(-self.w - 10)
        self.vel_x = 0
        if mundo["nombre"] in ["SATURNO", "APOCALIPSIS"]:
            self.vel_x = random.choice([-1, 1]) * random.uniform(1, 2.5)
        self.rect = pygame.Rect(int(self.x), int(self.y), self.w, self.w)
        self.color = mundo["color_enemigo"]
        self.vida_max = 1 + nivel // 5
        self.vida = self.vida_max
        self.angulo = 0
        self.tipo = random.choice(["normal","rapido","grande"]) if nivel > 3 else "normal"
        if self.tipo == "grande":
            self.w = min(110, self.w + 30)
            self.vida_max = 3
            self.vida = 3
        elif self.tipo == "rapido":
            pass  # velocidad extra se añade en update

    def update(self, vel_base, nivel):
        vel_extra = vel_base + nivel * 0.4
        if self.tipo == "rapido":
            vel_extra *= 1.4
        self.y   += vel_extra
        self.x   += self.vel_x
        if self.x < 5:
            self.x, self.vel_x = 5, abs(self.vel_x)
        if self.x + self.w > ANCHO - 5:
            self.x, self.vel_x = ANCHO - self.w - 5, -abs(self.vel_x)
        self.angulo = (self.angulo + 2) % 360
        self.rect.update(int(self.x), int(self.y), self.w, self.w)

    def draw(self, surface, invisible=False):
        if invisible and random.random() < 0.4:
            return  # efecto "El Vacío"
        cx, cy = self.rect.centerx, self.rect.centery
        # Color según vida
        if self.vida == 1:
            color = self.color
        else:
            t = self.vida / self.vida_max
            color = (int(self.color[0]*t + 255*(1-t)),
                     int(self.color[1]*t),
                     int(self.color[2]*t))
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        pygame.draw.rect(surface, (0,0,0), self.rect.inflate(-10,-10), border_radius=4)
        # Vida si >1
        if self.vida_max > 1:
            for i in range(self.vida):
                pygame.draw.circle(surface, VERDE, (cx - (self.vida_max-1)*6 + i*12, self.rect.top-8), 4)

# ─────────────────────────────────────────────────────────────────
#  CLASE PRINCIPAL DEL JUEGO
# ─────────────────────────────────────────────────────────────────
class JuegoTora:
    def __init__(self):
        self.estado          = "NOMBRE" if not db["nombre_jugador"] else ("TUTORIAL" if not db["tutorial_visto"] else "MENU")
        self.estado_anterior = "MENU"
        self.estrellas       = [Estrella() for _ in range(70)]
        self.particulas: list[Particula]       = []
        self.numeros_flotantes: list[NumeroFlotante] = []
        self.ticker          = 0  # frame counter
        self.input_nombre    = ""
        self.input_error     = ""
        self.scroll_skin     = 0   # índice de skin seleccionada para scroll
        self.scroll_mundo    = 0
        self.scroll_arma     = 0
        self.tutorial_paso   = 0
        self.arcoiris_t      = 0  # timer para skin arcoíris
        # Dialogo
        self.dialogo_msg     = ""
        self.dialogo_timer   = 0
        # Club
        self.input_club      = ""
        self.input_amigo_pin = ""
        self.input_amigo_err = ""
        # Score pantalla final
        self.score_final     = 0
        self.puntuacion_100  = 0
        self.puntuacion_motivo = ""
        # Estado juego
        self.reset_partida()

    # ── Dialogo flotante ──────────────────────────────────────────
    def mostrar_dialogo(self, msg, ticks=180):
        self.dialogo_msg   = msg
        self.dialogo_timer = ticks

    # ── Reset de partida ─────────────────────────────────────────
    def reset_partida(self):
        self.jugador      = pygame.Rect(ANCHO//2-25, ALTO-150, 50, 50)
        self.enemigos: list[Enemigo] = []
        self.balas: list[Bala]       = []
        self.particulas              = []
        self.numeros_flotantes       = []
        self.estela                  = []
        self.score          = 0
        self.nivel          = 1
        self.dash_cooldown  = 0
        self.dash_carga_max = 90    # frames para recargar dash
        self.dash_cargado   = True
        self.balas_restantes = 15   # comienza con 15 balas
        self.balas_timer    = 0     # cuenta frames para dar balas cada 5000 pts
        self.pts_ultima_bala= 0
        self.frame_inicio   = self.ticker
        self.cuenta_atras   = 4     # 3,2,1 ¡YA!
        self.cuenta_timer   = 0
        self.en_cuenta_atras= True
        self.angulo_jugador = 0
        self.godmode_timer  = 0     # invulnerabilidad tras crear cuenta
        self.bits_acumulados= 0     # bits ganados en esta partida

    # ── Color activo de la skin ──────────────────────────────────
    def color_skin(self):
        s = SKINS[db["skin_actual"]]
        if s["nombre"] == "ARCOÍRIS":
            self.arcoiris_t = (self.arcoiris_t + 2) % 360
            r = int(128 + 127 * math.sin(math.radians(self.arcoiris_t)))
            g = int(128 + 127 * math.sin(math.radians(self.arcoiris_t + 120)))
            b = int(128 + 127 * math.sin(math.radians(self.arcoiris_t + 240)))
            return (r, g, b)
        if s["nombre"] == "NEÓN CAÓTICO":
            self.arcoiris_t = (self.arcoiris_t + 4) % 360
            r = int(128 + 127 * math.sin(math.radians(self.arcoiris_t)))
            return (r, 205, 50)
        return s["color"]

    # ── Dibujar jugador ──────────────────────────────────────────
    def draw_jugador(self, surface, color):
        s = SKINS[db["skin_actual"]]
        cx, cy = self.jugador.centerx, self.jugador.centery
        r  = 25
        # Brillo
        if s["brillo"]:
            glow = pygame.Surface((r*6, r*6), pygame.SRCALPHA)
            pygame.draw.circle(glow, (*color, 50), (r*3, r*3), r*3)
            surface.blit(glow, (cx - r*3, cy - r*3))
        # Forma
        if s["forma"] == "diamante":
            pts = [(cx, cy-r), (cx+r, cy), (cx, cy+r), (cx-r, cy)]
            pygame.draw.polygon(surface, color, pts)
            pygame.draw.polygon(surface, BLANCO, pts, 2)
        else:
            pygame.draw.rect(surface, color, self.jugador, border_radius=12)
            pygame.draw.rect(surface, BLANCO, self.jugador, 2, border_radius=12)

    # ── Disparar ─────────────────────────────────────────────────
    def disparar(self):
        arma = ARMAS[db["arma_actual"]]
        if arma["tipo"] == "ninguna":
            self.mostrar_dialogo("¡Compra un arma en la tienda!")
            play_snd(SND_ERROR)
            return
        if self.balas_restantes <= 0:
            self.mostrar_dialogo("¡Sin balas! Cada 5000 pts ganas 5.")
            play_snd(SND_ERROR)
            return
        self.balas_restantes -= 1
        play_snd(SND_DISPARO)
        cx = self.jugador.centerx
        cy = self.jugador.top
        c  = arma["color"]
        v  = arma["velocidad_bala"]
        t  = arma["tipo"]
        if t == "pistola":
            self.balas.append(Bala(cx, cy, -v, c, t))
        elif t == "laser":
            self.balas.append(Bala(cx, cy, -v, c, "laser"))
        elif t == "spread":
            for angulo in [-20, -10, 0, 10, 20]:
                rad = math.radians(angulo)
                self.balas.append(Bala(cx, cy, -v*math.cos(rad), c, "pistola", v*math.sin(rad)))
        elif t == "plasma":
            self.balas.append(Bala(cx, cy, -v, c, "plasma"))

    # ── Calcular puntuación /100 ──────────────────────────────────
    def calcular_puntuacion(self):
        s = self.score_final
        if   s >= 8000: pts, motivo = 100, "¡LEYENDA ABSOLUTA! 🏆"
        elif s >= 6000: pts, motivo = 95,  "¡Maestro del espacio! 🌌"
        elif s >= 4000: pts, motivo = 88,  "¡Increíble esquivador! ⚡"
        elif s >= 2500: pts, motivo = 80,  "¡Muy buen desempeño! 🎯"
        elif s >= 1500: pts, motivo = 70,  "¡Buen jugador! 💪"
        elif s >= 800:  pts, motivo = 58,  "Promedio, ¡puedes más!"
        elif s >= 400:  pts, motivo = 44,  "Aún en entrenamiento."
        elif s >= 150:  pts, motivo = 30,  "¡Sigue intentándolo!"
        else:            pts, motivo = 15,  "Principiante, ¡tú puedes!"
        return pts, motivo

    # ── Calcular bits ganados ────────────────────────────────────
    def bits_por_score(self, score):
        """Bits más escasos: ~1 bit por cada 12 puntos, con bonus."""
        base  = score // 12
        bonus = 0
        if score >= 5000: bonus += 200
        if score >= 2000: bonus += 80
        if score >= 1000: bonus += 30
        return base + bonus

    # ── Panel de fondo ───────────────────────────────────────────
    def draw_bg(self, mundo):
        pantalla.fill(mundo["bg"])
        for e in self.estrellas:
            e.update(pantalla, mundo["estrella"])

    # ─────────────────────────────────────────────────────────────
    #  BUCLE PRINCIPAL
    # ─────────────────────────────────────────────────────────────
    def ejecutar(self):
        while True:
            self.ticker += 1
            mundo_idx   = db["mundo_actual"]
            skin_idx    = db["skin_actual"]
            mundo       = MUNDOS[mundo_idx]
            skin        = SKINS[skin_idx]
            color_jug   = self.color_skin()

            # --- Fondo ---
            self.draw_bg(mundo)

            # --- Eventos globales ---
            eventos = pygame.event.get()
            for e in eventos:
                if e.type == pygame.QUIT:
                    guardar_datos(db)
                    pygame.quit(); sys.exit()

                if e.type == pygame.MOUSEWHEEL:
                    self._mousewheel(e.y)

                if e.type == pygame.KEYDOWN:
                    self._keydown(e)

                if e.type == pygame.MOUSEBUTTONDOWN:
                    if e.button == 1:
                        self._click(e.pos)

            # --- Renderizar estado ---
            dispatch = {
                "NOMBRE":        self.render_nombre,
                "TUTORIAL":      self.render_tutorial,
                "MENU":          self.render_menu,
                "JUGANDO":       self.render_jugando,
                "CUENTA_ATRAS":  self.render_cuenta_atras,
                "GAMEOVER":      self.render_gameover,
                "TIENDA_SKINS":  self.render_tienda_skins,
                "TIENDA_MUNDOS": self.render_tienda_mundos,
                "TIENDA_ARMAS":  self.render_tienda_armas,
                "CONFIG":        self.render_config,
                "SOCIAL":        self.render_social,
                "CLUB":          self.render_club,
            }
            if self.estado in dispatch:
                dispatch[self.estado](mundo, color_jug)
            else:
                self.estado = "MENU"

            # --- Dialogo flotante ---
            if self.dialogo_timer > 0:
                self.dialogo_timer -= 1
                alpha = min(255, self.dialogo_timer * 4)
                r = pygame.Rect(ANCHO//2-200, ALTO-80, 400, 50)
                panel(pantalla, r, (20,20,40), min(alpha, 200), 10, CIAN)
                img = F_SMALL.render(self.dialogo_msg, True, BLANCO)
                img.set_alpha(alpha)
                pantalla.blit(img, img.get_rect(center=r.center))

            pygame.display.flip()
            reloj.tick(FPS)

    # ─────────────────────────────────────────────────────────────
    #  EVENTOS TECLADO / MOUSE
    # ─────────────────────────────────────────────────────────────
    def _mousewheel(self, dy):
        if self.estado == "TIENDA_SKINS":
            self.scroll_skin = (self.scroll_skin - dy) % len(SKINS)
        elif self.estado == "TIENDA_MUNDOS":
            self.scroll_mundo = (self.scroll_mundo - dy) % len(MUNDOS)
        elif self.estado == "TIENDA_ARMAS":
            self.scroll_arma = (self.scroll_arma - dy) % len(ARMAS)

    def _keydown(self, e):
        st = self.estado

        # Input nombre
        if st == "NOMBRE":
            if e.key == pygame.K_BACKSPACE:
                self.input_nombre = self.input_nombre[:-1]
            elif e.key == pygame.K_RETURN:
                self._confirmar_nombre()
            elif len(self.input_nombre) < 16 and e.unicode.isprintable():
                self.input_nombre += e.unicode

        # Tutorial
        elif st == "TUTORIAL":
            if e.key in [pygame.K_SPACE, pygame.K_RETURN, pygame.K_RIGHT]:
                self.tutorial_paso += 1
                if self.tutorial_paso >= 7:
                    db["tutorial_visto"] = True
                    guardar_datos(db)
                    self.estado = "MENU"

        # Config
        elif st == "CONFIG":
            if e.key == pygame.K_ESCAPE:
                self.estado = "MENU"
            elif e.key == pygame.K_c:
                db["controles"] = "WASD" if db["controles"] == "FLECHAS" else "FLECHAS"
            elif e.key == pygame.K_r:
                db["record"] = 0
                self.mostrar_dialogo("Récord borrado.")
            elif e.key == pygame.K_UP:
                db["volumen"] = min(1.0, round(db["volumen"] + 0.1, 1))
                actualizar_vol_musica()
            elif e.key == pygame.K_DOWN:
                db["volumen"] = max(0.0, round(db["volumen"] - 0.1, 1))
                actualizar_vol_musica()

        # Gameover
        elif st == "GAMEOVER":
            if e.key == pygame.K_SPACE:
                self.reset_partida()
                self.estado = "CUENTA_ATRAS"
            elif e.key == pygame.K_m:
                self.estado = "MENU"
            elif e.key == pygame.K_w:
                self._compartir_whatsapp()

        # Social / club — input
        elif st == "SOCIAL":
            if e.key == pygame.K_ESCAPE:
                self.estado = "MENU"

        elif st == "CLUB":
            if e.key == pygame.K_ESCAPE:
                self.estado = "SOCIAL"
            if e.key == pygame.K_BACKSPACE:
                self.input_club = self.input_club[:-1]
                self.input_amigo_pin = self.input_amigo_pin[:-1]
            elif e.unicode.isprintable():
                if len(self.input_club) < 20:
                    self.input_club += e.unicode

        # Tiendas — ESC vuelve al menú sin cerrar
        elif st in ["TIENDA_SKINS","TIENDA_MUNDOS","TIENDA_ARMAS"]:
            if e.key == pygame.K_ESCAPE:
                guardar_datos(db)
                self.estado = "MENU"

        # Jugando
        elif st == "JUGANDO":
            if e.key == pygame.K_RIGHT:
                self.disparar()
            elif e.key == pygame.K_ESCAPE:
                self.estado = "MENU"

        # Cuenta atrás
        elif st == "CUENTA_ATRAS":
            pass  # solo esperar

    def _click(self, pos):
        """Maneja clics. Los botones de cada estado manejan sus propios clics."""
        pass  # Los botones usan su propia detección con pygame.event.get()

    def _confirmar_nombre(self):
        n = self.input_nombre.strip()
        if not nombre_valido(n):
            self.input_error = "Nombre inválido (2-16 letras, sin malas palabras)"
            play_snd(SND_ERROR)
            return
        db["nombre_jugador"] = n
        guardar_datos(db)
        self.estado = "TUTORIAL" if not db["tutorial_visto"] else "MENU"
        self.mostrar_dialogo(f"¡Bienvenido, {n}!")

    def _compartir_whatsapp(self):
        s = db["skin_actual"]
        m = db["mundo_actual"]
        msg = (f"🎮 ¡Hice {self.score_final} pts en Geometric Pro TORA!\n"
               f"Mundo: {MUNDOS[m]['nombre']} | Skin: {SKINS[s]['nombre']}\n"
               f"Mi PIN de amigo: {db['pin_amigo']}\n"
               f"¿Puedes superarme? 🏆")
        webbrowser.open("https://wa.me/?text=" + msg.replace(" ", "%20").replace("\n", "%0A"))

    def _comprar_skin(self, idx):
        if idx >= len(SKINS): return
        s = SKINS[idx]
        if db["skins_desbloqueadas"][idx]:
            db["skin_actual"] = idx
            self.mostrar_dialogo(f"Equipado: {s['nombre']}")
        elif db["bits"] >= s["precio"]:
            db["bits"] -= s["precio"]
            db["skins_desbloqueadas"][idx] = True
            db["skin_actual"] = idx
            play_snd(SND_COMPRA)
            self.mostrar_dialogo(f"¡Comprado: {s['nombre']}!")
            guardar_datos(db)
        else:
            falta = s["precio"] - db["bits"]
            self.mostrar_dialogo(f"Faltan {falta} bits")
            play_snd(SND_ERROR)

    def _comprar_mundo(self, idx):
        if idx >= len(MUNDOS): return
        m = MUNDOS[idx]
        if db["mundos_desbloqueados"][idx]:
            db["mundo_actual"] = idx
            self.mostrar_dialogo(f"Mundo: {m['nombre']}")
        elif db["bits"] >= m["precio"]:
            db["bits"] -= m["precio"]
            db["mundos_desbloqueados"][idx] = True
            db["mundo_actual"] = idx
            play_snd(SND_COMPRA)
            self.mostrar_dialogo(f"¡Desbloqueado: {m['nombre']}!")
            guardar_datos(db)
        else:
            falta = m["precio"] - db["bits"]
            self.mostrar_dialogo(f"Faltan {falta} bits")
            play_snd(SND_ERROR)

    def _comprar_arma(self, idx):
        if idx >= len(ARMAS): return
        a = ARMAS[idx]
        if db["armas_desbloqueadas"][idx]:
            db["arma_actual"] = idx
            self.mostrar_dialogo(f"Arma: {a['nombre']}")
        elif db["bits"] >= a["precio"]:
            db["bits"] -= a["precio"]
            db["armas_desbloqueadas"][idx] = True
            db["arma_actual"] = idx
            play_snd(SND_COMPRA)
            self.mostrar_dialogo(f"¡Comprado: {a['nombre']}!")
            guardar_datos(db)
        else:
            falta = a["precio"] - db["bits"]
            self.mostrar_dialogo(f"Faltan {falta} bits")
            play_snd(SND_ERROR)

    # ─────────────────────────────────────────────────────────────
    #  RENDER: PANTALLA DE NOMBRE
    # ─────────────────────────────────────────────────────────────
    def render_nombre(self, mundo, color_jug):
        panel(pantalla, pygame.Rect(100, 200, ANCHO-200, 450), (10,10,30), 230, 20, CIAN)
        txt(pantalla, "GEOMETRIC PRO", F_BIG, CIAN, ANCHO//2, 280, sombra=True)
        txt(pantalla, "TORA EDITION", F_MED, AMARILLO, ANCHO//2, 360)
        txt(pantalla, "¿Cuál es tu nombre, jugador?", F_SMALL, BLANCO, ANCHO//2, 430)

        # Caja de texto
        r = pygame.Rect(150, 460, ANCHO-300, 50)
        pygame.draw.rect(pantalla, (30,30,60), r, border_radius=8)
        pygame.draw.rect(pantalla, CIAN, r, 2, border_radius=8)
        cursor = "|" if (self.ticker // 30) % 2 == 0 else ""
        txt(pantalla, self.input_nombre + cursor, F_MED, BLANCO, ANCHO//2, 485)

        # Error
        if self.input_error:
            txt(pantalla, self.input_error, F_SMALL, ROJO, ANCHO//2, 530)

        txt(pantalla, "[ENTER] Confirmar", F_SMALL, GRIS, ANCHO//2, 580)

    # ─────────────────────────────────────────────────────────────
    #  RENDER: TUTORIAL
    # ─────────────────────────────────────────────────────────────
    TUTORIAL_PASOS = [
        ("¡Bienvenido!", "Esquiva los bloques rojos que caen del espacio.", CIAN),
        ("MOVERSE", "← → (o A/D) para moverte. ¡No te choques!", AMARILLO),
        ("BOOST / DASH", "Tecla IZQUIERDA del teclado: activa el BOOST.\n¡Es muy rápido pero tarda en recargarse!", NARANJA),
        ("DISPARAR", "Tecla DERECHA: dispara contra los enemigos.\n¡Tienes balas limitadas! Cada 5000 pts ganas 5.", ROJO),
        ("BITS", "Ganas BITS al terminar partidas.\nCon bits compras skins, mundos y armas.", AMARILLO),
        ("TIENDAS", "[S] Skins  [W] Mundos  [A] Armas\nElige con la rueda del mouse o las flechas.", VERDE),
        ("¡LISTO!", f"Tu PIN de amigo: {db['pin_amigo']}\nCompártelo para que te añadan. ¡Suerte!", MAGENTA),
    ]

    def render_tutorial(self, mundo, color_jug):
        paso = min(self.tutorial_paso, len(self.TUTORIAL_PASOS)-1)
        titulo, desc, color = self.TUTORIAL_PASOS[paso]

        panel(pantalla, pygame.Rect(60, 180, ANCHO-120, 500), (10,10,30), 220, 20, color)
        txt(pantalla, f"TUTORIAL  {paso+1}/{len(self.TUTORIAL_PASOS)}", F_SMALL, GRIS, ANCHO//2, 210)
        txt(pantalla, titulo, F_BIG, color, ANCHO//2, 310, sombra=True)

        for i, linea in enumerate(desc.split("\n")):
            txt(pantalla, linea, F_MED, BLANCO, ANCHO//2, 420 + i*50)

        # Barra de progreso
        bw = ANCHO - 200
        dibujar_barra(pantalla, 100, 640, bw, 12, paso+1, len(self.TUTORIAL_PASOS), color)

        pulsa = "ESPACIO / →" if paso < len(self.TUTORIAL_PASOS)-1 else "ESPACIO para jugar"
        txt(pantalla, f"[{pulsa}]", F_SMALL, GRIS, ANCHO//2, 680)

        # Mini jugador animado
        ang = math.sin(self.ticker * 0.05) * 20
        cx, cy = ANCHO//2, 570
        pygame.draw.rect(pantalla, CIAN, (cx-20, cy-20, 40, 40), border_radius=8)

    # ─────────────────────────────────────────────────────────────
    #  RENDER: MENÚ
    # ─────────────────────────────────────────────────────────────
    def render_menu(self, mundo, color_jug):
        # Título con efecto latido
        escala = 1.0 + 0.03 * math.sin(self.ticker * 0.05)
        img_t = F_HUGE.render("GEOMETRIC PRO", True, color_jug)
        w, h  = img_t.get_size()
        img_t2 = pygame.transform.scale(img_t, (int(w*escala), int(h*escala)))
        pantalla.blit(img_t2, img_t2.get_rect(center=(ANCHO//2, 130)))

        txt(pantalla, "TORA EDITION v2.0", F_MED, AMARILLO, ANCHO//2, 200, sombra=True)

        # Panel info
        panel(pantalla, pygame.Rect(50, 230, ANCHO-100, 100), (15,15,35), 200, 14)
        txt(pantalla, f"👤 {db['nombre_jugador']}   PIN: {db['pin_amigo']}", F_SMALL, GRIS, ANCHO//2, 260)
        txt(pantalla, f"🏆 RÉCORD: {db['record']}   💰 BITS: {db['bits']}", F_MED, AMARILLO, ANCHO//2, 295)

        # Botones
        bts = [
            (pygame.Rect(200, 360, 300, 55), "▶  JUGAR",          VERDE,    NEGRO),
            (pygame.Rect(200, 430, 300, 55), "🎨 SKINS",           AZUL_NEÓN,BLANCO),
            (pygame.Rect(200, 500, 300, 55), "🌍 MUNDOS",          NARANJA,  NEGRO),
            (pygame.Rect(200, 570, 300, 55), "⚔  ARMAS",           ROJO,     BLANCO),
            (pygame.Rect(200, 640, 300, 55), "👥 SOCIAL / CLUB",   MAGENTA,  BLANCO),
            (pygame.Rect(200, 710, 300, 55), "⚙  CONFIG",          GRIS_OSC, BLANCO),
        ]
        acciones = ["JUGANDO","TIENDA_SKINS","TIENDA_MUNDOS","TIENDA_ARMAS","SOCIAL","CONFIG"]

        for (rect, label, cf, ct), accion in zip(bts, acciones):
            if boton_click(pantalla, label, F_MED, rect, cf, ct, 14, BLANCO):
                if accion == "JUGANDO":
                    self.reset_partida()
                    self.estado = "CUENTA_ATRAS"
                else:
                    self.estado = accion

        # Mundo y skin actuales
        txt(pantalla, f"Mundo: {mundo['nombre']}  |  Skin: {SKINS[db['skin_actual']]['nombre']}", F_TINY, GRIS, ANCHO//2, 790)

    # ─────────────────────────────────────────────────────────────
    #  RENDER: CUENTA ATRÁS (3, 2, 1, ¡YA!)
    # ─────────────────────────────────────────────────────────────
    def render_cuenta_atras(self, mundo, color_jug):
        self.cuenta_timer += 1
        cuenta_intervalo  = 60  # 1 segundo por número
        num_actual = 3 - (self.cuenta_timer // cuenta_intervalo)

        if num_actual < 0:
            self.estado = "JUGANDO"
            return

        t_en_num = self.cuenta_timer % cuenta_intervalo
        escala   = 1.0 + 0.5 * (1 - t_en_num/cuenta_intervalo)  # rebote
        alpha    = int(255 * (1 - t_en_num/cuenta_intervalo))

        labels = {3:"3", 2:"2", 1:"1", 0:"¡YA!"}
        colores= {3:ROJO, 2:AMARILLO, 1:VERDE, 0:CIAN}
        label  = labels.get(num_actual, "¡YA!")
        color  = colores.get(num_actual, CIAN)

        fuente_grande = pygame.font.Font(None, max(20, int(200*escala)))
        img = fuente_grande.render(label, True, color)
        img.set_alpha(alpha)
        pantalla.blit(img, img.get_rect(center=(ANCHO//2, ALTO//2)))

        txt(pantalla, "¡PREPÁRATE!", F_MED, BLANCO, ANCHO//2, ALTO//2 + 130)

    # ─────────────────────────────────────────────────────────────
    #  RENDER: JUGANDO
    # ─────────────────────────────────────────────────────────────
    def render_jugando(self, mundo, color_jug):
        teclas       = pygame.key.get_pressed()
        velocidad    = 7
        boost_activo = False

        ctrl_izq = teclas[pygame.K_LEFT]  if db["controles"] == "FLECHAS" else teclas[pygame.K_a]
        ctrl_der = teclas[pygame.K_RIGHT] if db["controles"] == "FLECHAS" else teclas[pygame.K_d]
        ctrl_boost = teclas[pygame.K_LALT] or teclas[pygame.K_RALT]   # ALT para boost

        # ── BOOST ────────────────────────────────────────────────
        if ctrl_boost and self.dash_cargado:
            velocidad    = 18
            boost_activo = True
            self.dash_cargado   = False
            self.dash_cooldown  = self.dash_carga_max
            play_snd(SND_DASH)
            for _ in range(8):
                self.particulas.append(Particula(
                    self.jugador.centerx, self.jugador.centery, color_jug, 6))

        if not self.dash_cargado:
            self.dash_cooldown -= 1
            if self.dash_cooldown <= 0:
                self.dash_cargado = True

        # ── MOVIMIENTO ───────────────────────────────────────────
        if ctrl_izq: self.jugador.x -= velocidad
        if ctrl_der: self.jugador.x += velocidad
        self.jugador.clamp_ip(pygame.Rect(2, 0, ANCHO-4, ALTO))
        if self.jugador.left  < 2:     self.jugador.left  = 2
        if self.jugador.right > ANCHO-2: self.jugador.right = ANCHO-2

        # ── ESTELA ───────────────────────────────────────────────
        self.estela.append((self.jugador.x, self.jugador.y, color_jug))
        if len(self.estela) > 14:
            self.estela.pop(0)
        for i, (ex, ey, ec) in enumerate(self.estela):
            a = int(255 * (i/14) * 0.5)
            s = pygame.Surface((50,50), pygame.SRCALPHA)
            pygame.draw.rect(s, (*ec, a), (0,0,50,50), border_radius=12)
            pantalla.blit(s, (ex, ey))

        # ── DIBUJAR JUGADOR ──────────────────────────────────────
        self.draw_jugador(pantalla, color_jug)

        # ── CREAR ENEMIGOS ───────────────────────────────────────
        frec = max(8, mundo["frecuencia"] - self.nivel)
        if random.randint(1, frec) == 1:
            # Evitar superposición
            for _ in range(5):
                en = Enemigo(mundo, self.nivel)
                if not any(en.rect.inflate(20,20).colliderect(ex.rect) for ex in self.enemigos):
                    self.enemigos.append(en)
                    break

        # ── ACTUALIZAR ENEMIGOS ──────────────────────────────────
        invisible = mundo["nombre"] == "EL VACÍO"
        for en in self.enemigos[:]:
            en.update(mundo["vel_base"], self.nivel)
            en.draw(pantalla, invisible)
            if en.y > ALTO + 20:
                self.enemigos.remove(en)
                continue
            # Colisión con jugador
            if en.rect.inflate(-8,-8).colliderect(self.jugador.inflate(-8,-8)):
                self._game_over(color_jug)
                return

        # ── BALAS ────────────────────────────────────────────────
        arma = ARMAS[db["arma_actual"]]
        for b in self.balas[:]:
            b.update(pantalla)
            if not b.activa:
                self.balas.remove(b)
                continue
            for en in self.enemigos[:]:
                if en.rect.collidepoint(b.x, b.y):
                    en.vida -= arma["daño"]
                    b.activa = False
                    play_snd(SND_BALA_HIT)
                    for _ in range(12):
                        self.particulas.append(Particula(b.x, b.y, en.color, 5))
                    if en.vida <= 0:
                        self.enemigos.remove(en)
                        self.score += 50
                        self.numeros_flotantes.append(NumeroFlotante(en.rect.x, en.rect.y, "+50", VERDE))
                    break

        # ── PARTÍCULAS ───────────────────────────────────────────
        self.particulas      = [p for p in self.particulas      if p.update(pantalla)]
        self.numeros_flotantes = [n for n in self.numeros_flotantes if n.update(pantalla)]

        # ── SCORE ────────────────────────────────────────────────
        self.score += 1
        if self.score % 500 == 0:
            self.nivel += 1
            play_snd(SND_NIVEL)
            self.mostrar_dialogo(f"¡NIVEL {self.nivel}!")

        # Balas extra cada 5000 pts
        if self.score - self.pts_ultima_bala >= 5000:
            self.pts_ultima_bala = self.score
            self.balas_restantes += 5
            self.numeros_flotantes.append(NumeroFlotante(ANCHO//2-40, ALTO//2, "+5 BALAS", AMARILLO))

        # ── HUD ──────────────────────────────────────────────────
        # Barra de boost
        boost_ratio = self.dash_cooldown / self.dash_carga_max if not self.dash_cargado else 0
        boost_color = VERDE if self.dash_cargado else NARANJA
        dibujar_barra(pantalla, 10, 10, 150, 14, self.dash_carga_max - self.dash_cooldown, self.dash_carga_max, boost_color)
        txt(pantalla, "BOOST [ALT]", F_TINY, boost_color, 88, 30, False)
        if self.dash_cargado:
            txt(pantalla, "¡LISTO!", F_TINY, VERDE, 165, 10, False)

        # Score y nivel
        txt(pantalla, f"SCORE: {self.score}", F_MED, BLANCO, ANCHO//2, 25, sombra=True)
        txt(pantalla, f"NV {self.nivel}", F_SMALL, GRIS, ANCHO//2, 55)

        # Balas
        arma_c = arma["color"] if db["arma_actual"] > 0 else GRIS
        txt(pantalla, f"⚡{self.balas_restantes} balas", F_SMALL, arma_c, ANCHO-10, 10, centrado=False)

        # Bits ganados esta partida (no acumulados en db hasta game over)
        self.bits_acumulados = self.bits_por_score(self.score)
        txt(pantalla, f"💰+{self.bits_acumulados}", F_TINY, AMARILLO, ANCHO-10, 40, centrado=False)

    def _game_over(self, color_jug):
        for _ in range(60):
            self.particulas.append(Particula(
                self.jugador.centerx, self.jugador.centery, color_jug, 10))
        play_snd(SND_MUERTE)
        self.score_final = self.score
        bits_ganados     = self.bits_por_score(self.score)
        db["bits"]       += bits_ganados
        db["bits_acumulados_sesion"] = db.get("bits_acumulados_sesion", 0) + bits_ganados
        if self.score > db["record"]:
            db["record"] = self.score
        db["partidas_jugadas"] = db.get("partidas_jugadas", 0) + 1
        guardar_datos(db)
        self.puntuacion_100, self.puntuacion_100_motivo = self.calcular_puntuacion()
        self.bits_ganados_ultima = bits_ganados
        self.estado = "GAMEOVER"

    # ─────────────────────────────────────────────────────────────
    #  RENDER: GAME OVER
    # ─────────────────────────────────────────────────────────────
    def render_gameover(self, mundo, color_jug):
        self.particulas = [p for p in self.particulas if p.update(pantalla)]

        panel(pantalla, pygame.Rect(60, 120, ANCHO-120, 620), (20,5,5), 210, 20, ROJO)

        txt(pantalla, "¡GAME OVER!", F_HUGE, ROJO, ANCHO//2, 210, sombra=True)
        txt(pantalla, f"PUNTOS: {self.score_final}", F_BIG, BLANCO, ANCHO//2, 300)
        txt(pantalla, f"RÉCORD: {db['record']}", F_MED, AMARILLO, ANCHO//2, 360)

        # Puntuación /100
        color_pts = VERDE if self.puntuacion_100 >= 80 else (AMARILLO if self.puntuacion_100 >= 50 else ROJO)
        txt(pantalla, f"PUNTUACIÓN: {self.puntuacion_100}/100", F_MED, color_pts, ANCHO//2, 415)
        txt(pantalla, getattr(self, "puntuacion_100_motivo", ""), F_SMALL, color_pts, ANCHO//2, 450)

        txt(pantalla, f"💰 +{self.bits_ganados_ultima} bits ganados", F_SMALL, AMARILLO, ANCHO//2, 490)

        # Botones
        b_retry = pygame.Rect(110, 530, 220, 55)
        b_menu  = pygame.Rect(370, 530, 220, 55)
        b_wp    = pygame.Rect(ANCHO//2-150, 600, 300, 55)

        if boton_click(pantalla, "▶ REINTENTAR", F_MED, b_retry, VERDE, NEGRO, 14, BLANCO):
            self.reset_partida()
            self.estado = "CUENTA_ATRAS"

        if boton_click(pantalla, "🏠 MENÚ", F_MED, b_menu, GRIS_OSC, BLANCO, 14, GRIS):
            self.estado = "MENU"

        if boton_click(pantalla, "📲 COMPARTIR WA", F_SMALL, b_wp, WHATSAPP, BLANCO, 14):
            self._compartir_whatsapp()

    # ─────────────────────────────────────────────────────────────
    #  RENDER: TIENDA SKINS
    # ─────────────────────────────────────────────────────────────
    def render_tienda_skins(self, mundo, color_jug):
        txt(pantalla, "🎨 ARMERÍA DE SKINS", F_BIG, CIAN, ANCHO//2, 60, sombra=True)
        txt(pantalla, f"💰 BITS: {db['bits']}", F_MED, AMARILLO, ANCHO//2, 105)
        txt(pantalla, "Rueda del mouse para cambiar | [ESC] Volver", F_TINY, GRIS, ANCHO//2, 135)

        idx = self.scroll_skin % len(SKINS)
        s   = SKINS[idx]
        desbloq = db["skins_desbloqueadas"][idx]
        equipada = db["skin_actual"] == idx

        # Preview grande
        cx, cy = ANCHO//2, 320
        color_prev = s["color"]
        if s["nombre"] == "ARCOÍRIS":
            t = self.ticker * 2 % 360
            color_prev = (int(128+127*math.sin(math.radians(t))),
                          int(128+127*math.sin(math.radians(t+120))),
                          int(128+127*math.sin(math.radians(t+240))))
        if s["brillo"]:
            glow = pygame.Surface((120,120), pygame.SRCALPHA)
            pygame.draw.circle(glow, (*color_prev, 60), (60,60), 60)
            pantalla.blit(glow, (cx-60, cy-60))
        if s["forma"] == "diamante":
            pts = [(cx, cy-40), (cx+40, cy), (cx, cy+40), (cx-40, cy)]
            pygame.draw.polygon(pantalla, color_prev, pts)
        else:
            pygame.draw.rect(pantalla, color_prev, (cx-35, cy-35, 70, 70), border_radius=12)

        # Flechas de navegación
        txt(pantalla, "◀", F_BIG, BLANCO, cx-160, cy)
        txt(pantalla, "▶", F_BIG, BLANCO, cx+160, cy)

        # Info
        panel(pantalla, pygame.Rect(100, 400, ANCHO-200, 200), (15,15,35), 200, 14, s["color"])
        txt(pantalla, s["nombre"], F_BIG, s["color"], ANCHO//2, 440, sombra=True)
        txt(pantalla, s["descripcion"], F_SMALL, BLANCO, ANCHO//2, 485)

        if equipada:
            estado_txt, c_btn = "✓ EQUIPADA", VERDE
        elif desbloq:
            estado_txt, c_btn = "EQUIPAR (gratis)", AZUL_NEÓN
        else:
            estado_txt, c_btn = f"COMPRAR  {s['precio']} bits", AMARILLO

        b = pygame.Rect(ANCHO//2-130, 510, 260, 55)
        if boton_click(pantalla, estado_txt, F_MED, b, c_btn, NEGRO, 14, BLANCO):
            self._comprar_skin(idx)
            guardar_datos(db)

        # Índice visual
        txt(pantalla, f"{idx+1} / {len(SKINS)}", F_SMALL, GRIS, ANCHO//2, 580)

        # Botones flechas clicables
        b_izq = pygame.Rect(cx-220, cy-30, 60, 60)
        b_der = pygame.Rect(cx+160, cy-30, 60, 60)
        if boton_click(pantalla, "◀", F_MED, b_izq, GRIS_OSC, BLANCO, 8):
            self.scroll_skin = (self.scroll_skin - 1) % len(SKINS)
        if boton_click(pantalla, "▶", F_MED, b_der, GRIS_OSC, BLANCO, 8):
            self.scroll_skin = (self.scroll_skin + 1) % len(SKINS)

        # Botón reset compras skins
        b_reset = pygame.Rect(ANCHO//2-120, 620, 240, 44)
        if boton_click(pantalla, "🔄 Resetear compras skins", F_TINY, b_reset, (60,10,10), ROJO, 10, ROJO):
            db["skins_desbloqueadas"] = [True] + [False]*(len(SKINS)-1)
            db["skin_actual"] = 0
            self.mostrar_dialogo("Skins reseteadas.")
            guardar_datos(db)

        b_back = pygame.Rect(ANCHO//2-80, 680, 160, 44)
        if boton_click(pantalla, "[ESC] Volver", F_SMALL, b_back, GRIS_OSC, BLANCO, 10):
            self.estado = "MENU"
            guardar_datos(db)

    # ─────────────────────────────────────────────────────────────
    #  RENDER: TIENDA MUNDOS
    # ─────────────────────────────────────────────────────────────
    def render_tienda_mundos(self, mundo, color_jug):
        txt(pantalla, "🌍 MUNDOS", F_BIG, NARANJA, ANCHO//2, 60, sombra=True)
        txt(pantalla, f"💰 BITS: {db['bits']}", F_MED, AMARILLO, ANCHO//2, 105)
        txt(pantalla, "Rueda del mouse para cambiar | [ESC] Volver", F_TINY, GRIS, ANCHO//2, 135)

        idx  = self.scroll_mundo % len(MUNDOS)
        m    = MUNDOS[idx]
        desbloq  = db["mundos_desbloqueados"][idx]
        actual   = db["mundo_actual"] == idx

        panel(pantalla, pygame.Rect(60, 165, ANCHO-120, 480), m["bg"], 230, 16, m["estrella"])

        # Mini estrellas del mundo preview
        for _ in range(8):
            rx, ry = random.randint(70, ANCHO-70), random.randint(175, 560)
            pygame.draw.circle(pantalla, m["estrella"], (rx, ry), random.randint(1,2))

        txt(pantalla, m["nombre"], F_HUGE, m["estrella"], ANCHO//2, 280, sombra=True)
        txt(pantalla, m["descripcion"], F_SMALL, BLANCO, ANCHO//2, 360)
        txt(pantalla, f"Velocidad: {'⚡'*int(m['vel_base']//2+1)}", F_SMALL, m["estrella"], ANCHO//2, 400)

        if actual:
            estado_txt, c_btn = "✓ ACTUAL", VERDE
        elif desbloq:
            estado_txt, c_btn = "SELECCIONAR", AZUL_NEÓN
        else:
            precio = m["precio"]
            estado_txt, c_btn = f"COMPRAR  {precio} bits", AMARILLO

        b = pygame.Rect(ANCHO//2-130, 440, 260, 55)
        if boton_click(pantalla, estado_txt, F_MED, b, c_btn, NEGRO, 14, BLANCO):
            self._comprar_mundo(idx)
            guardar_datos(db)

        # Flechas
        b_izq = pygame.Rect(70, 300, 60, 60)
        b_der = pygame.Rect(ANCHO-130, 300, 60, 60)
        if boton_click(pantalla, "◀", F_MED, b_izq, GRIS_OSC, BLANCO, 8):
            self.scroll_mundo = (self.scroll_mundo - 1) % len(MUNDOS)
        if boton_click(pantalla, "▶", F_MED, b_der, GRIS_OSC, BLANCO, 8):
            self.scroll_mundo = (self.scroll_mundo + 1) % len(MUNDOS)

        txt(pantalla, f"{idx+1} / {len(MUNDOS)}", F_SMALL, GRIS, ANCHO//2, 510)

        # Botón reset mundos
        b_reset = pygame.Rect(ANCHO//2-120, 560, 240, 44)
        if boton_click(pantalla, "🔄 Resetear mundos", F_TINY, b_reset, (60,10,10), ROJO, 10, ROJO):
            db["mundos_desbloqueados"] = [True] + [False]*(len(MUNDOS)-1)
            db["mundo_actual"] = 0
            self.mostrar_dialogo("Mundos reseteados.")
            guardar_datos(db)

        b_back = pygame.Rect(ANCHO//2-80, 620, 160, 44)
        if boton_click(pantalla, "[ESC] Volver", F_SMALL, b_back, GRIS_OSC, BLANCO, 10):
            self.estado = "MENU"
            guardar_datos(db)

    # ─────────────────────────────────────────────────────────────
    #  RENDER: TIENDA ARMAS
    # ─────────────────────────────────────────────────────────────
    def render_tienda_armas(self, mundo, color_jug):
        txt(pantalla, "⚔  ARMERÍA", F_BIG, ROJO, ANCHO//2, 60, sombra=True)
        txt(pantalla, f"💰 BITS: {db['bits']}", F_MED, AMARILLO, ANCHO//2, 105)
        txt(pantalla, "Rueda del mouse para cambiar | [ESC] Volver", F_TINY, GRIS, ANCHO//2, 135)

        idx    = self.scroll_arma % len(ARMAS)
        a      = ARMAS[idx]
        desbloq = db["armas_desbloqueadas"][idx]
        actual  = db["arma_actual"] == idx

        panel(pantalla, pygame.Rect(80, 165, ANCHO-160, 400), (15,5,5), 220, 16, a["color"])

        # Animación de la bala
        t = self.ticker % 80
        bx = ANCHO//2
        by = int(220 + t * 3)
        if a["tipo"] == "spread":
            for ang in [-20,-10,0,10,20]:
                rad = math.radians(ang)
                pygame.draw.circle(pantalla, a["color"],
                    (int(bx + math.sin(rad)*t*0.5), int(220 + t*2.5 - abs(ang)*0.5)), 6)
        elif a["tipo"] == "plasma":
            pygame.draw.circle(pantalla, a["color"], (bx, by), 12)
            glow = pygame.Surface((50,50),pygame.SRCALPHA)
            pygame.draw.circle(glow, (*a["color"],80),(25,25),25)
            pantalla.blit(glow, (bx-25, by-25))
        elif a["tipo"] == "laser":
            pygame.draw.rect(pantalla, a["color"], (bx-2, 220, 4, t*3))
        elif a["tipo"] != "ninguna":
            pygame.draw.circle(pantalla, a["color"], (bx, by), 7)

        txt(pantalla, a["nombre"], F_BIG, a["color"], ANCHO//2, 390, sombra=True)
        txt(pantalla, a["desc"],   F_SMALL, BLANCO, ANCHO//2, 435)

        if actual:
            estado_txt, c_btn = "✓ EQUIPADA", VERDE
        elif desbloq:
            estado_txt, c_btn = "EQUIPAR", AZUL_NEÓN
        else:
            estado_txt, c_btn = f"COMPRAR  {a['precio']} bits", AMARILLO

        b = pygame.Rect(ANCHO//2-130, 480, 260, 55)
        if boton_click(pantalla, estado_txt, F_MED, b, c_btn, NEGRO, 14, BLANCO):
            self._comprar_arma(idx)
            guardar_datos(db)

        b_izq = pygame.Rect(85, 390, 60, 55)
        b_der = pygame.Rect(ANCHO-145, 390, 60, 55)
        if boton_click(pantalla, "◀", F_MED, b_izq, GRIS_OSC, BLANCO, 8):
            self.scroll_arma = (self.scroll_arma - 1) % len(ARMAS)
        if boton_click(pantalla, "▶", F_MED, b_der, GRIS_OSC, BLANCO, 8):
            self.scroll_arma = (self.scroll_arma + 1) % len(ARMAS)

        txt(pantalla, f"{idx+1} / {len(ARMAS)}", F_SMALL, GRIS, ANCHO//2, 550)

        b_back = pygame.Rect(ANCHO//2-80, 610, 160, 44)
        if boton_click(pantalla, "[ESC] Volver", F_SMALL, b_back, GRIS_OSC, BLANCO, 10):
            self.estado = "MENU"
            guardar_datos(db)

    # ─────────────────────────────────────────────────────────────
    #  RENDER: CONFIG
    # ─────────────────────────────────────────────────────────────
    def render_config(self, mundo, color_jug):
        panel(pantalla, pygame.Rect(60, 60, ANCHO-120, 750), (12,12,28), 220, 18, CIAN)
        txt(pantalla, "⚙  CONFIGURACIÓN", F_BIG, BLANCO, ANCHO//2, 130, sombra=True)

        # Volumen
        txt(pantalla, f"VOLUMEN: {int(db['volumen']*100)}%", F_MED, BLANCO, ANCHO//2, 220)
        dibujar_barra(pantalla, 150, 245, ANCHO-300, 20, db["volumen"], 1.0, CIAN)
        txt(pantalla, "[↑] Subir   [↓] Bajar", F_TINY, GRIS, ANCHO//2, 280)

        # Controles
        c_ctrl = VERDE if db["controles"] == "WASD" else CIAN
        b_ctrl = pygame.Rect(ANCHO//2-150, 310, 300, 55)
        if boton_click(pantalla, f"[C] CONTROLES: {db['controles']}", F_MED, b_ctrl, (20,30,50), c_ctrl, 12, c_ctrl):
            db["controles"] = "WASD" if db["controles"] == "FLECHAS" else "FLECHAS"

        # Nombre
        txt(pantalla, f"Jugador: {db['nombre_jugador']}", F_MED, BLANCO, ANCHO//2, 400)
        b_nombre = pygame.Rect(ANCHO//2-120, 425, 240, 48)
        if boton_click(pantalla, "Cambiar nombre", F_SMALL, b_nombre, (20,20,50), CIAN, 10, CIAN):
            db["nombre_jugador"] = ""
            self.input_nombre    = ""
            self.input_error     = ""
            guardar_datos(db)
            self.estado = "NOMBRE"

        # Borrar récord
        b_rec = pygame.Rect(ANCHO//2-120, 495, 240, 48)
        if boton_click(pantalla, "Borrar récord", F_SMALL, b_rec, (50,10,10), ROJO, 10, ROJO):
            db["record"] = 0
            self.mostrar_dialogo("Récord borrado.")

        # Reset skins
        b_rs = pygame.Rect(ANCHO//2-150, 565, 300, 48)
        if boton_click(pantalla, "🔄 Resetear SKINS", F_SMALL, b_rs, (50,10,10), ROJO, 10, ROJO):
            db["skins_desbloqueadas"] = [True]+[False]*(len(SKINS)-1)
            db["skin_actual"] = 0
            self.mostrar_dialogo("Skins reseteadas.")
            guardar_datos(db)

        # Reset mundos
        b_rm = pygame.Rect(ANCHO//2-150, 625, 300, 48)
        if boton_click(pantalla, "🔄 Resetear MUNDOS", F_SMALL, b_rm, (50,10,10), ROJO, 10, ROJO):
            db["mundos_desbloqueados"] = [True]+[False]*(len(MUNDOS)-1)
            db["mundo_actual"] = 0
            self.mostrar_dialogo("Mundos reseteados.")
            guardar_datos(db)

        # Reset armas
        b_ra = pygame.Rect(ANCHO//2-150, 685, 300, 48)
        if boton_click(pantalla, "🔄 Resetear ARMAS", F_SMALL, b_ra, (50,10,10), ROJO, 10, ROJO):
            db["armas_desbloqueadas"] = [True]+[False]*(len(ARMAS)-1)
            db["arma_actual"] = 0
            self.mostrar_dialogo("Armas reseteadas.")
            guardar_datos(db)

        guardar_datos(db)

        b_back = pygame.Rect(ANCHO//2-80, 750, 160, 44)
        if boton_click(pantalla, "[ESC] Volver", F_SMALL, b_back, GRIS_OSC, BLANCO, 10):
            guardar_datos(db)
            self.estado = "MENU"

    # ─────────────────────────────────────────────────────────────
    #  RENDER: SOCIAL / AMIGOS / CLUB
    # ─────────────────────────────────────────────────────────────
    def render_social(self, mundo, color_jug):
        panel(pantalla, pygame.Rect(50, 60, ANCHO-100, 760), (10,5,25), 220, 18, MAGENTA)
        txt(pantalla, "👥 SOCIAL", F_BIG, MAGENTA, ANCHO//2, 130, sombra=True)

        # Tu PIN
        txt(pantalla, f"Tu PIN de amigo: {db['pin_amigo']}", F_MED, AMARILLO, ANCHO//2, 200)
        txt(pantalla, "Compártelo y que te busquen con él", F_TINY, GRIS, ANCHO//2, 230)

        # Añadir amigo
        txt(pantalla, "Añadir amigo (ingresa su PIN):", F_SMALL, BLANCO, ANCHO//2, 280)
        r_inp = pygame.Rect(200, 295, 300, 45)
        pygame.draw.rect(pantalla, (30,30,60), r_inp, border_radius=8)
        pygame.draw.rect(pantalla, MAGENTA, r_inp, 2, border_radius=8)
        cursor = "|" if (self.ticker//30)%2==0 else ""
        txt(pantalla, self.input_amigo_pin + cursor, F_MED, BLANCO, ANCHO//2, 317)

        # Input PIN amigo con teclado (solo números)
        teclas_pres = pygame.key.get_pressed()
        for ev in pygame.event.get(pygame.KEYDOWN):
            if ev.key == pygame.K_BACKSPACE:
                self.input_amigo_pin = self.input_amigo_pin[:-1]
            elif ev.unicode.isdigit() and len(self.input_amigo_pin) < 6:
                self.input_amigo_pin += ev.unicode
            elif ev.key == pygame.K_RETURN:
                self._agregar_amigo()
            elif ev.key == pygame.K_ESCAPE:
                self.estado = "MENU"

        if self.input_amigo_err:
            txt(pantalla, self.input_amigo_err, F_TINY, ROJO, ANCHO//2, 350)

        b_add = pygame.Rect(ANCHO//2-80, 360, 160, 44)
        if boton_click(pantalla, "Añadir amigo", F_SMALL, b_add, MAGENTA, NEGRO, 10, BLANCO):
            self._agregar_amigo()

        # Lista de amigos
        txt(pantalla, "Amigos:", F_SMALL, BLANCO, ANCHO//2, 425)
        amigos = db.get("amigos", [])
        if not amigos:
            txt(pantalla, "(Ninguno aún — ¡comparte tu PIN!)", F_TINY, GRIS, ANCHO//2, 455)
        for i, pin in enumerate(amigos[:6]):
            txt(pantalla, f"• PIN {pin}", F_SMALL, VERDE, ANCHO//2, 455 + i*30)

        # Compartir por WhatsApp
        b_wa = pygame.Rect(ANCHO//2-150, 640, 300, 50)
        if boton_click(pantalla, "📲 Compartir PIN por WhatsApp", F_SMALL, b_wa, WHATSAPP, BLANCO, 12):
            msg = (f"¡Únete a mi club en Geometric Pro TORA!\n"
                   f"Mi PIN: {db['pin_amigo']}\nDescárgalo y búscame 🎮")
            webbrowser.open("https://wa.me/?text=" + msg.replace(" ","%20").replace("\n","%0A"))

        # Botón club
        b_club = pygame.Rect(ANCHO//2-100, 705, 200, 50)
        if boton_click(pantalla, "🏆 MI CLUB", F_MED, b_club, (30,10,50), MAGENTA, 12, MAGENTA):
            self.estado = "CLUB"

        b_back = pygame.Rect(ANCHO//2-80, 770, 160, 44)
        if boton_click(pantalla, "[ESC] Volver", F_SMALL, b_back, GRIS_OSC, BLANCO, 10):
            self.estado = "MENU"

    def _agregar_amigo(self):
        pin = self.input_amigo_pin.strip()
        if len(pin) != 6 or not pin.isdigit():
            self.input_amigo_err = "El PIN debe tener 6 dígitos"
            play_snd(SND_ERROR)
            return
        if pin == db["pin_amigo"]:
            self.input_amigo_err = "No puedes añadirte a ti mismo"
            play_snd(SND_ERROR)
            return
        amigos = db.get("amigos", [])
        if pin in amigos:
            self.input_amigo_err = "Ya es tu amigo"
            return
        amigos.append(pin)
        db["amigos"] = amigos
        guardar_datos(db)
        self.input_amigo_pin = ""
        self.input_amigo_err = ""
        self.mostrar_dialogo(f"¡Solicitud enviada al PIN {pin}! (pendiente de aceptar)")
        play_snd(SND_COMPRA)

    # ─────────────────────────────────────────────────────────────
    #  RENDER: CLUB
    # ─────────────────────────────────────────────────────────────
    def render_club(self, mundo, color_jug):
        panel(pantalla, pygame.Rect(60, 60, ANCHO-120, 760), (5,5,20), 220, 18, PURPURA)
        txt(pantalla, "🏆 CLUB", F_BIG, PURPURA, ANCHO//2, 130, sombra=True)

        nombre_club = db.get("club_nombre", "")
        if not nombre_club:
            txt(pantalla, "Tu club no tiene nombre aún.", F_SMALL, GRIS, ANCHO//2, 210)
            txt(pantalla, "Escribe el nombre de tu club:", F_SMALL, BLANCO, ANCHO//2, 250)

            r_inp = pygame.Rect(150, 270, ANCHO-300, 48)
            pygame.draw.rect(pantalla, (20,20,45), r_inp, border_radius=8)
            pygame.draw.rect(pantalla, PURPURA, r_inp, 2, border_radius=8)
            cursor = "|" if (self.ticker//30)%2==0 else ""
            txt(pantalla, self.input_club + cursor, F_MED, BLANCO, ANCHO//2, 294)

            b_ok = pygame.Rect(ANCHO//2-100, 335, 200, 48)
            if boton_click(pantalla, "Crear Club", F_MED, b_ok, PURPURA, NEGRO, 12, BLANCO):
                nc = self.input_club.strip()
                if not nombre_valido(nc):
                    self.mostrar_dialogo("Nombre inválido para club")
                    play_snd(SND_ERROR)
                else:
                    db["club_nombre"] = nc
                    guardar_datos(db)
                    self.mostrar_dialogo(f"¡Club '{nc}' creado!")
                    play_snd(SND_COMPRA)
        else:
            txt(pantalla, nombre_club, F_BIG, PURPURA, ANCHO//2, 210, sombra=True)
            txt(pantalla, f"Fundador: {db['nombre_jugador']}", F_SMALL, BLANCO, ANCHO//2, 270)
            txt(pantalla, f"Miembros: {len(db.get('club_miembros',[]))+1}", F_SMALL, GRIS, ANCHO//2, 305)

            # Invitar por WhatsApp
            b_inv = pygame.Rect(ANCHO//2-160, 360, 320, 50)
            if boton_click(pantalla, "📲 Invitar al Club por WA", F_SMALL, b_inv, WHATSAPP, BLANCO, 12):
                msg = (f"¡Te invito al club '{nombre_club}' en Geometric Pro TORA! 🏆\n"
                       f"Mi PIN: {db['pin_amigo']}\nDescárgalo y únete.")
                webbrowser.open("https://wa.me/?text=" + msg.replace(" ","%20").replace("\n","%0A"))

            # Disolver club
            b_dis = pygame.Rect(ANCHO//2-100, 430, 200, 48)
            if boton_click(pantalla, "Disolver Club", F_SMALL, b_dis, (50,10,10), ROJO, 10, ROJO):
                db["club_nombre"] = ""
                guardar_datos(db)
                self.mostrar_dialogo("Club disuelto.")

            txt(pantalla, "Chat local del club:", F_SMALL, BLANCO, ANCHO//2, 510)
            txt(pantalla, "(El chat en tiempo real requiere servidor online.)", F_TINY, GRIS, ANCHO//2, 540)
            txt(pantalla, "Comparte clips de partida por WhatsApp ↑", F_TINY, GRIS, ANCHO//2, 570)

        b_back = pygame.Rect(ANCHO//2-80, 770, 160, 44)
        if boton_click(pantalla, "[ESC] Volver", F_SMALL, b_back, GRIS_OSC, BLANCO, 10):
            self.estado = "SOCIAL"


# ─────────────────────────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("  GEOMETRIC PRO: TORA EDITION v2.0 ULTRA")
    print("=" * 60)
    print(f"  Jugador: {db.get('nombre_jugador','(nuevo)')}")
    print(f"  PIN:     {db.get('pin_amigo','------')}")
    print(f"  Bits:    {db.get('bits', 0)}")
    print(f"  Récord:  {db.get('record', 0)}")
    print("=" * 60)
    print("  CONTROLES EN PARTIDA:")
    print("  ← / → (o A/D)  — Moverse")
    print("  ALT             — BOOST (recarga sola)")
    print("  →  (flecha der) — Disparar")
    print("  ESC             — Volver al menú")
    print("=" * 60)
    JuegoTora().ejecutar()
