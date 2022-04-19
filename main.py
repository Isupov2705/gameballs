# импортирование модулей

import sqlite3 as sql
import pygame
from pygame.color import THECOLORS
import sys
import random
import time
from tkinter import *

# подключение базы данных

connection2 = sql.connect("data/db/game.db", check_same_thread=False)
r = connection2.cursor()

# основной код

''' Создание требуемых переменных '''
x = 475
y = 640
width = 150
height = 100
speed = 60
coordinates = [130, 190, 250, 310, 370, 430, 490, 550, 610, 670, 730, 790, 850, 910, 970]
nextBalls = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255), (255, 0, 255)]
a = 1
kill = 0
bullets = []
balls = []
rects = []
lvl = 1
iff = 0

''' Функции выбора уровня '''

def easy():
    global lvl
    lvl = 1

def medium():
    global lvl
    lvl = 2

def hard():
    global lvl
    lvl = 3

''' Функция запуска меню игры '''

def nachat():
    global iff
    iff += 1
    window = Tk()
    window.title('Добро пожаловать в игру "Шарики!"')
    btn = Button(window, text="Старт", font=("Courier New", 20), command=window.destroy)
    btn.grid(column=1, row=1)
    menu = Menu(window)
    new_item = Menu(menu, tearoff=0)
    new_item.add_command(label='Лёгкий', command=easy)
    new_item.add_separator()
    new_item.add_command(label='Средний', command=medium)
    new_item.add_separator()
    new_item.add_command(label='Тяжёлый', command=hard)
    menu.add_cascade(label='Настройки сложности', menu=new_item)
    window.config(menu=menu)
    window.mainloop()

''' Запуск игры '''

if iff == 0:
    nachat()

nachalo = time.time()

'''Создание начального окна'''

pygame.init()
win = pygame.display.set_mode((1100, 750))

gun = pygame.image.load('data/photo/gun.png')
background = pygame.image.load('data/photo/background.jpg')
pygame.display.set_caption('Игра "Шарики"')

''' Class снаряда (при выстреле) '''

class shell():
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed = 15

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

''' Class пушки  '''

class rect():
    def __init__(self, x, y, wight, height, color):
        self.x = x
        self.y = y
        self.wight = wight
        self.height = height
        self.color = color

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.wight, self.height))

''' Class мишени (шариков, по которым будет стрелять пушка) '''

class target():
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

''' Отрисовка окна игры '''

def drawWindow():
    win.blit(background, (0, 0))

    # pygame.draw.line(win, (0, 0, 0), (0, 430), (1100, 430), width=5)    -----    Линия между пушкой и шариками. Если требуется - можно раскомментировать

    for ball in balls:
        ball.draw(win)

    for bullet in bullets:
        bullet.draw(win)

    win.blit(gun, (x, y))

    for rec in rects:
        rec.draw(win)

    ''' Функция для отображения цвета последующих шариков '''

    if rects != []:
        font = pygame.font.SysFont('couriernew', 26, bold=True)
        text = font.render(str('Следующие цвета снарядов:'), True, THECOLORS['green'])
        win.blit(text, (5, 5))

    ''' Таймер, отсчитывающий время с начала игры '''

    font2 = pygame.font.SysFont('couriernew', 24, bold=True)
    text2 = font2.render(str(f'С начала игры прошло: {vremya}'), True, THECOLORS['yellow'])
    win.blit(text2, (630, 7))

    pygame.display.update()

''' Дополнительна функция, преобразующая данные базы данных в требуемый список '''

def checking(n):
    if n == '(255, 0, 0)': return (255, 0, 0)
    elif n == '(0, 255, 0)': return (0, 255, 0)
    elif n == '(0, 0, 255)': return (0, 0, 255)
    elif n == '(0, 255, 255)': return (0, 255, 255)
    elif n == '(255, 0, 255)': return (255, 0, 255)
    elif n == '(255, 255, 0)': return (255, 255, 0)
    elif n == '(255, 255, 255)': return (255, 255, 255)

''' Отрисовка самих шариков на поле '''

for i in range(3):
    for j in range(15):
        c = random.randint(1, 6)
        if c == 1:
            c = (255, 0, 0)
        elif c == 2:
            c = (0, 255, 0)
        elif c == 3:
            c = (0, 0, 255)
        elif c == 4:
            c = (255, 255, 0)
        elif c == 5:
            c = (0, 255, 255)
        else:
            c = (255, 0, 255)
        if i == 0:
            y1 = 130
            r.execute(f"SELECT * FROM first WHERE id = 1")
        elif i == 1:
            y1 = 190
            r.execute(f"SELECT * FROM first WHERE id = 2")
        else:
            y1 = 250
            r.execute(f"SELECT * FROM first WHERE id = 3")
        m = i + 1
        k = j + 1
        result = r.fetchall()
        x1 = result[0][j+1]
        if k == 1:
            r.execute(f"UPDATE second SET one = '{c}' WHERE id = '{m}'")
        elif k == 2:
            r.execute(f"UPDATE second SET two = '{c}' WHERE id = '{m}'")
        elif k == 3:
            r.execute(f"UPDATE second SET three = '{c}' WHERE id = '{m}'")
        elif k == 4:
            r.execute(f"UPDATE second SET four = '{c}' WHERE id = '{m}'")
        elif k == 5:
            r.execute(f"UPDATE second SET five = '{c}' WHERE id = '{m}'")
        elif k == 6:
            r.execute(f"UPDATE second SET six = '{c}' WHERE id = '{m}'")
        elif k == 7:
            r.execute(f"UPDATE second SET seven = '{c}' WHERE id = '{m}'")
        elif k == 8:
            r.execute(f"UPDATE second SET eight = '{c}' WHERE id = '{m}'")
        elif k == 9:
            r.execute(f"UPDATE second SET nine = '{c}' WHERE id = '{m}'")
        elif k == 10:
            r.execute(f"UPDATE second SET ten = '{c}' WHERE id = '{m}'")
        elif k == 11:
            r.execute(f"UPDATE second SET eleven = '{c}' WHERE id = '{m}'")
        elif k == 12:
            r.execute(f"UPDATE second SET twelve = '{c}' WHERE id = '{m}'")
        elif k == 13:
            r.execute(f"UPDATE second SET thirteen = '{c}' WHERE id = '{m}'")
        elif k == 14:
            r.execute(f"UPDATE second SET fourteen = '{c}' WHERE id = '{m}'")
        elif k == 15:
            r.execute(f"UPDATE second SET fifteen = '{c}' WHERE id = '{m}'")
        balls.append(target(x1, y1, 20, c))
        connection2.commit()

while True:
    vremya = str(int(time.time() - nachalo)) + ' сек.'
    pygame.time.delay(60)

    ''' Если нажата кнопка выхода '''

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print('Ну... Пока...')
            pygame.quit()
            sys.exit()

    ''' Проверка времени по уровням '''

    if lvl == 1:
        if int(time.time() - nachalo) > 400:
            print('Вы проиграли. Соболезную =(')
            pygame.quit()
            sys.exit()
    elif lvl == 2:
        if int(time.time() - nachalo) > 300:
            print('Вы проиграли. Соболезную =(')
            pygame.quit()
            sys.exit()
    elif lvl == 3:
        if int(time.time() - nachalo) > 200:
            print('Вы проиграли. Соболезную =(')
            pygame.quit()
            sys.exit()

    ''' Если уничтожены все шарики '''

    if kill == 45:
        print('Поздравляю! Вы выиграли!')
        pygame.quit()
        sys.exit()

    ''' Сравнение положения пули с шариками. Событие столкновения пули и шарика '''

    for bullet in bullets:
        if bullet.y > 0:
            if bullet.x == 130:
                e = 1
            elif bullet.x == 190:
                e = 2
            elif bullet.x == 250:
                e = 3
            elif bullet.x == 310:
                e = 4
            elif bullet.x == 370:
                e = 5
            elif bullet.x == 430:
                e = 6
            elif bullet.x == 490:
                e = 7
            elif bullet.x == 550:
                e = 8
            elif bullet.x == 610:
                e = 9
            elif bullet.x == 670:
                e = 10
            elif bullet.x == 730:
                e = 11
            elif bullet.x == 790:
                e = 12
            elif bullet.x == 850:
                e = 13
            elif bullet.x == 910:
                e = 14
            else:
                e = 15
            if bullet.y <= 250:
                r.execute(f"SELECT * FROM second WHERE id = 3")
                result = r.fetchall()
                itog = result[0][e]
                connection2.commit()
                if checking(itog) == bullet.color:
                    bullets.pop(bullets.index(bullet))
                    balls[30+e-1] = target(bullet.x, 250, 0, (255, 255, 255))
                    kill += 1
                    if e == 1:
                        r.execute(f"UPDATE second SET one = '(255, 255, 255)' WHERE id = '3'")
                    elif e == 2:
                        r.execute(f"UPDATE second SET two = '(255, 255, 255)' WHERE id = '3'")
                    elif e == 3:
                        r.execute(f"UPDATE second SET three = '(255, 255, 255)' WHERE id = '3'")
                    elif e == 4:
                        r.execute(f"UPDATE second SET four = '(255, 255, 255)' WHERE id = '3'")
                    elif e == 5:
                        r.execute(f"UPDATE second SET five = '(255, 255, 255)' WHERE id = '3'")
                    elif e == 6:
                        r.execute(f"UPDATE second SET six = '(255, 255, 255)' WHERE id = '3'")
                    elif e == 7:
                        r.execute(f"UPDATE second SET seven = '(255, 255, 255)' WHERE id = '3'")
                    elif e == 8:
                        r.execute(f"UPDATE second SET eight = '(255, 255, 255)' WHERE id = '3'")
                    elif e == 9:
                        r.execute(f"UPDATE second SET nine = '(255, 255, 255)' WHERE id = '3'")
                    elif e == 10:
                        r.execute(f"UPDATE second SET ten = '(255, 255, 255)' WHERE id = '3'")
                    elif e == 11:
                        r.execute(f"UPDATE second SET eleven = '(255, 255, 255)' WHERE id = '3'")
                    elif e == 12:
                        r.execute(f"UPDATE second SET twelve = '(255, 255, 255)' WHERE id = '3'")
                    elif e == 13:
                        r.execute(f"UPDATE second SET thirteen = '(255, 255, 255)' WHERE id = '3'")
                    elif e == 14:
                        r.execute(f"UPDATE second SET fourteen = '(255, 255, 255)' WHERE id = '3'")
                    else:
                        r.execute(f"UPDATE second SET fifteen = '(255, 255, 255)' WHERE id = '3'")
                    connection2.commit()
                else:
                    r.execute(f"SELECT * FROM second WHERE id = 3")
                    result = r.fetchall()
                    itog = result[0][e]
                    connection2.commit()
                    if checking(itog) == (255, 255, 255):
                        if bullet.y <= 190:
                            r.execute(f"SELECT * FROM second WHERE id = 2")
                            result = r.fetchall()
                            itog = result[0][e]
                            connection2.commit()
                            if checking(itog) == bullet.color:
                                bullets.pop(bullets.index(bullet))
                                balls[15 + e - 1] = target(bullet.x, 190, 0, (255, 255, 255))
                                kill += 1
                                if e == 1:
                                    r.execute(f"UPDATE second SET one = '(255, 255, 255)' WHERE id = '2'")
                                elif e == 2:
                                    r.execute(f"UPDATE second SET two = '(255, 255, 255)' WHERE id = '2'")
                                elif e == 3:
                                    r.execute(f"UPDATE second SET three = '(255, 255, 255)' WHERE id = '2'")
                                elif e == 4:
                                    r.execute(f"UPDATE second SET four = '(255, 255, 255)' WHERE id = '2'")
                                elif e == 5:
                                    r.execute(f"UPDATE second SET five = '(255, 255, 255)' WHERE id = '2'")
                                elif e == 6:
                                    r.execute(f"UPDATE second SET six = '(255, 255, 255)' WHERE id = '2'")
                                elif e == 7:
                                    r.execute(f"UPDATE second SET seven = '(255, 255, 255)' WHERE id = '2'")
                                elif e == 8:
                                    r.execute(f"UPDATE second SET eight = '(255, 255, 255)' WHERE id = '2'")
                                elif e == 9:
                                    r.execute(f"UPDATE second SET nine = '(255, 255, 255)' WHERE id = '2'")
                                elif e == 10:
                                    r.execute(f"UPDATE second SET ten = '(255, 255, 255)' WHERE id = '2'")
                                elif e == 11:
                                    r.execute(f"UPDATE second SET eleven = '(255, 255, 255)' WHERE id = '2'")
                                elif e == 12:
                                    r.execute(f"UPDATE second SET twelve = '(255, 255, 255)' WHERE id = '2'")
                                elif e == 13:
                                    r.execute(f"UPDATE second SET thirteen = '(255, 255, 255)' WHERE id = '2'")
                                elif e == 14:
                                    r.execute(f"UPDATE second SET fourteen = '(255, 255, 255)' WHERE id = '2'")
                                else:
                                    r.execute(f"UPDATE second SET fifteen = '(255, 255, 255)' WHERE id = '2'")
                                connection2.commit()
                            else:
                                r.execute(f"SELECT * FROM second WHERE id = 2")
                                result = r.fetchall()
                                itog = result[0][e]
                                connection2.commit()
                                if checking(itog) == (255, 255, 255):
                                    if bullet.y <= 130:
                                        r.execute(f"SELECT * FROM second WHERE id = 1")
                                        result = r.fetchall()
                                        itog = result[0][e]
                                        connection2.commit()
                                        if checking(itog) == bullet.color:
                                            bullets.pop(bullets.index(bullet))
                                            balls[e - 1] = target(bullet.x, 130, 0, (255, 255, 255))
                                            kill += 1
                                            if e == 1:
                                                r.execute(f"UPDATE second SET one = '(255, 255, 255)' WHERE id = '1'")
                                            elif e == 2:
                                                r.execute(f"UPDATE second SET two = '(255, 255, 255)' WHERE id = '1'")
                                            elif e == 3:
                                                r.execute(f"UPDATE second SET three = '(255, 255, 255)' WHERE id = '1'")
                                            elif e == 4:
                                                r.execute(f"UPDATE second SET four = '(255, 255, 255)' WHERE id = '1'")
                                            elif e == 5:
                                                r.execute(f"UPDATE second SET five = '(255, 255, 255)' WHERE id = '1'")
                                            elif e == 6:
                                                r.execute(f"UPDATE second SET six = '(255, 255, 255)' WHERE id = '1'")
                                            elif e == 7:
                                                r.execute(f"UPDATE second SET seven = '(255, 255, 255)' WHERE id = '1'")
                                            elif e == 8:
                                                r.execute(f"UPDATE second SET eight = '(255, 255, 255)' WHERE id = '1'")
                                            elif e == 9:
                                                r.execute(f"UPDATE second SET nine = '(255, 255, 255)' WHERE id = '1'")
                                            elif e == 10:
                                                r.execute(f"UPDATE second SET ten = '(255, 255, 255)' WHERE id = '1'")
                                            elif e == 11:
                                                r.execute(
                                                    f"UPDATE second SET eleven = '(255, 255, 255)' WHERE id = '1'")
                                            elif e == 12:
                                                r.execute(
                                                    f"UPDATE second SET twelve = '(255, 255, 255)' WHERE id = '1'")
                                            elif e == 13:
                                                r.execute(
                                                    f"UPDATE second SET thirteen = '(255, 255, 255)' WHERE id = '1'")
                                            elif e == 14:
                                                r.execute(
                                                    f"UPDATE second SET fourteen = '(255, 255, 255)' WHERE id = '1'")
                                            else:
                                                r.execute(
                                                    f"UPDATE second SET fifteen = '(255, 255, 255)' WHERE id = '1'")
                                            connection2.commit()
                                        else:
                                            bullet.y -= bullet.speed
                                    else:
                                        bullet.y -= bullet.speed
                                else:
                                    bullet.y -= bullet.speed
                        else:
                            bullet.y -= bullet.speed
                    else:
                        bullet.y -= bullet.speed
            else: bullet.y -= bullet.speed
        else:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()

    ''' Функция if, требуемая для отображения строки с цветами последующих шариков '''

    if keys[pygame.K_SPACE]:
        if len(bullets) < 1:
            if a == 1:
                color = (255, 0, 0)
                a1 = (0, 255, 0)
                a2 = (0, 0, 255)
                a3 = (255, 255, 0)
                a4 = (0, 255, 255)
                a5 = (255, 0, 255)
                a6 = (255, 0, 0)
                a = 2
            elif a == 2:
                color = (0, 255, 0)
                a6 = (0, 255, 0)
                a1 = (0, 0, 255)
                a2 = (255, 255, 0)
                a3 = (0, 255, 255)
                a4 = (255, 0, 255)
                a5 = (255, 0, 0)
                a = 3
            elif a == 3:
                color = (0, 0, 255)
                a5 = (0, 255, 0)
                a6 = (0, 0, 255)
                a1 = (255, 255, 0)
                a2 = (0, 255, 255)
                a3 = (255, 0, 255)
                a4 = (255, 0, 0)
                a = 4
            elif a == 4:
                color = (255, 255, 0)
                a4 = (0, 255, 0)
                a5 = (0, 0, 255)
                a6 = (255, 255, 0)
                a1 = (0, 255, 255)
                a2 = (255, 0, 255)
                a3 = (255, 0, 0)
                a = 5
            elif a == 5:
                color = (0, 255, 255)
                a3 = (0, 255, 0)
                a4 = (0, 0, 255)
                a5 = (255, 255, 0)
                a6 = (0, 255, 255)
                a1 = (255, 0, 255)
                a2 = (255, 0, 0)
                a = 6
            else:
                color = (255, 0, 255)
                a2 = (0, 255, 0)
                a3 = (0, 0, 255)
                a4 = (255, 255, 0)
                a5 = (0, 255, 255)
                a6 = (255, 0, 255)
                a1 = (255, 0, 0)
                a = 1
            bullets.append(shell(round(x + width // 2), round(y + height // 2), 20, color))
            rects = [rect(420, 10, 20, 20, a1), rect(445, 10, 20, 20, a2), rect(470, 10, 20, 20, a3), rect(495, 10, 20, 20, a4), rect(520, 10, 20, 20, a5), rect(545, 10, 20, 20, a6)]

    ''' Передвижение пушки нажатиями стрелочек '''

    if keys[pygame.K_LEFT] and x > speed + 50:
        x -= speed
    if keys[pygame.K_RIGHT] and x < 1100 - width - 55:
        x += speed

    ''' Функция Pygame для обновления/отрисовки окна. Т.е. она отображает всё, что вы прописани выше '''

    drawWindow()