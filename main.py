import pygame
from pygame.locals import *       #импортируем  модули и константы
import random


pygame.init()

screen_width = 1024
screen_height = 800

WINDOWSIZE = 700
GIRDSIZE = 10
CELL_SIZE = int(WINDOWSIZE / GIRDSIZE)         #сохроняем значения
LITElLEWINDOWSIZE = 150
LITELLEGIRDSIZE = 10
LITELLCELL_SIZE = int(LITElLEWINDOWSIZE/ LITELLEGIRDSIZE)

my_xod=True

blue_cells = []

white = (255, 255, 255)
blue = (0, 0, 255)                   #сохроняем цвета
black = (0, 0, 0)
red = (255, 0, 0)
green=(0,255,0)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Морской бой")

background_image = pygame.image.load("fon.jpg")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
                                                                                                 #сохроняеи картинки
background_image2 = pygame.image.load("fon2.png")
background_image2 = pygame.transform.scale(background_image2, (screen_width, screen_height))
background_image2.set_alpha(255)

background_image3 = pygame.image.load("fon3.png")
background_image3 = pygame.transform.scale(background_image3, (screen_width, screen_height))

win_image = pygame.image.load("victory.png")
win_image= pygame.transform.scale(win_image, (screen_width, screen_height))

lose_image = pygame.image.load("lose.png")
lose_image = pygame.transform.scale(lose_image , (screen_width, screen_height))

drow_image = pygame.image.load("drow.png")
drow_image = pygame.transform.scale(drow_image , (screen_width, screen_height))

font = pygame.font.Font(None, 74)
font_not_whith = pygame.font.Font(None, 35)          #сохроняем шрифты


shot_miss = pygame.mixer.Sound("sound/shoot_miss.mp3")
shot_miss .set_volume(0.1)

shot_hit = pygame.mixer.Sound("sound/shoot_hit.mp3")
shot_hit.set_volume(0.1)

sound_win = pygame.mixer.Sound("sound/sound_win.mp3")
sound_win.set_volume(0.1)


four_palub=True
three_palub=False
col_three_palub_corabl=0
two_palub=False
col_two_palub=0
one_palub=False
col_one_palub=0
nomer=3

state = "main_menu"  #сохроняем изначальное состояние экрана


#Создание (скачивание) виджетов для главного экрана
play_button = pygame.Rect(screen_width // 2 - 150, 200, 300, 100)
difficulty_button = pygame.Rect(screen_width // 2 - 150, 350, 300, 100)
rules_button = pygame.Rect(screen_width // 2 - 150, 500, 300, 100)


#Сохраняем переменные и создаём виджеты для игрового экрана
line_height = 30
enemy_button = pygame.Rect(800, 400, 200, 50)
cord_button = pygame.Rect(800, 200, 200, 50)
auto_cord_button= pygame.Rect(800, 600, 200, 50)

#Сохраняем переменные  и создаём виджеты для вражеского экрана
xod_button = pygame.Rect(800, 100, 200, 50)


#Сохраняем переменные и создаём виджеты для основного игрового цикла

col = 0
running = True
pole = [[0] * 10 for _ in range(10)]
last_blue_cells_count = 0
enemy_red_cells = []
enemy_green_cells = []
little_red_cells=[]
shoot=True
near_something=False
korabli={"1":"1",
         "2":"2",
         "3":"3",
         "4":"4",
         "5":"5",
         "6":"6",
         "7":"7",
         "8":"8",
         "9":"9",
         "10":"10"


         }
nom=0


list_of_cord_palub=[]

def draw_button(screen, rect, text):
    pygame.draw.rect(screen, blue, rect, 3)
    text_surf = font_not_whith.render(text, True, black)                      #функция  для отрисовки кнопки
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)

def is_button_pressed(rect, event):
    if event.type == MOUSEBUTTONDOWN:   # функция проверяющая нажата ли кнопка

        if rect.collidepoint(event.pos):

            return True
    return False

def right_corabl(col_palube):
    global col
    if col == col_palube:              #ФУНКЦИЯ ПРОВЕРЯЮЩАЯ ПРАВЕЛЬНОЕ ЛИ КОЛИЧЕСТВО ПАЛУБ У КОРОБЛЯ
        return True
    return False

def is_valid_position(pole, new_cells):
    for cell in new_cells:
        x, y = cell
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < 10 and 0 <= ny < 10 and pole[ny][nx] == 1:
                    return False
    return True


def is_one_line(new_cells):
    numx=0
    numy=0
    x,y=new_cells[0]    #вытащили x из первого элемента перед циклом
    old_x=x
    old_y=y


    for kletka in new_cells:
        x,y=kletka
        if x==old_x:

            old_x=x
        else:
            numx+=1


    for kletka in new_cells:
        x,y=kletka
        if y==old_y:

            old_y=y
        else:
            numy+=1


    if numx==0 or numy==0:
        return (True)

    else:
        return(False)


def is_near(new_cells):
    new_cells.sort()  # Сортируем клетки сначала по x, затем по y
    print(new_cells)
    for i in range(len(new_cells)-1):
        x1, y1 = new_cells[i]
        x2, y2 = new_cells[i + 1]
        if not ((x1 == x2 and abs(y1 - y2) == 1) or (y1 == y2 and abs(x1 - x2) == 1)):
            return False
    return True



def is_valid_pos(eboard, x, y, ship_size, direction):
    if direction == 'horizontal' and x + ship_size <= 10:
        for i in range(ship_size):
            if not is_valid_cell(eboard, x + i, y):
                return False
        return True
    elif direction == 'vertical' and y + ship_size <= 10:
        for i in range(ship_size):
            if not is_valid_cell(eboard, x, y + i):
                return False
        return True
    return False

def is_valid_cell(eboard, x, y):
    if eboard[y][x] != 0:
        return False
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if dx == 0 and dy == 0:
                continue
            nx, ny = x + dx, y + dy
            if 0 <= nx < 10 and 0 <= ny < 10 and eboard[ny][nx] != 0:
                return False
    return True

def generate_ship(eboard, ship_size):
    global list_of_cord_palub
    global nom
    while True:
        x = random.randint(0, 9)
        y = random.randint(0, 9)
        list_of_cord_palub = []

        direction = random.choice(['horizontal', 'vertical'])

        if is_valid_pos(eboard, x, y, ship_size, direction):
            if direction == 'horizontal':
                for i in range(ship_size):
                    eboard[y][x + i] = 1
                    list_of_cord_palub.append([y,x+i])

                    print(list_of_cord_palub )





            elif direction == 'vertical':
                for i in range(ship_size):
                    eboard[y + i][x] = 1
                    list_of_cord_palub.append([y+i, x])
                    print(list_of_cord_palub)
            current_key = nom % len(korabli)
            korabli[current_key] = list_of_cord_palub
            print(f"Координаты корабля для ключа {current_key}: {list_of_cord_palub}")

            nom += 1  # Увеличиваем счётчик, чтобы перейти к следующему ключу в следующем цикле
            return

def generate_board():
    eboard = [[0 for _ in range(10)] for _ in range(10)]
    ships = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]

    for ship_size in ships:
        generate_ship(eboard, ship_size)

    return eboard

def return_board(eboard):
    for row in eboard:
        return (' '.join(map(str, row)))

# Генерируем и выводим доску
eboard = generate_board()
return_board(eboard)
print(eboard )


def Hod():
    global shoot

    if my_xod == True:
        print("Сейчас ваш ход")


    elif my_xod == False:
        print("Сейчас ход соперника")
        if shoot==False:
            x_cord=random.randint(0,9)
            y_cord=random.randint(0,9)
            little_red_cells.append([x_cord,y_cord])
            shot_miss.play(loops=0)
            shot_miss.set_volume(0.1)
            shoot=not shoot


def draw_win():
    screen.blit(win_image, (0, 0))


def draw_lose():
    screen.blit(lose_image, (0, 0))


def Hwo_win(array):
    for i in array:
        if 1 in i:
            return False
    else:
        return(True )


def draw_gird(red_cells):
    global one_palub
    global col_one_palub
    global nomer
    for x in range(100,100+ WINDOWSIZE, CELL_SIZE):
        for y in range(50,50+ WINDOWSIZE, CELL_SIZE):
            rect = (x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, white, rect, 1)


            for date in blue_cells:

                kletka = (date[0] * CELL_SIZE + 100, date[1] * CELL_SIZE + 50, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, blue, kletka, 50)

    text = font.render("а   б   в   г   д   е   ё   ж   з   и", True, black)
    screen.blit(text, (100, 0))
    text1 = [font.render("1 ", True, black),
             font.render("2 ", True, black),
             font.render("3 ", True, black),
             font.render("4 ", True, black),
             font.render("5 ", True, black),
             font.render("6 ", True, black),
             font.render("7 ", True, black),
             font.render("8 ", True, black),
             font.render("9 ", True, black),
             font.render("10 ", True, black)]
    x, start_y = 40, 60
    line_height = 70
    for i, text in enumerate(text1):
        y = start_y + i * line_height
        screen.blit(text, (x, y))



def draw_enemy_gird(enemy_red_cells,enemy_green_cells):
    global one_palub
    global col_one_palub
    global nomer
    for x in range(100, 100 + WINDOWSIZE, CELL_SIZE):
        for y in range(50, 50 + WINDOWSIZE, CELL_SIZE):
            rect = (x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, white, rect, 1)


            for date in enemy_red_cells:

                kletka = (date[0] * CELL_SIZE + 100, date[1] * CELL_SIZE + 50, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, red, kletka, 50)
            for date in enemy_green_cells:
                kletka = (date[0] * CELL_SIZE + 100, date[1] * CELL_SIZE + 50, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen,green , kletka, 50)



    text = font.render("а   б   в   г   д   е   ё   ж   з   и", True, black)
    screen.blit(text, (100, 0))
    text1 = [font.render("1 ", True, black),
             font.render("2 ", True, black),
             font.render("3 ", True, black),
             font.render("4 ", True, black),
             font.render("5 ", True, black),
             font.render("6 ", True, black),
             font.render("7 ", True, black),
             font.render("8 ", True, black),
             font.render("9 ", True, black),
             font.render("10 ", True, black)]
    x, start_y = 40, 60
    line_height = 70
    for i, text in enumerate(text1):
        y = start_y + i * line_height
        screen.blit(text, (x, y))




def draw_little_gird(red_cells):
    global one_palub
    global col_one_palub
    global nomer
    for x in range(850, 850 + LITElLEWINDOWSIZE , LITELLCELL_SIZE ):
        for y in range(600, 600 + LITElLEWINDOWSIZE, LITELLCELL_SIZE ):
            rect = (x, y,  LITELLCELL_SIZE ,  LITELLCELL_SIZE )
            pygame.draw.rect(screen, white, rect, 1)

            for date in blue_cells:
                kletka = (date[0] * LITELLCELL_SIZE + 850  , date[1] *  LITELLCELL_SIZE + 600 , LITELLCELL_SIZE ,  LITELLCELL_SIZE )
                pygame.draw.rect(screen, blue, kletka, 50)
            for date in little_red_cells:
                kletka = (
                date[0] * LITELLCELL_SIZE + 850, date[1] * LITELLCELL_SIZE + 600, LITELLCELL_SIZE, LITELLCELL_SIZE)
                pygame.draw.rect(screen, red, kletka, 50)


    text = font.render("а   б   в   г   д   е   ё   ж   з   и", True, black)
    screen.blit(text, (100, 0))
    text1 = [font.render("1 ", True, black),
             font.render("2 ", True, black),
             font.render("3 ", True, black),
             font.render("4 ", True, black),
             font.render("5 ", True, black),
             font.render("6 ", True, black),
             font.render("7 ", True, black),
             font.render("8 ", True, black),
             font.render("9 ", True, black),
             font.render("10 ", True, black)]
    x, start_y = 40, 60
    line_height = 70
    for i, text in enumerate(text1):
        y = start_y + i * line_height
        screen.blit(text, (x, y))


def draw_main_menu():
    screen.blit(background_image, (0, 0))


    draw_button(screen, play_button, "Играть")
    draw_button(screen, difficulty_button, "Сложность")
    draw_button(screen, rules_button, "Правила")

    return play_button, difficulty_button, rules_button
def draw_enemy_screen():
    screen.blit(background_image3, (0, 0))
    draw_button(screen,xod_button , "поменять ход")
    return xod_button
def draw_game_screen():
    global four_palub
    global three_palub
    global two_palub
    global one_palub
    global col_one_palub
    global nomer
    x, y = 800, 10
    screen.blit(background_image2, (0, 0))
    if four_palub :
        text_four_kl = [font_not_whith.render("Поставьте", True, black),
                        font_not_whith.render(" четырёхпалубный ", True, black),
                        font_not_whith.render(" корабль", True, black)]
    elif  three_palub :
        text_four_kl = [font_not_whith.render("Поставьте", True, black),
                        font_not_whith.render(" трёхпалубный ", True, black),
                        font_not_whith.render(" корабль", True, black)]
    elif  two_palub:
        text_four_kl = [font_not_whith.render("Поставьте", True, black),
                        font_not_whith.render("двухпалубный ", True, black),
                        font_not_whith.render(" корабля", True, black)]
    elif one_palub and col_one_palub>=nomer:
        text_four_kl = [font.render("Корабли ", True, black),
        font.render("раставл-", True, black),
        font.render("енны", True, black)]


    elif  one_palub:
        text_four_kl = [font_not_whith.render("Поставьте", True, black),
                        font_not_whith.render(" однопалубный ", True, black),
                        font_not_whith.render(" корабль", True, black)]


    for i, text in enumerate(text_four_kl):
        y_line = y + i * line_height
        screen.blit(text, (x, y_line))


    draw_button(screen, enemy_button, "перейти")
    draw_button(screen, cord_button, "Поставить")
    draw_button(screen, auto_cord_button, "авто"
                                          "растановка")


    return enemy_button,cord_button,auto_cord_button





# Начинаем основной цикл программы
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        if state == "main_menu":
            play_button, difficulty_button, rules_button = draw_main_menu()
            if is_button_pressed(play_button, event):
                state = "game_screen"
        elif state == "game_screen":
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                state = "main_menu"

            enemy_button, cord_button,auto_cord_button  = draw_game_screen()
            if is_button_pressed(enemy_button, event):
                if one_palub and col_one_palub >= nomer:
                    state = "enemy_screen"
                    print("перейти")
                # else:
                #     print("Сначала раставьте корабли")
            if is_button_pressed(auto_cord_button, event):
                pole = generate_board()
                blue_cells = []
                for y in range(10):
                    for x in range(10):
                        if pole[y][x] == 1:
                            blue_cells.append([x, y])
                state = "enemy_screen"

            if is_button_pressed(cord_button, event):
                print("поставить")
                new_cells = blue_cells[last_blue_cells_count:]  # клетки, добавленные в текущей попытке
                print(new_cells)
                if four_palub:
                    col_palube = 4
                elif three_palub:
                    col_palube = 3
                elif two_palub:
                    col_palube = 2
                elif one_palub:
                    col_palube = 1

                if right_corabl(col_palube) and is_valid_position(pole, new_cells) and is_one_line(new_cells) and is_near(new_cells):
                    print("Правильно")
                    if four_palub:
                        four_palub = False
                        three_palub = True
                    elif three_palub and col_three_palub_corabl == 1:
                        three_palub = False
                        two_palub = True
                    elif three_palub:
                        col_three_palub_corabl += 1
                    elif two_palub and col_two_palub == 2:
                        two_palub = False
                        one_palub = True
                    elif two_palub:
                        col_two_palub += 1
                    elif one_palub and col_one_palub >= nomer:
                        print('привет')
                    elif one_palub:
                        col_one_palub += 1

                    for cell in new_cells:
                        pole[cell[1]][cell[0]] = 1
                        last_blue_cells_count = len(blue_cells)  # обновляем количество клеток после успешного размещения
                        print(pole)
                else:
                    print("Неправильно")
                    # Удаляем неправильно поставленные клетки из red_cells
                    blue_cells = blue_cells[:last_blue_cells_count]

                col = 0  # сброс счетчика

            if not (one_palub and col_one_palub >= nomer):
                if event.type == MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    if 100 <= mouse_x < 100 + WINDOWSIZE and 50 <= mouse_y < 50 + WINDOWSIZE:
                        grid_x = (mouse_x - 100) // CELL_SIZE
                        grid_y = (mouse_y - 50) // CELL_SIZE
                        blue_cells.append([grid_x, grid_y])
                        col += 1
            else:
                print("все корабли расставлены")
                state = "enemy_screen"

        if state == "enemy_screen":
            if Hwo_win(pole) == True:
                state = "win"


            if Hwo_win(eboard ) == True:
                state = "lose"



            xod_button = draw_enemy_screen()
            if Hwo_win(eboard):
                print("вы победили")
                state = "win"
                sound_win.play(loops=0)

            if Hwo_win(pole):
                print("вы проиграли")
                state = "lose"

            if is_button_pressed(xod_button, event):
                print("кнопка хода нажата")
                Hod()
                my_xod = not my_xod

            if event.type == MOUSEBUTTONDOWN:
                print(korabli)
                mouse_x, mouse_y = event.pos
                for i in eboard:
                    print(i)
                print(event.pos)


                if shoot==True:
                    if 100 <= mouse_x < 100 + WINDOWSIZE and 50 <= mouse_y < 50 + WINDOWSIZE:
                        gird_x = (mouse_x - 100) // CELL_SIZE
                        gird_y = (mouse_y - 50) // CELL_SIZE
                        print(gird_x, gird_y)
                        if ([gird_x,gird_y] not in enemy_red_cells) and ([gird_x,gird_y] not in enemy_red_cells):

                            if eboard[gird_y][gird_x] == 1:
                                shot_hit .play(loops=0)
                                print("попал")
                                enemy_green_cells.append([gird_x, gird_y])
                                shoot=True
                                eboard[gird_y][gird_x]=0





                            else:

                                print("не попал")
                                shot_miss.play(loops=0)
                                enemy_red_cells.append([gird_x, gird_y])
                                shoot=False
                        else:
                            print("вы сюда уже стреляли")
                else:
                    print("вы уже сделали выстрел")

    if state == "main_menu":
        draw_main_menu()
    elif state == "game_screen":
        draw_game_screen()
        draw_gird(blue_cells)
    elif state == "enemy_screen":
        draw_enemy_screen()
        draw_enemy_gird(enemy_red_cells, enemy_green_cells)
        draw_little_gird(blue_cells)
    elif state =="win":
        draw_win()
    elif state == "lose":
        draw_lose()



    pygame.display.flip()

pygame.quit()




