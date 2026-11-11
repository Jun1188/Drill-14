# 리소스와 수업 코드 출처

- `bird_animation.png`: `2DGP-2024184011/Labs/LEC16_Time/bird_animation.png` 원본 복사. 918×506, 111,462바이트. 편집하지 않는다.
- 이미지의 사용 목적은 수업 Drill #14 구현이다. 원본의 별도 라이선스 표기는 이 폴더에서 확인되지 않았다.
- `game_framework.py`, `game_world.py`: 같은 lec16의 모드 실행기와 3계층 월드를 참고·재사용한다.
- `main.py`, `play_mode.py`: lec16의 초기화→이벤트→갱신→렌더→종료 호출 순서를 따른다.
- `bird.py`: lec16 `boy.py`의 `초당 프레임 × frame_time`, `방향 × 초당 픽셀 × frame_time` 방식을 새 이미지에 맞게 작성한다.
- 캐릭터·공·풀·눈금자·폰트와 transitions 의존성은 사용하지 않는다.

이 문서의 원본 경로는 출처 설명이다. 프로그램은 형제 폴더를 읽지 않고 이 저장소 내부 PNG만 사용한다.
