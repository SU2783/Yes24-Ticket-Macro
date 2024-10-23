# Yes24 티켓팅 매크로

⚠️ 해당 매크로를 사용함으로써 발생하는 모든 문제에 대한 책임은 사용자에게 따르며, 본 프로그램의 개발자는 민형사상 책임을 포함한 어떠한 책임도 부담하지 않습니다.        
❌ 상업적 목적으로 이용하는 것을 절대 금합니다.  

--------------------------------------

부모님 나훈아 마지막 콘서트 보내드리려고 만든 매크로.   
업데이트는 (아마도) 없을 예정이니 정상적으로 작동하지 않을 경우 직접 코드를 수정하셔야 합니다.          
_마지막 업데이트 날짜: 2024.10.24_
<br/>
<br/>

## 설치


### pip
```
git clone https://github.com/SU2783/Yes24-Ticket-Macro.git
cd Yes24-Ticket-Macro
pip install -r requirements.txt
```

### poetry
```
git clone https://github.com/SU2783/Yes24-Ticket-Macro.git
cd Yes24-Ticket-Macro
poetry install
```

--------------------------------------

## 사용 방법


```
1. config.py 파일을 열어서 항목 수정
2. python main.py
```

--------------------------------------

## 주의 사항


- 자동 결제는 무통장 입금으로 설정되어 있습니다. 예매 완료 후 반드시 가상계좌로 입금을 진행 해야 최종 예매가 완료됩니다.
- 예매 창에서 step4 수령방법 란의 주문자 정보와 배송지 정보를 미리 입력해 두어야 결제 프로세스가 정상적으로 진행됩니다.

--------------------------------------

## Note


- 첫 실행 시 OCR 모델 다운로드가 진행되기 때문에 시간이 소요될 수 있습니다.

