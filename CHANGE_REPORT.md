# 전체 변경 대조와 실제 개발 기록

최초 작업 전 Drill-14 폴더는 없었다. 아래 전체 파일의 최초 before는 없음이다.
최종 after는 LEC16 소년 장면과 새 레이어를 함께 포함한다. 원본 labs와 다른 DRILL은 수정하지 않았다.
단계 01~23은 초기 구현·인터프리터 수정, 24는 원본 복원, 25는 계층·크기 변경이다.
단계 26은 이 문서의 최종 동기화와 run.ps1 경로 수정 커밋이다.
사용자 기존 python-envs.defaultEnvManager는 아래 현재 설정에 포함되지만 이번 작업의 추가·커밋 항목이 아니다.

## 실제 커밋

```text
a3bb6c3 step 01: define Drill 14 photo requirements and development stages
f268ab3 step 02: exclude Python runtime artifacts from the standalone repository
316a3ab step 03: include the original lec16 bird sheet and source attribution
42c3c03 step 04: define ten birds and time-based flight units
3dca9be step 05: reuse the lec16 layered world with an explicit add_object API
3a16987 step 06: bring in the lec16 mode lifecycle framework
587d710 step 07: sample monotonic frame time before updating the current frame
2e33304 step 08: map fourteen valid frames with top-to-bottom sprite coordinates
0b12727 step 09: own per-bird flight state and share one local image texture
da6a34a step 10: advance wing animation by elapsed seconds instead of render count
b459a55 step 11: translate flight speed into pixels per elapsed second
2697cf0 step 12: reflect overshoot at both visible boundaries without losing distance
1558418 step 13: draw the selected wing frame at the bird position
7bb8980 step 14: mirror the same wing sequence while flying left
c5d1ed1 step 15: populate ten staggered birds and connect the lec16 world loop
3db9be8 step 16: open the lesson-sized canvas and guarantee canvas cleanup
f239d02 step 17: handle Escape and window close and release the shared bird image
7215782 step 18: provide pinned pico2d dependencies and a Python 3.13 launcher
86532f0 step 19: align editor debug runner and new terminals with Python 3.13
61902c0 step 20: document user-run acceptance checks and Public publishing handoff
fcb2473 step 21: record complete source before-after and genuine development commits
c98d2ac step 22: 새 10마리 왕복 비행 완료 및 정확한 애니메이션 구현 논리
54bf22a step 23: fix debugpy WinError 2 by pinning the existing Python 3.13 path
713daff step 24: restore the original lec16 boy grass ball sources and complete assets
ee87aba step 25: keep the lec16 boy scene and add ten smaller birds in their own layer
```

## 후속 수정의 before/after 근거

- 단계 23 수정 전: `git show c98d2ac:.vscode/launch.json` 및 `.vscode/settings.json`.
- 원본 복원 전 전체 상태: `git show 54bf22a:<파일>`.
- 단계 24: `git show 713daff`에서 Boy/Grass/Ball·자산 추가 및 main의 작업 폴더 설정 확인.
- 단계 25: `git show ee87aba`에서 원본 play_mode 유지, 별도 BIRDS 계층과 60×55 확인.
- 전체 후속 차이: `git diff 54bf22a HEAD`.
- 원본 API add_oject를 보존하고 기존 add_object를 별칭으로 유지한다.
- 원본 파일의 위치·보존 범위는 ASSETS.md, 최종 계산과 논리는 ANIMATION_LOGIC.md를 따른다.

## 입력 → 상태/변환 → 출력

main이 코드 폴더를 작업 폴더로 설정하고 캔버스를 연다.
원본 Boy·Grass를 생성한 뒤 별도 계층에 Bird 10개를 등록한다.
원본 소년 입력을 처리하고 각 계층의 update/draw를 순서대로 호출한다.
새는 이미지 1장을 공유하면서 각자의 frame/x/direction을 dt로 갱신하고 경계에서 반사한다.
소년·배경·공 위에 작은 새가 함께 그려진다. 종료 시 월드를 비운 후 캔버스를 닫는다.

## 전체 소스 before/after

각 파일의 before는 최초 생성 기준으로 없음이다. 후속 수정의 중간 before는 위 실제 Git 리비전에서 보존한다.

### config.py

**before:** 없음.

**after:**

```python
"""Drill 14의 화면, 단위, 애니메이션 설정."""

CANVAS_WIDTH = 1600
CANVAS_HEIGHT = 600
BIRD_COUNT = 10
DRAW_WIDTH = 60
DRAW_HEIGHT = 55

SPRITE_COLUMNS = 5
SPRITE_ROWS = 3
FRAME_COUNT = 14
ANIMATION_CYCLE_SECONDS = 1.0
FRAMES_PER_SECOND = FRAME_COUNT / ANIMATION_CYCLE_SECONDS

# LEC16 boy.py와 같은 10픽셀 = 0.3미터 기준을 사용한다.
PIXEL_PER_METER = 10.0 / 0.3
FLY_SPEED_KMPH = 30.0
FLY_SPEED_MPS = FLY_SPEED_KMPH * 1000.0 / 3600.0
FLY_SPEED_PPS = FLY_SPEED_MPS * PIXEL_PER_METER
```

### game_world.py

**before:** 없음.

**after:**

```python
"""LEC16 월드에 새 전용 계층을 추가한다."""

BACKGROUND = 0
OBJECTS = 1
BIRDS = 2
UI = 3
world = [[], [], [], []]


def add_oject(o, depth=OBJECTS):
    world[depth].append(o)


# 원본 LEC16의 호출과 기존 Drill-14의 호출을 모두 유지한다.
add_object = add_oject


def remove_object(o):
    for layer in world:
        if o in layer:
            layer.remove(o)
            return


def update():
    for layer in world:
        for o in layer[:]:
            o.update()


def render():
    for layer in world:
        for o in layer[:]:
            o.draw()


def clear():
    for layer in world:
        layer.clear()
```

### game_framework.py

**before:** 없음.

**after:**

```python
import time
running = False
stack = []
frame_time = 0.0

def change_mode(mode):
    if stack:
        stack.pop().finish()
    stack.append(mode)
    mode.init()


def push_mode(mode):
    if stack:
        stack[-1].pause()
    stack.append(mode)
    mode.init()


def pop_mode():
    if stack:
        stack.pop().finish()
    if stack:
        stack[-1].resume()
    else:
        quit()


def quit():
    global running
    running = False


def run(start_mode):
    global running, stack, frame_time
    frame_time = 0.0
    running = True
    stack = [start_mode]
    try:
        start_mode.init()
        previous_time = time.perf_counter()
        while running:
            current_time = time.perf_counter()
            frame_time = current_time - previous_time
            previous_time = current_time
            stack[-1].handle_events()
            if not running:
                break
            stack[-1].update()
            stack[-1].render()
    finally:
        while stack:
            stack.pop().finish()
        running = False
```

### bird.py

**before:** 없음.

**after:**

```python
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
    def draw(self):
        left, bottom, width, height = frame_rectangle(Bird.image, self.frame)
        flip = 'h' if self.direction < 0 else ''
        Bird.image.clip_composite_draw(
            left, bottom, width, height, 0, flip,
            self.x, self.y, DRAW_WIDTH, DRAW_HEIGHT
        )
```

### boy.py

**before:** 없음.

**after:**

```python
from math import pi

from pico2d import *
from sdl2 import (SDL_KEYDOWN, SDL_KEYUP, SDLK_LEFT, SDLK_RIGHT,
                  SDLK_SPACE)
from transitions import Machine

import game_world
from ball import Ball

import game_framework





class Idle:
    def enter(self, boy):
        boy.idle_started_at = get_time()
        boy.frame = 0

    def do(self, boy):
        if get_time() - boy.idle_started_at >= 5.0:
            boy.fall_asleep()
        else:
            boy.frame = (boy.frame + 1) % 8

    def draw(self, boy):
        row = 300 if boy.face_dir == 1 else 200
        boy.image.clip_draw(boy.frame * 100, row, 100, 100, boy.x, boy.y)

    def space(self, boy):
        boy.fire_ball()

    def move(self, boy):
        boy.start_run()


class Sleep:
    def enter(self, boy):
        boy.frame = 0

    def do(self, boy):
        pass

    def draw(self, boy):
        angle = pi / 2 if boy.face_dir == 1 else -pi / 2
        flip = '' if boy.face_dir == 1 else 'h'
        boy.image.clip_composite_draw(
            boy.frame * 100, 300, 100, 100,
            angle, flip, boy.x, boy.y - 30, 100, 100
        )

    def space(self, boy):
        boy.wake_up()

    def move(self, boy):
        boy.start_run()


class Run:
    def enter(self, boy):
        boy.frame = 0

    def do(self, boy): #게임 - 물리적인 크기, 단위를 정하고 가는 게 중요하다
        PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
        RUN_SPEED_KMPH = 20.0  # Km / Hour
        RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
        RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
        RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER) # Pixel per Second, 게임세계 내에서의 최종 속도 보정

        STRIDE_LENGTH_M = 1.8 # 보폭 길이
        RUN_FRAMES_PER_STRIDE = 5 # 1개 보폭에 대한 애니메이션 프레임 
        # 프레임 증가 속도, 즉 1초당 몇개 프레임을 증가시켜야 하는가? 
        RUN_FRAMES_PER_SECOND = RUN_SPEED_MPS / STRIDE_LENGTH_M * RUN_FRAMES_PER_STRIDE 
        boy.frame = (boy.frame +  RUN_FRAMES_PER_SECOND * game_framework.frame_time) % 8
        boy.x += boy.dir * RUN_SPEED_PPS * game_framework.frame_time
        boy.x = max(25, min(get_canvas_width() - 25, boy.x))

    def draw(self, boy):
        row = 100 if boy.face_dir == 1 else 0
        boy.image.clip_draw(int(boy.frame) * 100, row, 100, 100, boy.x, boy.y)

    def space(self, boy):
        boy.fire_ball()

    def move(self, boy):
        pass


class Boy:
    def __init__(self):
        self.font = load_font('ENCR10B.TTF', 16)
        self.x, self.y = 400, 90
        self.frame = 0
        self.image = load_image('animation_sheet.png')
        self.idle_started_at = get_time()
        self.dir = 0
        self.face_dir = 1
        self.pressed_keys = set()
        self.item = 'Ball'

        self.states = {'IDLE': Idle(), 'SLEEP': Sleep(), 'RUN': Run()}

        self.machine = Machine(
            model=self,
            states=['IDLE', 'SLEEP', 'RUN'],
            transitions=[
                {'trigger': 'fall_asleep',
                 'source': 'IDLE', 'dest': 'SLEEP'},
                {'trigger': 'wake_up',
                 'source': 'SLEEP', 'dest': 'IDLE'},
                {'trigger': 'start_run',
                 'source': ['IDLE', 'SLEEP'], 'dest': 'RUN'},
                {'trigger': 'stop_run',
                 'source': 'RUN', 'dest': 'IDLE'},
            ],
            initial='IDLE',
            auto_transitions=False,
        )

    def on_enter_IDLE(self):
        self.states['IDLE'].enter(self)

    def on_enter_SLEEP(self):
        self.states['SLEEP'].enter(self)

    def on_enter_RUN(self):
        self.states['RUN'].enter(self)

    def fire_ball(self):
        if self.item is None:
            return
        ball = Ball(self.x, self.y, self.face_dir * 10, 1 if self.item == 'Ball' else 2)
        game_world.add_oject(ball)

    def pause(self):
        self.pressed_keys.clear()
        if self.state == 'RUN':
            self.dir = 0
            self.stop_run()

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            self.states[self.state].space(self)
            return

        if (event.type not in (SDL_KEYDOWN, SDL_KEYUP) or
                event.key not in (SDLK_LEFT, SDLK_RIGHT)):
            return

        if event.type == SDL_KEYDOWN:
            self.pressed_keys.add(event.key)
        else:
            self.pressed_keys.discard(event.key)

        direction = (int(SDLK_RIGHT in self.pressed_keys) -
                     int(SDLK_LEFT in self.pressed_keys))

        if direction != 0:
            self.dir = direction
            self.face_dir = direction
            self.states[self.state].move(self)
        elif self.state == 'RUN':
            self.dir = 0
            self.stop_run()

    def update(self):
        self.states[self.state].do(self)

    def draw(self):
        self.states[self.state].draw(self)
        self.font.draw(self.x - 60, self.y + 50, f'(Time: {get_time():.2f}), Frame Time: {game_framework.frame_time:.2f} fps', (255, 255, 255))
```

### ball.py

**before:** 없음.

**after:**

```python
from pico2d import get_canvas_width, load_image

import game_world


class Ball:
    images = {}

    def __init__(self, x, y, velocity, ball_type=1):
        if ball_type not in Ball.images:
            Ball.images[ball_type] = load_image(
                'ball21x21.png' if ball_type == 1 else 'ball41x41.png')
        self.image = Ball.images[ball_type]
        self.x, self.y = x, y
        self.velocity = velocity

    def update(self):
        self.x += self.velocity
        if self.x < 0 or self.x > get_canvas_width():
            game_world.remove_object(self)

    def draw(self):
        self.image.draw(self.x, self.y)
```

### grass.py

**before:** 없음.

**after:**

```python
from pico2d import *

class Grass:
    def __init__(self):
        self.image = load_image('grass.png')
        self.ruler_image = load_image('ruler.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(400, 30)
        self.image.draw(1200, 30)
        self.ruler_image.draw(800, 350)
```

### play_mode.py

**before:** 없음.

**after:**

```python
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
```

### main.py

**before:** 없음.

**after:**

```python
"""Drill 14 실행 진입점. 작업 폴더와 무관하게 이 파일을 실행한다."""

import os
from pathlib import Path

from pico2d import close_canvas, open_canvas

import game_framework
import play_mode
from config import CANVAS_HEIGHT, CANVAS_WIDTH


def main():
    # LEC16의 상대 리소스 경로를 폴더 단독 실행에서도 유지한다.
    os.chdir(Path(__file__).resolve().parent)
    open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    try:
        game_framework.run(play_mode)
    finally:
        close_canvas()


if __name__ == '__main__':
    main()
```

### requirements.txt

**before:** 없음.

**after:**

```text
pico2d==1.5.1
PySDL2==0.9.17
pysdl2-dll==2.32.10
transitions==0.9.3
```

### run.ps1

**before:** 없음.

**after:**

```powershell
param(
    [string]$Python = 'C:\Users\변준영\AppData\Local\Programs\Python\Python313\python.exe'
)

$ErrorActionPreference = 'Stop'
if (-not (Test-Path -LiteralPath $Python -PathType Leaf)) {
    throw 'Python 실행 파일이 없습니다. -Python 인수로 pico2d와 transitions가 설치된 실행 파일을 지정하세요.'
}
& $Python (Join-Path $PSScriptRoot 'main.py')
exit $LASTEXITCODE
```

### .vscode/settings.json

**before:** 없음.

**after:**

```json
{
    "python.defaultInterpreterPath": "C:/Users/변준영/AppData/Local/Programs/Python/Python313/python.exe",
    "python.terminal.executeInFileDir": true,
    "terminal.integrated.env.windows": {
        "PATH": "C:/Users/변준영/AppData/Local/Programs/Python/Python313;C:/Users/변준영/AppData/Local/Programs/Python/Python313/Scripts;${env:PATH}"
    },
    "code-runner.runInTerminal": true,
    "code-runner.fileDirectoryAsCwd": true,
    "code-runner.executorMap": {
        "python": "& \"C:/Users/변준영/AppData/Local/Programs/Python/Python313/python.exe\" -u"
    },
    "files.encoding": "utf8bom",
    "python-envs.defaultEnvManager": "ms-python.python:system"
}
```

### .vscode/launch.json

**before:** 없음.

**after:**

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Drill-14: Python 3.13 (pico2d)",
            "type": "debugpy",
            "request": "launch",
            "python": "C:/Users/변준영/AppData/Local/Programs/Python/Python313/python.exe",
            "program": "${workspaceFolder}/main.py",
            "cwd": "${workspaceFolder}",
            "console": "integratedTerminal"
        }
    ]
}
```

### .gitignore

**before:** 없음.

**after:**

```text
__pycache__/
*.py[cod]
.venv/
venv/
.pytest_cache/
.vscode/*.log
```

## 사용자 확인과 남은 상태

로컬 코드·설정·리소스·문서와 단계별 커밋을 작성했다. 모든 수정 텍스트는 UTF-8 BOM이다.
사용자는 README와 MANUAL_CHECKS를 따라 실행한다. 게임·디버거·빌드·테스트·검증기는 실행하지 않았다.
원격 Public publish·원격 파일와 커밋 수 확인·e-Class 제출은 수행하지 않았다.
기존 사용자 설정 변경은 별도로 남겼다. 기능에 필요 없는 더미·임시 산출물은 만들지 않았다.
