"""LEC16의 시간 기반 이동을 14프레임 새 이미지에 적용한다."""

from config import FRAME_COUNT, SPRITE_COLUMNS, SPRITE_ROWS


def frame_rectangle(image, frame):
    """위쪽 행부터 센 프레임을 pico2d의 아래쪽 기준 좌표로 바꾼다."""
    index = int(frame) % FRAME_COUNT
    row, column = divmod(index, SPRITE_COLUMNS)
    left = column * image.w // SPRITE_COLUMNS
    right = (column + 1) * image.w // SPRITE_COLUMNS
    top = row * image.h // SPRITE_ROWS
    bottom = (row + 1) * image.h // SPRITE_ROWS
    return left, image.h - bottom, right - left, bottom - top
