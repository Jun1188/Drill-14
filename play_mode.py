from pico2d import *
import game_world
import game_framework
from boy import Boy
from grass import Grass
from bird import Bird
from config import BIRD_COUNT, CANVAS_HEIGHT, CANVAS_WIDTH, FRAME_COUNT

boy = None


def handle_events():


    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
            return
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            boy.handle_event(event)


def init():
    global boy

    game_world.clear()
    boy = Boy()
    game_world.add_oject(boy, game_world.OBJECTS)

    grass = Grass()
    game_world.add_oject(grass, game_world.BACKGROUND)

    for index in range(BIRD_COUNT):
        row, column = divmod(index, 5)
        x = (column + 1) * CANVAS_WIDTH / 6
        y = (row + 1) * CANVAS_HEIGHT / 3 + (column - 2) * 12
        frame = index * FRAME_COUNT / BIRD_COUNT
        game_world.add_oject(Bird(x, y, frame), game_world.BIRDS)


def pause():
    boy.pause()


def resume():
    pass


def finish():
    global boy
    game_world.clear()
    boy = None
    Bird.image = None


def update():
    game_world.update()
    delay(0.01)  # 0.01초마다 업데이트, 100fps로 동작하게 됨

def render():
    clear_canvas()
    game_world.render()
    update_canvas()
