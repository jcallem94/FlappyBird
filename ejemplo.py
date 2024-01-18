import pgzrun

WIDTH = 800
HEIGHT = 600

# Cargar las imágenes de fondo
background_day = 'background-day.png'
background_night = 'background-night.png'

# Inicializar la posición del fondo
posicion_fondo = 0

# Inicializar la mezcla entre día y noche
mezcla_dia_noche = 0.0
velocidad_mezcla = 0.005  # Ajusta la velocidad de la mezcla

def update():
    global posicion_fondo, mezcla_dia_noche

    # Mover el fondo hacia la izquierda
    posicion_fondo -= 2

    # Incrementar la mezcla gradualmente
    mezcla_dia_noche += velocidad_mezcla

    # Asegurarse de que la mezcla esté en el rango [0, 1]
    mezcla_dia_noche = min(1.0, max(0.0, mezcla_dia_noche))

    # Si el fondo se ha movido completamente fuera de la pantalla, reinícialo
    if posicion_fondo <= -WIDTH:
        posicion_fondo = 0

def draw():
    global mezcla_dia_noche

    # Interpolar entre las imágenes de fondo del día y la noche
    fondo_dia = interpolate_color('white', 'lightblue', mezcla_dia_noche)
    fondo_noche = interpolate_color('black', 'midnightblue', mezcla_dia_noche)

    # Dibujar el fondo en su posición actual y en la posición desplazada
    screen.fill(fondo_dia)
    screen.blit(background_day, (posicion_fondo, 0))

    screen.fill(fondo_noche)
    screen.blit(background_night, (posicion_fondo + WIDTH, 0))

def interpolate_color(color1, color2, alpha):
    """Realiza una interpolación lineal entre dos colores."""
    r = int((1 - alpha) * color1[0] + alpha * color2[0])
    g = int((1 - alpha) * color1[1] + alpha * color2[1])
    b = int((1 - alpha) * color1[2] + alpha * color2[2])
    return (r, g, b)

# Ejecutar el juego
pgzrun.go()