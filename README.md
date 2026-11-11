# Drill #14 — 새 10마리의 왕복 비행

수업 `Labs/LEC16_Time`의 모드 실행기, 월드 관리와 `frame_time` 방식을 참고했다.
10마리가 14프레임 날갯짓을 반복하며 화면 양 끝에서 방향을 바꾼다.
`bird_animation.png` 한 장을 최초 1회 로드해 공유한다.

## 사용자가 실행

이 `Drill-14` 폴더를 독립적으로 열고 PowerShell에서 실행한다.

```powershell
.\run.ps1
```

기본 인터프리터는 `$env:LOCALAPPDATA\Programs\Python\Python313\python.exe`이다.
다른 설치 위치에서는 pico2d가 있는 인터프리터를 지정한다.

```powershell
.\run.ps1 -Python 'C:\원하는경로\python.exe'
```

의존성이 없는 새 환경에서만 사용자가 설치한다. Codex는 설치와 실행을 수행하지 않았다.

```powershell
& "$env:LOCALAPPDATA\Programs\Python\Python313\python.exe" -m pip install -r .\requirements.txt
```

- 창: 1600×600, 새 10마리. ESC 또는 창의 닫기 버튼으로 종료한다.
- `.vscode` 설정은 **Drill-14 자체를 연 경우** 적용한다. 부모 폴더를 열었다면 하위 설정이 자동 적용된다고 가정하지 않는다.
- VS Code에서 `Python: Select Interpreter`로 pico2d가 있는 Python 3.13을 선택한다. 기존 터미널은 닫고 새 터미널을 연다.
- F5는 `Drill-14: Python 3.13 (pico2d)` 구성을 사용한다.
- 이 PC의 VS Code·F5·Code Runner·새 터미널에는 실제 `C:/Users/변준영/AppData/Local/Programs/Python/Python313/python.exe` 경로를 지정했다. 다른 PC에서는 이 설정을 해당 PC의 Python 경로로 바꾼다.
- 디버그 로그의 Python 경로가 `/Programs/...`로 시작하면 환경 변수 치환이 비어 있는 상태다. `Python: Select Interpreter`에서 위 실행 파일을 직접 선택하고 `Developer: Reload Window` 후 F5를 다시 실행한다.
- 실행 파일 경로 기준으로 이미지를 읽으므로 다른 작업 폴더에서도 `main.py`의 전체 경로로 실행할 수 있다.

## 파일과 호출 흐름

`main.py → game_framework.run(play_mode) → init / handle_events / update / render / finish`.
`play_mode.init()`가 `Bird` 10개를 월드에 넣고, `game_world`가 각각 `update()`와 `draw()`를 호출한다.

| 파일 | 역할 |
|---|---|
| PRD.md | 사진 요구사항, 개발 단계, 제출 상태 |
| config.py | 화면, 새 수, 속도 단위와 애니메이션 주기 |
| bird.py | 공유 이미지, 프레임 좌표, 이동, 반사, 좌우 반전 |
| game_framework.py | LEC16 기반 모드 수명과 현재 프레임 경과 시간 |
| game_world.py | LEC16 기반 3계층 오브젝트 관리 |
| play_mode.py | 10마리 생성, 이벤트, 갱신, 렌더, 해제 |
| main.py | 캔버스 생성과 종료 |
| bird_animation.png | LEC16 원본 이미지 |
| ASSETS.md | 리소스와 수업 코드 출처 |
| run.ps1 / requirements.txt / .vscode | 실행 환경 |
| MANUAL_CHECKS.md | 사용자가 수행할 확인 절차 |
| CHANGE_REPORT.md | 전체 코드 before/after와 개발 커밋 대응 |
| ANIMATION_LOGIC.md | 최종 커밋 본문과 함께 읽는 계산·구현 설명 |

## 사용자가 원격 publish

이 폴더는 자체 `.git`을 가진 독립 로컬 저장소다. **부모 폴더가 아닌 Drill-14 저장소**를 publish한다.
원격 Public 저장소 생성, 연결, push는 사용자가 진행한다. 다른 DRILL 저장소를 재사용하지 않는다.

1. VS Code 등의 Publish 기능에서 별도 `Drill-14` 저장소를 **Public**으로 게시한다.
2. GitHub 웹에서 `PRD.md`, `main.py`, 모든 로컬 모듈, `bird_animation.png`의 존재를 확인한다.
3. 최소 20개의 개발 커밋과 **가장 마지막 커밋의 상세 본문**을 원격에서 확인한다. 히스토리를 squash하지 않는다.
4. 공개 저장소 URL을 e-Class 과제 안내에 맞춰 제출한다. 수업 시간과 마감은 e-Class에서 확인한다. 제공 사진에는 시간이 없다.
5. e-Class의 실제 제출 결과를 확인한다.

최종 커밋 설명은 다음 명령으로 로컬에서도 볼 수 있다.

```powershell
git log -1 --format=fuller
git rev-list --count HEAD
```

로컬 작성·커밋과 원격 공개·업로드·e-Class 제출은 서로 다른 완료 상태다.
빌드·게임 실행·테스트는 수행하지 않았다. 사용자가 MANUAL_CHECKS.md를 따라 결과를 확인한다.
