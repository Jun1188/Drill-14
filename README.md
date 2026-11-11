# Drill #14 — 소년과 새 10마리

원본 `Labs/LEC16_Time` 장면을 유지하고 새 전용 레이어를 추가했다.
소년·풀·눈금자·공이 함께 나오며, 작은 새 10마리(60×55)가 14프레임 날갯짓으로 왕복한다.
새 이미지는 실행 중 최초 1회 로드해 공유한다. 원본 labs 폴더는 수정하지 않는다.

## 사용자가 실행

Drill-14 자체를 폴더로 열고 PowerShell에서 실행한다.

```powershell
.\run.ps1
```

이 PC의 기본 인터프리터는 `C:\Users\변준영\AppData\Local\Programs\Python\Python313\python.exe`다.
실행 스크립트·F5·기본 Python·Code Runner·새 터미널에 같은 실제 경로를 지정했다.
LOCALAPPDATA가 빈 문자열로 치환되어 `/Programs/...`가 되는 경로 오류를 피한다.

다른 PC에서는 run.ps1의 `-Python`과 `.vscode`의 Python 경로를 해당 설치 위치로 바꾼다.

```powershell
.\run.ps1 -Python 'C:\원하는경로\python.exe'
```

필요한 패키지는 requirements.txt의 pico2d·PySDL2·pysdl2-dll·transitions다.
기존 환경에 없을 때만 사용자가 설치한다. Codex는 설치·실행하지 않았다.

```powershell
& 'C:\Users\변준영\AppData\Local\Programs\Python\Python313\python.exe' -m pip install -r .\requirements.txt
```

VS Code는 Python: Select Interpreter에서 위 실행 파일을 직접 선택한 뒤 Developer: Reload Window를 실행한다.
F5 구성은 `Drill-14: Python 3.13 (pico2d)`다. 기존 터미널은 닫고 새로 연다.
부모 폴더를 열면 Drill-14 하위 .vscode 설정이 자동 적용된다고 가정하지 않는다.

## 조작과 장면

- 좌우 방향키: 원본 소년 이동.
- Space: 깨어 있을 때 공 발사. 5초 대기 후 잠들면 Space로 기상.
- ESC 또는 X: 종료.
- 새: 자동 비행. 소년과 별개 상태로 움직이며 방향 전환 시 이미지도 수평 반전한다.

계층은 `0 배경(풀·눈금자) → 1 소년·공 → 2 새 10마리 → 3 UI`다.

## 파일 구성

원본 LEC16의 main, game_framework, game_world, play_mode 구조와 boy.py, ball.py, grass.py를 사용한다.
모든 원본 PNG와 ENCR10B.TTF를 내부에 포함한다. 이미지·폰트를 부모 labs에서 읽지 않는다.
추가 파일은 bird.py, config.py, 실행 설정, PRD와 설명 문서다.

- PRD.md: 요구사항과 확인 상태.
- ASSETS.md: 원본 코드·리소스와 보존 범위.
- ANIMATION_LOGIC.md: 최종 커밋 본문에도 포함한 상세 논리.
- CHANGE_REPORT.md: 실제 개발 커밋과 전체 소스 before/after.
- MANUAL_CHECKS.md: 소년·새·입력·종료를 사용자가 확인할 절차.

## 사용자가 원격 publish와 제출

1. 부모 폴더가 아닌 Drill-14 자체 저장소를 별도 Public GitHub 저장소로 publish한다.
2. GitHub 웹에서 PRD.md, 모든 Python 코드, 이미지·폰트와 26개 개발 커밋을 확인한다. squash하지 않는다.
3. 가장 마지막 커밋 본문의 상세 구현 설명도 확인한다.
4. e-Class 과제 안내의 수업 시간·마감·제출 자료를 확인하고 저장소 URL 등을 제출한다.
5. 실제 제출 결과를 확인한다. 제공 사진에는 마감 시각이 없다.

로컬 커밋 확인: `git rev-list --count HEAD`, 상세 본문: `git log -1 --format=%B`.
게임 실행·테스트는 사용자 확인 대기다. 원격 publish·Public 확인·e-Class 제출은 수행하지 않았다.
