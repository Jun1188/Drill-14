"""LEC16의 시간 기반 이동을 14프레임 새 이미지에 적용한다."""

from pathlib import Path

from pico2d import load_image

import game_framework
from config import (CANVAS_WIDTH, DRAW_HEIGHT, DRAW_WIDTH, FLY_SPEED_PPS,
                    FRAME_COUNT, FRAMES_PER_SECOND, SPRITE_COLUMNS, SPRITE_ROWS)


def frame_rectangle(image, frame):
    """위쪽 행부터 센 프레임을 pico2d의 아래쪽 기준 좌표로 바꾼다."""
    index = int(frame) % FRAME_COUNT
    row, column = divmod(index, SPRITE_COLUMNS)
    left = column * image.w // SPRITE_COLUMNS
    right = (column + 1) * image.w // SPRITE_COLUMNS
    top = row * image.h // SPRITE_ROWS
    bottom = (row + 1) * image.h // SPRITE_ROWS
    return left, image.h - bottom, right - left, bottom - top

class Bird:
    image = None

    def __init__(self, x, y, frame=0.0):
        if Bird.image is None:
            image_path = Path(__file__).resolve().with_name('bird_animation.png')
            Bird.image = load_image(str(image_path))
        self.x = float(x)
        self.y = float(y)
        self.frame = float(frame) % FRAME_COUNT
        self.direction = 1
    def update(self):
        self.frame = (self.frame + FRAMES_PER_SECOND * game_framework.frame_time) % FRAME_COUNT
        self._move(game_framework.frame_time)

    def _move(self, elapsed):
        left = DRAW_WIDTH / 2
        right = CANVAS_WIDTH - DRAW_WIDTH / 2
        self.x += self.direction * FLY_SPEED_PPS * elapsed
        # 초과 거리를 보존하며, 긴 프레임의 여러 차례 경계 통과도 반사한다.
        while self.x < left or self.x > right:
            if self.x > right:
                self.x = 2 * right - self.x
                self.direction = -1
            else:
                self.x = 2 * left - self.x
                self.direction = 1
        if self.x == left:
            self.direction = 1
        elif self.x == right:
            self.direction = -1
