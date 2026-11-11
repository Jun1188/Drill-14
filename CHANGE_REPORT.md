# 전체 변경 대조와 단계별 개발 기록

## 작업 경계

작업 시작 시 `Drill-14` 폴더는 없었다. 이 문서의 before는 모든 파일에 대해 **없음**이다.
기존 labs와 다른 DRILL은 수정하지 않았다. 같은 부모 폴더 아래 새 독립 저장소만 만들었다.
수업 소스의 참고·복사와 이번 폴더의 before/after를 구분한다.
아래 코드는 이 문서를 작성하는 시점의 전체 원문이다. 게임 실행·테스트 결과를 의미하지 않는다.

## 단계별 커밋

단계 01~20은 다음 실제 커밋에 대응한다. 단계 21은 이 문서를 추가한 커밋이고, 단계 22는 PRD 완료 상태와 ANIMATION_LOGIC.md를 포함한 마지막 커밋이다.
각 커밋의 전체 차이는 `git show <해시>`로 볼 수 있다. 최종 상세 구현 설명은 `git log -1 --format=%B`로 읽는다.

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
```

## 수업 코드에서 바꾼 점

- `game_world.py`: LEC16의 계층형 목록, 복사 순회, 삭제, clear를 재사용했다. 오타 API `add_oject`를 `add_object`로 통일하고 새 호출부에서도 같은 이름을 사용한다.
- `game_framework.py`: 모드 수명 구조를 재사용했다. `time.time()` 대신 단조 시계 `time.perf_counter()`를 사용하고, 현재 프레임의 경과 시간을 update 전에 계산한다. 사용하지 않는 `1 / frame_time` 계산을 제거하여 0초 분모를 없앴다. 종료 입력 뒤에는 update/render에 진입하지 않는다.
- `main.py`: 수업과 같은 1600×600 캔버스, play_mode 시작. finally로 캔버스 종료를 보장한다.
- `play_mode.py`: Boy/Grass 대신 Bird 10개를 등록한다. 수업의 월드 갱신·그리기·0.01초 delay 방식을 따른다. 종료 시 월드와 공유 이미지 참조를 해제한다.
- `bird.py`: 수업 Boy의 시간 기반 애니메이션과 이동 개념을 재사용한다. PNG 14개 좌표, 1회 이미지 로드, 새별 상태, 경계 반사와 좌우 반전을 적용한다.
- 이미지와 코드의 경로는 실행 시 부모 labs에 의존하지 않는다.

## 입력 → 상태/변환 → 출력

1. `main()`에서 캔버스를 연 뒤 프레임워크를 시작한다.
2. `play_mode.init()`가 각 새의 x/y, 날갯짓 위상과 오른쪽 방향을 설정한다. PNG는 최초 Bird 생성 때만 로드한다.
3. 프레임워크가 경과 시간 dt를 구하고 종료 이벤트를 처리한다.
4. 월드가 각 새의 update를 호출한다. 프레임은 `(기존 프레임 + 14 × dt) % 14`, 위치는 `x + 방향 × 277.78 × dt`로 갱신한다.
5. 좌우 한계를 넘으면 초과분을 반사하고 방향을 바꾼다. 긴 프레임은 화면 내부에 들어올 때까지 반복 반사한다.
6. 프레임 정수부를 위→아래 행 순서의 crop 좌표로 바꾼다. draw는 방향에 따라 수평 반전을 선택한다.
7. ESC 또는 창 닫기로 루프를 끝내고 finish 이후 캔버스를 닫는다.

## 전체 before / after

새 코드만 있으므로 파일 전체를 하나의 추가 블록으로 제시한다. binary PNG는 편집하지 않은 원본 복사이며 ASSETS.md에 위치와 크기를 기록했다.
문서 산출물은 PRD.md, ASSETS.md, README.md, MANUAL_CHECKS.md, 이 문서, ANIMATION_LOGIC.md다.

### config.py

단계: 04: 화면, 단위, 주기

**before:** 없음.

**after:**

```python
"""Drill 14의 화면, 단위, 애니메이션 설정."""

CANVAS_WIDTH = 1600
CANVAS_HEIGHT = 600
BIRD_COUNT = 10
DRAW_WIDTH = 120
DRAW_HEIGHT = 110

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

단계: 05: 수업 월드 관리

**before:** 없음.

**after:**

```python
world = [[], [], []]  # 0: 배경, 1: 오브젝트, 2: UI

def add_object(o, depth=1):
    world[depth].append(o)

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

단계: 06~07: 수업 프레임워크와 경과 시간

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

단계: 08~14: 좌표, 공유 이미지, 시간 기반 상태, 반사, 그리기

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

### play_mode.py

단계: 15, 17: 10마리 월드와 이벤트·해제

**before:** 없음.

**after:**

```python
"""LEC16의 play_mode 역할: 새 10마리의 생성, 갱신, 렌더."""

from pico2d import (SDL_KEYDOWN, SDL_QUIT, SDLK_ESCAPE, clear_canvas, delay,
                    get_events, update_canvas)

import game_framework
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


def handle_events():
    for event in get_events():
        if event.type == SDL_QUIT:
            game_framework.quit()
            return
        if event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
            return


def finish():
    game_world.clear()
    # 캔버스가 닫히기 전에 공유 텍스처 참조를 해제한다.
    Bird.image = None


def pause():
    pass


def resume():
    pass
```

### main.py

단계: 16: 캔버스 진입점

**before:** 없음.

**after:**

```python
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
```

### requirements.txt

단계: 18: 의존성 고정

**before:** 없음.

**after:**

```text
pico2d==1.5.1
PySDL2==0.9.17
pysdl2-dll==2.32.10
```

### run.ps1

단계: 18: 실행 인터프리터 선택

**before:** 없음.

**after:**

```powershell
param(
    [string]$Python = (Join-Path $env:LOCALAPPDATA 'Programs\Python\Python313\python.exe')
)

$ErrorActionPreference = 'Stop'
if (-not (Test-Path -LiteralPath $Python -PathType Leaf)) {
    throw 'Python 3.13이 없습니다. -Python 인수로 pico2d가 설치된 실행 파일을 지정하세요.'
}
& $Python (Join-Path $PSScriptRoot 'main.py')
exit $LASTEXITCODE
```

### .vscode/settings.json

단계: 19: 편집기·Code Runner·새 터미널

**before:** 없음.

**after:**

```json
{
    "python.defaultInterpreterPath": "${env:LOCALAPPDATA}/Programs/Python/Python313/python.exe",
    "python.terminal.executeInFileDir": true,
    "terminal.integrated.env.windows": {
        "PATH": "${env:LOCALAPPDATA}/Programs/Python/Python313;${env:LOCALAPPDATA}/Programs/Python/Python313/Scripts;${env:PATH}"
    },
    "code-runner.runInTerminal": true,
    "code-runner.fileDirectoryAsCwd": true,
    "code-runner.executorMap": {
        "python": "& \"$env:LOCALAPPDATA/Programs/Python/Python313/python.exe\" -u"
    },
    "files.encoding": "utf8bom"
}
```

### .vscode/launch.json

단계: 19: F5 디버거

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
            "python": "${env:LOCALAPPDATA}/Programs/Python/Python313/python.exe",
            "program": "${workspaceFolder}/main.py",
            "cwd": "${workspaceFolder}",
            "console": "integratedTerminal"
        }
    ]
}
```

### .gitignore

단계: 02: 생성 파일 제외

**before:** 없음.

**after:**

```gitignore
__pycache__/
*.py[cod]
.venv/
venv/
.pytest_cache/
.vscode/*.log
```

## 사용자 확인과 남은 상태

실행 명령과 실제 확인 항목은 README.md, MANUAL_CHECKS.md를 따른다.
화면에서 10마리·14프레임·양방향 왕복·반전·정상 종료를 확인하는 작업은 사용자가 진행한다.
빌드, 게임 실행, 테스트, 자동 검증기는 실행하지 않았다. 학습 내용의 사용자 이해 확인도 수행하지 않았다.
원격 publish, Public 확인, 원격 파일·커밋 수 확인과 e-Class 제출은 사용자 작업으로 남아 있다.

실행에 필요한 임시·더미 파일은 만들지 않았다. PNG, 문서, 실행 설정과 `.git`은 최종 산출물이다.
