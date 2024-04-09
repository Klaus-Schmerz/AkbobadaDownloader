## About
악보바다의 악보들을 자동으로 다운로드합니다.

## Installation
```
git clone https://github.com/Klaus-Schmerz/AkbobadaDownloader.git
```

## Features
* 아이디와 비밀번호 입력 한 번으로 계정의 모든 악보 다운로드
* 여러개의 아이디를 등록해 실행 한 번으로 여러 계정의 악보 다운로드
* 멀티코어 활용으로 빠른 다운로드
* 새로운 악보를 다운로드할 때, 마지막으로 받았던 악보까지만 다운로드하여 전체 소요시간 단축

## Flaws
* 다운로드 일시정지 기능이 없음
* 실행 파일(.exe/.dmg)로의 변환 한계로 인한 GUI 미지원
* 파이썬 실행환경이 설정되어있어야 함

## How to use
In shell
```
python main.py
```

## Arguments
* -m, --mode  
  "append" - 새로운 아이디를 추가합니다.  
  "delete" - 저장된 아이디 중 입력한 아이디를 삭제합니다.
* -r, --recovery  
  다운로드 도중 프로그램 종료나 오류로 인해 다운로드가 정상적으로 진행되지 않을 경우, 이 옵션을 사용하여 전체를 다시 다운로드할 수 있습니다.
* -p, --proxy  
  프록시를 사용해 아이피 차단을 방지합니다. 아이디가 3개 이상일 때부터는 같이 사용해 주는 게 좋습니다.
  <br/><br/>
* For example:
```
python main.py -m append
```
```
python main.py -r
```
```
python main.py -r -v
```

## Supported OS
Windows  
Mac  
Linux

## Troubleshoot
In windows:
```
DELETE %APPDATA%\Local\skymj\(악보바다 ID)_last.p
```
In Mac or Linux:
```
DELETE ~\.local\share\skymj\(악보바다 ID)_last.p\
```

