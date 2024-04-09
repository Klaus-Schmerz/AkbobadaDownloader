## About
악보바다의 악보들을 자동으로 다운로드합니다.

## Installation
```
git clone https://github.com/Klaus-Schmerz/AkbobadaDownloader.git
```

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
* -v, --vpn  
  프록시를 사용해 아이피 차단을 방지합니다. 아이디가 3개 이상일 때부터 같이 사용해 주는 게 좋습니다.
  <br/><br/>
* For example:
```
python main.py -m append "악보바다 ID"
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

