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
