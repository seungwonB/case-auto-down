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
import datetime
import openpyxl

wb = openpyxl.Workbook()
sheet = wb.active

def main_Crawler(name, jumin1, jumin2, bub):
    global wb
    url = 'https://www.scourt.go.kr/portal/information/finalruling/peruse/peruse_status.jsp'
    driver = webdriver.Chrome()
    driver.get(url)
    driver.maximize_window()

    now = datetime.datetime.now()
    nowDate = now.strftime('%Y-%m-%d')
    nowDate = nowDate.replace("-", "")


    def login():
        # 개인정보 클릭
        driver.switch_to.frame('wcdFrame')
        driver.find_element_by_xpath('//*[@id="accept"]').click()

        # 스크롤 내리기
        driver.execute_script("window.scrollTo(0, 300)")

        # 이름
        driver.find_element_by_class_name("mr").send_keys(name)

        # 주민 앞자리
        driver.find_element_by_id("jumin1").send_keys(jumin1)

        # 주민 뒷자리
        driver.find_element_by_id("jumin2").send_keys(jumin2)

        # 실명확인 클릭
        driver.find_element_by_id("auth").click()


    date_list = ["20130101", "20131231", "20140101", "20141231", "20150101", "20151231",
                 "20160101", "20161231", "20170101", "20171231", "20180101", "20181231", "20190101", "20191231",
                 "20200101", "20201231", "20210101", nowDate]


    # 달력에 날짜 지정
    def calendar():
        time.sleep(0.5)
        # 기존 날짜 지우기
        driver.find_element_by_id("ssDate").clear()
        driver.find_element_by_id("seDate").clear()
        # 첫번째 날짜 입력
        driver.find_element_by_id("ssDate").send_keys("20130101")
        driver.find_element_by_id("seDate").send_keys("20131231")


    # 법원명 선택
    def select():

        # 관련법령 작성
        driver.find_element_by_id('spanBub').send_keys(bub)

        # 검색 클릭
        driver.find_element_by_id('search-button').click()


    # 목록수
    def list50():
        time.sleep(0.5)
        # 목록 수 클릭
        driver.find_element_by_id('sviewlist').click()
        # 50개 클릭
        driver.find_element_by_xpath('//*[@id="sviewlist"]/option[5]').click()
        #
        driver.find_element_by_xpath('//*[@id="reasonArea"]/div[1]/div/dl/dd[4]/img').click()


    login()  # 로그인하고
    calendar()  # 날짜 선택하고
    select()  # 법원명, 조항 입력하고
    list50()  # 검색수 50건으로 설정하고

    res = requests.get(url)
    html = res.text
    bs = bs4.BeautifulSoup(html, 'html.parser')


    # 다음 페이지 갯수 추출
    def count():
        # 검색 결과 갯수 추출
        count = driver.find_element_by_xpath('//*[@id="reasonArea"]/h4/span').text
        # 숫자만 추출하기 위해 총, 건을 제거 - (ex-검색결과 : 총 260건)
        count = count.replace("총", "")
        count = count.replace("건", "")
        count = int(count)

        return count



    def fields():
        a = 1
        b = 51
        cnt = 0
        minus = 0
        total = 0
        return cnt, minus, total, a, b



    def text():
        global sheet
        cnt, minus, total, a, b = fields()
        k = 1
        for i in range(a, b):
            for j in range(2, 5):  # 선고일자, 법원명, 사건명만 긁어오기
                try:
                    name = driver.find_element_by_xpath('//*[@id="tbody"]/tr[' + str(k) + ']' + '/td[' + str(j) + ']')
                    # sheet.cell(row=i, column=j-1).value = name.text
                except:
                    minus += 1
                    break
                sheet.cell(row=i, column=j - 1).value = name.text  # 엑셀에 정보 저장
            cnt += 1
            k += 1
        total = cnt - minus  # 현재 페이지에서 긁어온 갯수
        a = b
        b += 50
        k = 1
        cnt = 0
        minus = 0


    text()  # 긁어오기


    def repeat():
        i = 2
        paging = int(count() / 50 + 1)
        if count() > 500:
            while True:
                page = driver.find_element_by_xpath('//*[@id="paging"]/a[' + str(i) + ']')
                page.click()
                time.sleep(1)
                text()
                time.sleep(1)
                i += 1
                if i == 11: break

            i = 3
            driver.find_element_by_xpath('//*[@id="paging"]/a[11]/img').click()
            paging = int((count() - 500) / 50 + 1)

            time.sleep(1)
            text()
            time.sleep(1)
            while True:
                page = driver.find_element_by_xpath(f'//*[@id="paging"]/a[{str(i)}]')

                page.click()
                time.sleep(1)
                text()
                time.sleep(1)
                i += 1
                if i == paging + 2: break

        else:
            while i < paging + 1:
                # 다음 페이지 클릭
                page = driver.find_element_by_xpath('//*[@id="paging"]/a[' + str(i) + ']')
                page.click()
                time.sleep(1)
                text()
                time.sleep(1)
                i += 1


    repeat()


    def search2(date_list, m, n):
        # 검색창 1년 단위로 검색함
        driver.find_element_by_xpath('//*[@id="swlink"]/img').click()
        time.sleep(1)

        driver.find_element_by_id("ssDate").clear()
        driver.find_element_by_id("seDate").clear()

        driver.find_element_by_id("ssDate").send_keys(date_list[m])
        driver.find_element_by_id("seDate").send_keys(date_list[n])

        driver.find_element_by_id('search-button').click()


    # 2013~현재
    # m = 0
    # n = 1
    # for i in range(10):
    #     search2(date_list, m ,n )
    #     list50()
    #     count()
    #     text()
    #     repeat()
    #     m += 2
    #     n += 2

    # 2021 수동 클릭 후
    # list50()
    # count()
    # text()

    # 저장
    wb.save('data_Case.xlsx')
