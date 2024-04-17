import pygame
import random
import mysql.connector

pygame.init()

# Definición de colores
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
bright_green = (0, 200, 0)
blue = (50, 153, 213)
bright_blue = (0, 0, 255)
red = (213, 50, 80)
bright_red = (255, 0, 0)
yellow = (255, 255, 102)

# Configuración de la pantalla
dis_width = 800
dis_height = 600
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game')

clock = pygame.time.Clock()

snake_block = 10
snake_speed = 15

# Fuentes
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# Conexión a la base de datos MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345678",
    database="snake_game"
)
cursor = db.cursor()

# Creación de la tabla si no existe
cursor.execute('''CREATE TABLE IF NOT EXISTS scores
                (name VARCHAR(255), score INT DEFAULT 0)''')
db.commit()
def get_max_score():
    cursor.execute("SELECT MAX(score) FROM scores")
    max_score = cursor.fetchone()[0]
    return max_score
# Función para mostrar el puntaje en pantalla
def Your_score(score):
    value = score_font.render("Score: " + str(score) + " Jugador: " + player_name + " Max_Score: " + str(get_max_score()), True, yellow)
    dis.blit(value, [0, 0])

# Función para dibujar la serpiente
def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])

# Función para mostrar mensajes en pantalla
def message(msg, color, y_displace=0):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])

# Función para crear botones interactivos
def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x < mouse[0] < x + w and y < mouse[1] < y + h:
        pygame.draw.rect(dis, ac, (x, y, w, h))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(dis, ic, (x, y, w, h))

    small_font = pygame.font.SysFont("bahnschrift", 20)
    text_surface = small_font.render(msg, True, black)
    text_rect = text_surface.get_rect()
    text_rect.center = (x + w / 2, y + h / 2)
    dis.blit(text_surface, text_rect)

# Función para mostrar el mensaje de ingreso de nombre
def display_enter_name_message():
    message("ENTER YOUR NAME", green, y_displace=50)
    button("Save", dis_width / 2 - 50, dis_height / 2 + 80, 100, 40, blue, bright_blue, save_name)

# Función para guardar el nombre del jugador
def save_name():
    global input_active, player_name, score

    input_active = False
    player_name = text_input
    print("Name saved:", player_name)
    gameLoop(player_name)

# Función para ingresar el nombre del jugador
def get_player_name():
    global input_active, text_input

    input_font = pygame.font.SysFont("bahnschrift", 32)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    text_input = text_input[:-1]
                else:
                    text_input += event.unicode

        dis.fill(blue)
        display_enter_name_message()

        pygame.draw.rect(dis, white, (dis_width / 3, dis_height / 2, 300, 40))
        txt_surface = input_font.render(text_input, True, black)
        dis.blit(txt_surface, (dis_width / 3 + 5, dis_height / 2 + 5))

        pygame.display.flip()
        clock.tick(30)
def game_over_message():
    game_over_font = pygame.font.SysFont("comicsansms", 50)
    text1 = game_over_font.render("Perdiste!", True, red)
    text2 = game_over_font.render("Presiona C para Jugar de Nuevo", True, red)
    text3 = game_over_font.render("o Q para Volver al Menú Principal", True, red)
    
    dis.blit(text1, (dis_width / 2 - text1.get_width() / 2, dis_height / 2 - text1.get_height()))
    dis.blit(text2, (dis_width / 2 - text2.get_width() / 2, dis_height / 2))
    dis.blit(text3, (dis_width / 2 - text3.get_width() / 2, dis_height / 2 + text3.get_height()))
# Función principal del juego
def gameLoop(player_name):
    global score
    score = 0
    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    while not game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0
                elif event.key == pygame.K_q:
                    game_over = True
                    game_close = False
                    break

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        dis.fill(blue)
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for segment in snake_List[:-1]:
            if segment == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)
        Your_score(Length_of_snake - 1)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1
            score = Length_of_snake - 1

        clock.tick(snake_speed)

        if game_close:
            dis.fill(blue)
            game_over_message()
            Your_score(Length_of_snake - 1)
            pygame.display.update()

            while True:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            game_over = True
                            game_close = False
                            save_high_score(player_name, score)
                            print("Score saved:", score)
                            game_menu()
                            pygame.quit()
                            quit()
                        if event.key == pygame.K_c:
                            gameLoop(player_name)
            break
    
    pygame.quit()
    quit()

# Función para ver los puntajes más altos
def view_high_scores():
    dis_scores = pygame.display.set_mode((dis_width, dis_height))
    pygame.display.set_caption('High Scores')

    dis_scores.fill(blue)

    cursor.execute("SELECT * FROM scores ORDER BY score DESC LIMIT 10")
    high_scores = cursor.fetchall()

    y_position = 20

    title_font = pygame.font.SysFont("bahnschrift", 40)
    title_text = title_font.render("High Scores", True, green)
    dis_scores.blit(title_text, (dis_width * 0.35, 10))

    for rank, score in enumerate(high_scores, start=1):
        text = f"{rank}. Name: {score[0]} | Score: {score[1]}"
        score_font = pygame.font.SysFont("comicsansms", 30)
        score_text = score_font.render(text, True, white)
        dis_scores.blit(score_text, (dis_width * 0.2, y_position))
        y_position += 40

    button_font = pygame.font.SysFont("bahnschrift", 30)
    button_text = button_font.render("Back", True, white)
    pygame.draw.rect(dis_scores, red, (dis_width * 0.4, dis_height * 0.8, dis_width * 0.2, 50))
    dis_scores.blit(button_text, (dis_width * 0.42, dis_height * 0.805))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if dis_width * 0.4 <= mouse_x <= dis_width * 0.6 and dis_height * 0.8 <= mouse_y <= dis_height * 0.85:
                    return

# Función para guardar el puntaje más alto
def save_high_score(name, score):
    if name:
        cursor.execute("INSERT INTO scores (name, score) VALUES (%s, %s)", (name, score))
        db.commit()
        print("Name saved:", name, "Score:", score)

# Función para salir del juego
def quit_game():
    pygame.quit()
    quit()

# Función para mostrar el menú principal
def game_menu():
    global text_input, input_active, player_name

    menu_active = True

    while menu_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    input_active = True
                    text_input = ""
                    player_name = ""
                    get_player_name()
                    if player_name:
                        input_active = False
                        gameLoop(player_name)
                        menu_active = False
                elif event.key == pygame.K_2:
                    view_high_scores()
                elif event.key == pygame.K_3:
                    quit_game()

        dis.fill(blue)

        # Ajusta la posición y tamaño del título centrado
        title_font = pygame.font.SysFont("bahnschrift", 60)
        title_text = title_font.render("Snake Game", True, green)
        title_rect = title_text.get_rect(center=(dis_width / 2, dis_height / 3))
        dis.blit(title_text, title_rect)

        button("Play", dis_width / 2 - 50, dis_height / 2, 100, 50, green, bright_green)
        button("High Scores", dis_width / 2 - 90, dis_height / 2 + 60, 180, 50, blue, bright_blue, view_high_scores)
        button("Quit", dis_width / 2 - 50, dis_height / 2 + 120, 100, 50, red, bright_red, quit_game)

        pygame.display.update()

    pygame.quit()
    quit()

text_input = ""
input_active = False
player_name = ""
score = 0

game_menu()
