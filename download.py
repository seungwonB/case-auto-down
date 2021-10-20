from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import re
import requests
import bs4
from bs4 import BeautifulSoup
import csv
import openpyxl
import pyautogui
import pyperclip
import datetime

def func_download(name, jumin1, jumin2, phone1, phone2):
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

    # 번호 창으로 이동
    time.sleep(0.5)
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

    now = datetime.datetime.now()
    nowDate = now.strftime('%Y-%m-%d')
    day = nowDate.replace("-", "")

    # 달력 초기화 and 날짜 입력
    def select_day():
        driver.find_element_by_xpath('//*[@id="contants"]/div[1]/ul/li[3]').click()
        driver.find_element_by_id("beginDateForm").clear()
        driver.find_element_by_id("endDateForm").clear()
        driver.find_element_by_id("beginDateForm").send_keys(day)
        driver.find_element_by_id("endDateForm").send_keys(day)
        # 검색 버튼 클릭
        driver.find_element_by_id("search_btn").click()

    # 증거목록 다운로드(1개인 경우와 여러개인 경우 존재)
    def jeng_down():
        i = 0
        try:
            while True:
                jn_name = f'jeng_{str(i)}'
                try:
                    driver.find_element_by_id(jn_name)
                except:
                    break
                i += 1
                driver.find_element_by_id(jn_name).click()
                time.sleep(0.5)
                driver.find_element_by_id("download-btn").click()
        except:
            pass

    # 기록목록 다운로드
    def gi_down():
        i = 0
        try:
            while True:
                gi_name = f'gi_{str(i)}'
                try:
                    driver.find_element_by_id(gi_name)
                except:
                    break
                i += 1
                driver.find_element_by_id(gi_name).click()
                time.sleep(0.5)
                driver.find_element_by_id("download-btn").click()
        except:
            pass


    def repeat_open(cnt):
        for i in range(1, cnt + 1):
            open_xpath = f'/html/body/div[1]/div[2]/div[2]/div[2]/table/tbody/tr[{str(i)}]/td[5]/a/img'

            # 열람하기 클릭
            driver.find_element_by_xpath(open_xpath).click()
            # 열람 창
            time.sleep(0.5)
            driver.switch_to.window(driver.window_handles[-1])
            time.sleep(0.5)
            # 판결문 다운로드
            driver.find_element_by_id("download-btn").click()
            # 증거목록 클릭
            time.sleep(0.5)
            jeng_down()
            time.sleep(0.5)
            gi_down()
            driver.switch_to.window(driver.window_handles[0])
            driver.switch_to.frame('wcdFrame')


    def repeat_open2(cnt, pth):
        for i in range(1, cnt + 1):
            # 2페이지 클릭
            driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div[3]/a').click()

            open_xpath = f'/html/body/div[1]/div[2]/div[2]/div[2]/table/tbody/tr[{str(i)}]/td[5]/a/img'
            # 열람하기 클릭
            driver.find_element_by_xpath(open_xpath).click()
            # 열람 창
            time.sleep(0.5)
            driver.switch_to.window(driver.window_handles[-1])
            time.sleep(0.5)
            # 판결문 다운로드
            driver.find_element_by_id("download-btn").click()
            # 증거목록 클릭
            time.sleep(0.5)
            jeng_down()
            # 기록목록 클릭
            time.sleep(0.5)
            gi_down()
            driver.switch_to.window(driver.window_handles[0])
            driver.switch_to.frame('wcdFrame')
            # 결제목록 클릭
            driver.find_element_by_xpath('//*[@id="contants"]/div[1]/ul/li[3]').click()
            # 날짜 설정
            select_day()
            # 다시 열람 클릭
            time.sleep(0.5)
            print("다시 열람 클릭")
            try:
                driver.find_element_by_xpath(pth).click()
            except:
                pass

    select_day() # 날짜 선택

    for i in range(1, 6):
        # i = i * 2 - 1 # i는 결제하여 확인 후 재설정, 햔재는 임의로 지정
        pay_xpath = f'//*[@id="contants"]/div[2]/div[2]/table/tbody/tr[{str(i)}]/td[6]/a[3]/img'

        driver.find_element_by_xpath(pay_xpath).click()
        print("열람하기 클릭")
        cnt2 = driver.find_element_by_class_name("colorNotice").text
        cnt2 = cnt2.replace("총", "")
        cnt2 = cnt2.replace("건", "")
        cnt2 = int(cnt2)
        print(str(i) + "번째 목록 수 : " + str(cnt2))

        if cnt2 <= 10:
            repeat_open(cnt2)  # 10개 이하 일 경우 반복하는 함수
            time.sleep(0.5)
            driver.switch_to.window(driver.window_handles[-1])
            driver.close()
        else:
            repeat_open(10)  # 10개 먼저 반복한 후

            time.sleep(0.5)
            driver.switch_to.window(driver.window_handles[-1])
            driver.close()

            driver.switch_to.window(driver.window_handles[0])
            driver.switch_to.frame('wcdFrame')
            print("다음 페이지 반복")
            repeat_open2(cnt2 - 10, pay_xpath)  # 다음 페이지 반복
            time.sleep(0.5)
            driver.switch_to.window(driver.window_handles[-1])
            driver.close()

        driver.switch_to.window(driver.window_handles[0])
        driver.switch_to.frame('wcdFrame')
        time.sleep(1)
        select_day()  # 날짜 설정