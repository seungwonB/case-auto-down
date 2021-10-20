from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import re
import requests
import csv
import openpyxl
import pyautogui
import pyperclip
import datetime

def func_receipt(name, jumin1, jumin2, phone1, phone2):
    # 창 열기
    url = 'https://www.scourt.go.kr/portal/information/finalruling/peruse/peruse_status.jsp'
    driver = webdriver.Chrome()

    driver.get(url)
    driver.maximize_window()

    # 개인정보 동의 클릭
    driver.switch_to.frame('wcdFrame')
    driver.find_element_by_xpath('//*[@id="accept"]').click()

    # 이름
    driver.find_element_by_class_name("mr").send_keys(name)

    # 주민 앞자리
    driver.find_element_by_id("jumin1").send_keys(jumin1)

    # 주민 뒷자리
    driver.find_element_by_id("jumin2").send_keys(jumin2)

    # 실명확인 클릭
    driver.find_element_by_id("auth").click()

    # 결제목록 클릭
    time.sleep(0.5)
    driver.find_element_by_xpath('//*[@id="contants"]/div[1]/ul/li[3]').click()

    time.sleep(0.5)
    # 번호 창으로 이동
    driver.switch_to.window(driver.window_handles[-1])

    # 앞자리 입력
    driver.find_element_by_xpath('//*[@id="tel_second"]').send_keys(phone1)
    # 뒷자리 입력
    driver.find_element_by_xpath('//*[@id="tel_end"]').send_keys(phone2)
    # 확인 클릭
    driver.find_element_by_id("okey").click()
    # 원래 창으로 복귀
    driver.switch_to.window(driver.window_handles[0])
    driver.switch_to.frame('wcdFrame')

    # 원하는 날짜를 적으시오.
    now = datetime.datetime.now()
    nowDate = now.strftime('%Y-%m-%d')
    day = nowDate.replace("-", "")

    # 달력 초기화 and 날짜 입력
    driver.find_element_by_id("beginDateForm").clear()
    driver.find_element_by_id("endDateForm").clear()
    driver.find_element_by_id("beginDateForm").send_keys(day)
    driver.find_element_by_id("endDateForm").send_keys(day)

    # 검색 버튼 클릭
    driver.find_element_by_id("search_btn").click()

    # 결제 갯수 파악하기
    count = driver.find_element_by_class_name("colorNotice").text
    count = count.replace("총","")
    count = count.replace("건","")
    count = int(count)

    x = 712
    y = 753
    if count <= 10:
        for i in range(1, count+1):
            i = i * 2 - 1
            path_name = f'//*[@id="contants"]/div[2]/div[2]/table/tbody/tr[{str(i)}]/td[6]/a[1]/img'
            # 확인서 클릭
            driver.find_element_by_xpath(path_name).click()
            time.sleep(1)
            driver.switch_to.window(driver.window_handles[-1])
            # 출력 클릭
            driver.find_element_by_id("printBtn").click()
            # 인쇄 버튼이 로딩으로 인하여 먹히지 않아 직접적으로 마우스를 움직여 클릭함.
            # x, y 좌표는 pyautogui.position()으로 추출
            pyautogui.moveTo(x, y)
            time.sleep(1)
            # 버튼 클릭
            pyautogui.click()
            time.sleep(1)
            # 파일 이름
            pyperclip.copy("결제"+str(i))
            pyautogui.hotkey('ctrl','v')
            # 저장
            pyautogui.hotkey('alt','s')
            # 현재 창 닫기
            driver.close()