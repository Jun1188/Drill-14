"""LEC16의 play_mode 역할: 새 10마리의 생성, 갱신, 렌더."""

from pico2d import clear_canvas, delay, update_canvas

import game_world
from bird import Bird
from config import BIRD_COUNT, CANVAS_HEIGHT, CANVAS_WIDTH, FRAME_COUNT


def init():
    game_world.clear()
    for index in range(BIRD_COUNT):
        row, column = divmod(index, 5)
        x = (column + 1) * CANVAS_WIDTH / 6
        y = (row + 1) * CANVAS_HEIGHT / 3 + (column - 2) * 12
        frame = index * FRAME_COUNT / BIRD_COUNT
        game_world.add_object(Bird(x, y, frame))


def update():
    game_world.update()
    delay(0.01)


def render():
    clear_canvas()
    game_world.render()
    update_canvas()
