"""Drill 14 실행 진입점. 작업 폴더와 무관하게 이 파일을 실행한다."""

from pico2d import close_canvas, open_canvas

import game_framework
import play_mode
from config import CANVAS_HEIGHT, CANVAS_WIDTH


def main():
    open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    try:
        game_framework.run(play_mode)
    finally:
        close_canvas()


if __name__ == '__main__':
    main()
