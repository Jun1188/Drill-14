# LEC16 베이스와 리소스

원본 위치: `2DGP-2024184011/Labs/LEC16_Time`.
원본 폴더의 파일 15개를 이 저장소 안에 포함한다. __pycache__는 복사하지 않는다.

| 구분 | 파일 | 보존·수정 |
|---|---|---|
| 소년 | boy.py, animation_sheet.png | 코드 내용과 PNG 유지, 텍스트 BOM·줄바꿈 통일 |
| 공 | ball.py, ball21x21.png, ball41x41.png | 코드 내용과 PNG 유지 |
| 배경 | grass.py, grass.png, ruler.png | 코드 내용과 PNG 유지 |
| 폰트 | ENCR10B.TTF | 원본 바이너리 복사 |
| 새 | bird_animation.png | 918×506, 원본 111,462바이트 그대로 복사 |
| 추가 원본 리소스 | run_animation.png | 원본 폴더 구성을 유지하기 위해 복사 |
| 진입점 | main.py | 코드 폴더를 작업 폴더로 설정, finally에서 캔버스 닫기 |
| 프레임워크 | game_framework.py | 모드 수명 유지, 단조 시계와 현재 프레임 dt 사용 |
| 월드 | game_world.py | 원본 계층형 관리에 새 전용 레이어 추가, API 두 철자 호환 |
| 플레이 모드 | play_mode.py | 소년·배경·입력 유지, 새 10개 등록·공유 참조 해제 추가 |

새 코드는 bird.py, 화면·단위 설정은 config.py다.
source 경로는 출처 설명이며 프로그램이 실행할 때 형제 labs를 읽지는 않는다.
별도 리소스 라이선스 표기는 원본 폴더에서 확인되지 않았다. 수업 과제의 제공 리소스로 사용한다.
