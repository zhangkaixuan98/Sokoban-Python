import copy
import sys
import pygame
from pygame import *

pygame.mixer.init()

IMG_SKIN = ['images/skin1.png',
            'images/skin2.png',
            'images/skin4.png',
            'images/skin5.png',
            'images/skin6.png',
            'images/skin7.png']

MUSIC = 'move.wav'
ME_DOWN = 'me_down.wav'

SKIN_SIZE = 60
SKIN = 0

FONT_SIZE = 24

WALL = 1
BLANK = 0
DOCK = 2
BOX = 3
WORKER = 4
BOX_DOCKED = 5
WORKER_DOCKED = 6

NEW_PASS = 0


class game_info:
    def __init__(self):
        self.level = 0

        self.step = 0


SIZE = WIDTH, HEIGHT = 800, 600
BACKGROUND = 250, 250, 250
TITLE = 'Sokoban'
FullScreen = 0

pygame.init()
# 窗口大小
screen = pygame.display.set_mode(SIZE, 0, 32)
# 背景颜色
screen.fill(BACKGROUND)
# 标题
pygame.display.set_caption(TITLE)


def game(PASS, SKIN):
    map = copy.deepcopy(MAP[PASS])
    screen.fill(BACKGROUND)
    # 图片
    try:
        skin = pygame.image.load(IMG_SKIN[SKIN]).convert()
    except:
        print('加载图片失败')

    font = pygame.font.SysFont("arial", 24)
    back = font.render('BACK', True, (0, 0, 0))
    replay = font.render('REPLAY', True, (0, 0, 0))
    next_pass = font.render('NEXT', True, (0, 0, 0))
    last_pass = font.render('LAST', True, (0, 0, 0))
    change_skin = font.render('SKIN', True, (0, 0, 0))
    if not move_stack.is_empty():
        move_stack.clear()
    while True:
        for event in pygame.event.get():
            # 退出
            if event.type == QUIT:
                sys.exit()
            # 键盘有按下？
            if event.type == KEYDOWN:
                if event.key == K_BACKSPACE:
                    if not move_stack.is_empty():
                        [move_x, move_y, box_moved] = move_stack.pop()
                        [x, y] = undo(map, x, y, move_x, move_y, box_moved)
                elif event.key == K_LEFT:
                    [x, y] = move(map, x, y, 0, -1)
                elif event.key == K_RIGHT:
                    [x, y] = move(map, x, y, 0, 1)
                elif event.key == K_UP:
                    [x, y] = move(map, x, y, -1, 0)
                elif event.key == K_DOWN:
                    [x, y] = move(map, x, y, 1, 0)
            elif event.type == MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed():
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    # back
                    if ((WIDTH - HEIGHT) / 2 - 30) < mouse_x < ((WIDTH - HEIGHT) / 2 + 30) and (
                            HEIGHT * 1 / 6) < mouse_y < (HEIGHT * 1 / 6 + FONT_SIZE):
                        return 0
                    # replay
                    if ((WIDTH - HEIGHT) / 2 - 30) < mouse_x < ((WIDTH - HEIGHT) / 2 + 30) and (
                            HEIGHT * 2 / 6) < mouse_y < (HEIGHT * 2 / 6 + FONT_SIZE):
                        game(PASS, SKIN)
                    # next_pass
                    if ((WIDTH - HEIGHT) / 2 - 30) < mouse_x < ((WIDTH - HEIGHT) / 2 + 30) and (
                            HEIGHT * 3 / 6) < mouse_y < (HEIGHT * 3 / 6 + FONT_SIZE):
                        if PASS + 1 < 5:
                            game(PASS + 1, SKIN)
                        else:
                            game(PASS, SKIN)
                    # last_pass
                    if ((WIDTH - HEIGHT) / 2 - 30) < mouse_x < ((WIDTH - HEIGHT) / 2 + 30) and (
                            HEIGHT * 4 / 6) < mouse_y < (HEIGHT * 4 / 6 + FONT_SIZE):
                        if PASS - 1 >= 0:
                            game(PASS - 1, SKIN)
                        else:
                            game(PASS, SKIN)
                    # skin
                    if ((WIDTH - HEIGHT) / 2 - 30) < mouse_x < ((WIDTH - HEIGHT) / 2 + 30) and (
                            HEIGHT * 5 / 6) < mouse_y < (HEIGHT * 5 / 6 + FONT_SIZE):
                        if (SKIN + 1) == 6:
                            SKIN = 0
                        else:
                            SKIN += 1
                        skin = pygame.image.load(IMG_SKIN[SKIN]).convert()
                    print(mouse_x, mouse_y)
            screen.fill(BACKGROUND)
            # 字体
            screen.blit(back, ((WIDTH - HEIGHT) / 2 - 30, HEIGHT * 1 / 6))
            screen.blit(replay, ((WIDTH - HEIGHT) / 2 - 30, HEIGHT * 2 / 6))
            screen.blit(next_pass, ((WIDTH - HEIGHT) / 2 - 30, HEIGHT * 3 / 6))
            screen.blit(last_pass, ((WIDTH - HEIGHT) / 2 - 30, HEIGHT * 4 / 6))
            screen.blit(change_skin, ((WIDTH - HEIGHT) / 2 - 30, HEIGHT * 5 / 6))
            is_dock = 1
            is_worker_dock = 1
            # 地图
            for i in range(0, 10):
                for j in range(0, 10):
                    if map[i][j] == BLANK:
                        screen.blit(skin, (j * SKIN_SIZE + 200, i * SKIN_SIZE),
                                    (0 * SKIN_SIZE, 0 * SKIN_SIZE, 1 * SKIN_SIZE, 1 * SKIN_SIZE))
                    elif map[i][j] == WALL:
                        screen.blit(skin, (j * SKIN_SIZE + 200, i * SKIN_SIZE),
                                    (2 * SKIN_SIZE, 2 * SKIN_SIZE, 1 * SKIN_SIZE, 1 * SKIN_SIZE))
                    elif map[i][j] == DOCK:
                        is_dock = 0
                        screen.blit(skin, (j * SKIN_SIZE + 200, i * SKIN_SIZE),
                                    (0 * SKIN_SIZE, 1 * SKIN_SIZE, 1 * SKIN_SIZE, 2 * SKIN_SIZE))
                    elif map[i][j] == BOX:
                        screen.blit(skin, (j * SKIN_SIZE + 200, i * SKIN_SIZE),
                                    (2 * SKIN_SIZE, 0 * SKIN_SIZE, 3 * SKIN_SIZE, 1 * SKIN_SIZE))
                    elif map[i][j] == WORKER:
                        x = i
                        y = j
                        screen.blit(skin, (j * SKIN_SIZE + 200, i * SKIN_SIZE),
                                    (1 * SKIN_SIZE, 0 * SKIN_SIZE, 2 * SKIN_SIZE, 1 * SKIN_SIZE))
                    elif map[i][j] == BOX_DOCKED:
                        screen.blit(skin, (j * SKIN_SIZE + 200, i * SKIN_SIZE),
                                    (2 * SKIN_SIZE, 1 * SKIN_SIZE, 3 * SKIN_SIZE, 2 * SKIN_SIZE))
                    elif map[i][j] == WORKER_DOCKED:
                        is_worker_dock = 0
                        screen.blit(skin, (j * SKIN_SIZE + 200, i * SKIN_SIZE),
                                    (1 * SKIN_SIZE, 1 * SKIN_SIZE, 2 * SKIN_SIZE, 2 * SKIN_SIZE))
            # 刷新
            pygame.display.update()
            if is_dock and is_worker_dock:
                pygame.time.wait(1000)
                if PASS + 1 < 5:
                    game(PASS + 1, SKIN)


map1 = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 1, 2, 1, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 3, 3, 0, 2, 1, 0],
    [0, 1, 2, 3, 4, 0, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 3, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 2, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

map2 = [
    [0, 0, 0, 0, 1, 1, 1, 1, 1, 0],
    [1, 1, 1, 1, 1, 0, 4, 0, 1, 0],
    [1, 0, 0, 1, 1, 3, 3, 0, 1, 0],
    [1, 0, 0, 0, 0, 0, 3, 0, 1, 0],
    [1, 0, 0, 0, 1, 1, 1, 1, 1, 0],
    [1, 1, 1, 0, 1, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 1, 1, 1, 0, 0, 0],
    [0, 1, 0, 2, 2, 2, 1, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

map3 = [
    [0, 1, 1, 1, 1, 0, 0, 0, 0, 0],
    [1, 1, 0, 0, 1, 1, 1, 0, 0, 0],
    [1, 2, 2, 4, 3, 0, 1, 0, 0, 0],
    [1, 2, 2, 0, 1, 0, 1, 0, 0, 0],
    [1, 1, 1, 3, 1, 0, 1, 0, 0, 0],
    [1, 0, 0, 0, 1, 0, 1, 0, 0, 0],
    [1, 0, 3, 0, 0, 0, 1, 0, 0, 0],
    [1, 0, 0, 3, 0, 1, 1, 0, 0, 0],
    [1, 1, 1, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 1, 1, 1, 1, 0, 0, 0, 0]
]

map4 = [
    [0, 1, 1, 1, 1, 1, 1, 0, 0, 0],
    [0, 1, 0, 4, 0, 1, 1, 1, 0, 0],
    [1, 1, 0, 2, 0, 0, 0, 1, 0, 0],
    [1, 2, 0, 3, 2, 3, 0, 1, 0, 0],
    [1, 1, 3, 1, 0, 1, 1, 1, 0, 0],
    [0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

map5 = [
    [0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
    [1, 1, 1, 0, 0, 1, 1, 1, 0, 0],
    [1, 0, 2, 2, 0, 3, 2, 1, 0, 0],
    [1, 0, 0, 3, 3, 0, 4, 1, 0, 0],
    [1, 1, 1, 1, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 1, 1, 1, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

MAP = [map1, map2, map3, map4, map5]


class Stack(object):
    # 初始化栈为空列表
    def __init__(self):
        self.items = []

    # 判断栈是否为空，返回布尔值
    def is_empty(self):
        return self.items == []

    # 返回栈顶元素
    def top(self):
        return self.items[len(self.items) - 1]

    # 返回栈的大小
    def size(self):
        return len(self.items)

    # 把新的元素堆进栈里面
    def push(self, item):
        self.items.append(item)

    # 把栈顶元素丢出去
    def pop(self):
        item = self.items[len(self.items) - 1]
        del self.items[len(self.items) - 1]
        return item

    # 清空栈
    def clear(self):
        self.items = []


def move(map, x, y, move_x, move_y):
    music = pygame.mixer.Sound(MUSIC)
    me_down = pygame.mixer.Sound(ME_DOWN)
    # X边空白
    if map[x + move_x][y + move_y] == BLANK:
        music.play()
        # 小人带有标记
        if map[x][y] == WORKER_DOCKED:
            # 小人原位置改为标记
            map[x][y] = DOCK
        # 小人不带标记
        else:
            # 小人原位置改为空白
            map[x][y] = BLANK
        x += move_x
        y += move_y
        # 小人左移
        map[x][y] = WORKER
        move_stack.push([move_x, move_y, 0])

    # X边标记 小人将带有标记
    elif map[x + move_x][y + move_y] == DOCK:
        music.play()
        # 小人带有标记
        if map[x][y] == WORKER_DOCKED:
            # 小人原位置改为标记
            map[x][y] = DOCK
        # 小人不带标记
        else:
            # 小人原位置改为空白
            map[x][y] = BLANK
        x += move_x
        y += move_y
        # 小人左移
        map[x][y] = WORKER_DOCKED
        move_stack.push([move_x, move_y, 0])
    # X边有箱子或者标记的箱子
    elif map[x + move_x][y + move_y] == BOX or map[x + move_x][y + move_y] == BOX_DOCKED:
        # X边的X边没有箱子和墙 可移动
        if map[x + 2 * move_x][y + 2 * move_y] != BOX and map[x + 2 * move_x][y + 2 * move_y] != WALL and \
                map[x + 2 * move_x][y + 2 * move_y] != BOX_DOCKED:
            music.play()
            # X边的X边有标记　箱子将带有标记
            if map[x + 2 * move_x][y + 2 * move_y] == DOCK:
                map[x + 2 * move_x][y + 2 * move_y] = BOX_DOCKED
            # X边的X边没有标记
            else:
                map[x + 2 * move_x][y + 2 * move_y] = BOX
            # X边有标记的箱子 小人将带有标记
            if map[x + move_x][y + move_y] == BOX_DOCKED:
                if map[x][y] == WORKER_DOCKED:
                    map[x][y] = DOCK
                else:
                    map[x][y] = BLANK
                x += move_x
                y += move_y
                map[x][y] = WORKER_DOCKED
                move_stack.push([move_x, move_y, 1])
            # X边没有标记的箱子
            else:
                if map[x][y] == WORKER_DOCKED:
                    map[x][y] = DOCK
                else:
                    map[x][y] = BLANK
                x += move_x
                y += move_y
                map[x][y] = WORKER
                move_stack.push([move_x, move_y, 1])
    else:
        me_down.play()
    return x, y


def undo(map, x, y, move_x, move_y, box_moved):
    # 小人当前有标记
    if map[x][y] == WORKER_DOCKED:
        # 上一步推箱子移动了
        if box_moved:
            # 当前箱子带有标记
            if map[x + move_x][y + move_y] == BOX_DOCKED:
                # 小人原位置箱子带标记
                map[x][y] = BOX_DOCKED
                # 箱子原位置变为标记
                map[x + move_x][y + move_y] = DOCK
            # 当前箱子不带有标记
            else:
                # 小人原位置箱子不带标记
                map[x][y] = BOX
                # 箱子原位置变为空白
                map[x + move_x][y + move_y] = BLANK
        # 箱子没移动
        else:
            # 小人原位置改为标记
            map[x][y] = DOCK
    # 小人当前没标记
    else:
        # 上一步推箱子移动了
        if box_moved:
            # 当前箱子带有标记
            if map[x + move_x][y + move_y] == BOX_DOCKED:
                # 箱子原位置变为标记
                map[x + move_x][y + move_y] = DOCK
            # 当前箱子不带有标记
            else:
                # 箱子原位置变为空白
                map[x + move_x][y + move_y] = BLANK
            # 小人原位置变为箱子不带标记
            map[x][y] = BOX
        # 箱子没移动
        else:
            # 小人原位置改为标记
            map[x][y] = BLANK
    x -= move_x
    y -= move_y
    # X边空白
    if map[x][y] == BLANK:
        # 小人X移 小人将不带标记
        map[x][y] = WORKER
    # X边有标记
    else:
        # 小人X移 小人将带标记
        map[x][y] = WORKER_DOCKED

    return x, y


if __name__ == '__main__':
    move_stack = Stack()
    game(NEW_PASS, SKIN)
