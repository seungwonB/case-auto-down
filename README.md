# 판결문 자동 검색, 다운로드 by python

순서

1. mainCrawler.py
판결문 사이트에서 원하는 법령의 판결문들을 엑셀에 저장하는 것이다.
현재 ui 상에서는 작동을 하지 않으므로 마지막줄에 해당 함수의 매개변수에 정보를 저장한다.
ex) main_Cralwer("홍길동", "901101", "1234567", "형법 제250조")
입력한 법령에 해당하는 판결문들의 정보(날짜, 사건번호, 법원)이 엑셀에 저장된다.

2. 수작업 엑셀정리
크롤링하여 저장된 데이터들 사이사이 빈 셀들이 존재한다.
이들을 제거 하는 것이다.
![image](https://user-images.githubusercontent.com/73030613/138045215-1ab2c7b7-0d04-4317-a9fc-b3952fff3a6e.png)

3. 수작업 데이터 필터링
엑셀에서 필요한 데이터들만 필터링한다.

4. pocket.py
엑셀 데이터를 토대로 판결문들을 장바구니에 담는다.
![image](https://user-images.githubusercontent.com/73030613/138045383-5b26140a-2626-42ae-a970-1f005ff67986.png)

5. 수작업 결제
<br>
6. receipt.py
결제한 판결문의 영수증을 다운로드 한다.
![image](https://user-images.githubusercontent.com/73030613/138045616-477cae54-b18f-4010-9181-82dc60d53804.png)

7. download.py
결제한 판결문, 기록목록, 증거목록을 다운로드 한다.
 
