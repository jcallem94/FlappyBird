import pgzrun
import random

#Configuración inicial del juego
path = "/home/jcallem94/Documentos/Kodland/FlappyBird/"
max_score_file = "max_score.txt"

def load_max_score():
    global max_score
    try:
        with open(max_score_file, "r") as file:
            max_score = int(file.read())
    except FileNotFoundError:
        # El archivo aún no existe
        max_score = 0

#Parámetros del juego
TITLE = 'Flappy Bird'
WIDTH = 280
HEIGHT = 500

# Definir el fondo y el personaje
bg = 'background-day'
bs = "base"
background = Actor(path+"images/background-day.png")
base = Actor(path+"images/base.png",(150,470))
bird = Actor(path+"images/yellowbird-midflap.png", (WIDTH / 4, HEIGHT / 3))

begin = Actor(path+"images/message.png", (WIDTH / 2, HEIGHT / 2))
game_over = Actor(path+"images/gameover.png", (WIDTH / 2, HEIGHT / 3))

#Definir los parámetros del juego
load_max_score()
mode = 'begin'
gravity = 3
vy = 0
jump = -2

bg_veloc = 2
bg_pos = 0

pipe_gap = 88
pipe_speed = 1


score = 0

def update_bird(dt):
    global vy
    vy += gravity * dt
    bird.y += vy + 0.5*vy*dt
    if vy > 1:
        bird.image = path+'images/yellowbird-downflap.png'
    elif vy < 0:
        bird.image = path+'images/yellowbird-upflap.png'
    else:
        bird.image = path+'images/yellowbird-midflap.png'

def generate_pipe(pipe_down, pipe_up):
    pipe_position = random.randint(100, 300)
    pipe_down.pos = (WIDTH+20, pipe_position + pipe_gap // 2)
    pipe_up.pos = (WIDTH+20, pipe_position - pipe_gap // 2)

pipe_down_1 = Actor(path+"images/pipe-green-down.png", anchor=('left', 'top'))
pipe_up_1 = Actor(path+"images/pipe-green-up.png", anchor=('left', 'bottom'))
pipe_down_2 = Actor(path+"images/pipe-green-down.png", anchor=('left', 'top'))
pipe_up_2 = Actor(path+"images/pipe-green-up.png", anchor=('left', 'bottom'))

generate_pipe(pipe_down_1, pipe_up_1)
generate_pipe(pipe_down_2, pipe_up_2)
pipe_down_2.x = pipe_down_1.x + 170
pipe_up_2.x = pipe_down_2.x

def update_pipe(pipe_down, pipe_up):
    global score
    pipe_down.x -= pipe_speed
    pipe_up.x = pipe_down.x
    if pipe_down.x < -50:
        generate_pipe(pipe_down, pipe_up)
        pipe_down.x = WIDTH + 20
        score += 1

def reset_game():
    global vy
    global score
    vy = 0
    generate_pipe(pipe_down_1, pipe_up_1)
    pipe_down_2.x = pipe_down_1.x + 170
    pipe_up_2.x = pipe_down_2.x
    bird.pos = (WIDTH / 4, HEIGHT / 3)
    score = 0

def draw():
    # Dibujar el fondo y el personaje
    background.draw()
    screen.blit(bg, (bg_pos, 0))
    screen.blit(bg, (bg_pos + WIDTH, 0))
    if mode == 'begin':
        begin.draw()
        base.draw()
    elif mode == 'game':
        bird.draw()
        pipe_up_1.draw()
        pipe_down_1.draw()
        pipe_up_2.draw()
        pipe_down_2.draw()
        screen.draw.text(
            str(score),
            color='white',
            midtop=(WIDTH // 2, 10),
            fontsize=70,
            shadow=(1, 1)
        )
        screen.blit(bs, (bg_pos, 410))
        screen.blit(bs, (bg_pos + WIDTH, 410))
        screen.draw.text(
            f'Max Score: {max_score}',
            color='white',
            midtop=(WIDTH // 2, HEIGHT-50),
            fontsize=40,
            shadow=(1, 1)
        )
    elif mode == 'game_over':
        game_over.draw()
        screen.draw.text(
            'Press SPACE to play again',
            color='white',
            midtop=(WIDTH // 2, 250),
            fontsize=30,
            shadow=(1, 1)
        )   
        base.draw()
    
def update(dt):
    global vy
    global mode
    global max_score
    global bg_pos

    bg_pos -= bg_veloc

    if bg_pos <= -WIDTH:
        bg_pos = 0
    if mode == 'game':
        update_bird(dt)
    # Actualizar el juego (se llama automáticamente)
    if mode == 'game':
        update_bird(dt)
        update_pipe(pipe_down_1, pipe_up_1)
        update_pipe(pipe_down_2, pipe_up_2)
        if bird.colliderect(base) or bird.colliderect(pipe_down_1) or bird.colliderect(pipe_up_1) or bird.colliderect(pipe_down_2) or bird.colliderect(pipe_up_2):
            mode = 'game_over'
            if score > max_score:
                max_score = score
                with open(max_score_file, "w") as file:
                    file.write(str(max_score))

def on_key_down(key):
    global vy 
    global mode
    if mode == 'begin':
        if key == keys.SPACE:
            mode = 'game'
            reset_game()
    elif mode == 'game':
        if key == keys.SPACE:
            vy = jump
    elif mode == 'game_over':
        if key == keys.SPACE:
            mode = 'game'
            reset_game()

def on_mouse_down(button, pos) :
    global mode, vy
    if button == mouse.LEFT and mode == 'begin':
        mode = 'game'
        reset_game()
    elif mode == 'game' and button == mouse.LEFT:
        vy = jump
    elif mode == 'game_over' and button == mouse.LEFT:
        mode = 'game'
        reset_game()

pgzrun.go()