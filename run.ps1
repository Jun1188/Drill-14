param(
    [string]$Python = 'C:\Users\변준영\AppData\Local\Programs\Python\Python313\python.exe'
)

$ErrorActionPreference = 'Stop'
if (-not (Test-Path -LiteralPath $Python -PathType Leaf)) {
    throw 'Python 실행 파일이 없습니다. -Python 인수로 pico2d와 transitions가 설치된 실행 파일을 지정하세요.'
}
& $Python (Join-Path $PSScriptRoot 'main.py')
exit $LASTEXITCODE
