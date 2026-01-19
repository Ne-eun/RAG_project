from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
import re
from bs4 import BeautifulSoup
import os


def get_row_per_page():
    page_source = driver.find_element(By.ID, "contentBody").get_attribute("innerHTML")
    time.sleep(1)
    조문정보_html = re.search(
        r"<!--\s*조문정보\s*-->[\s\S]*?<!--\s*조문정보\s*-->", page_source, re.DOTALL
    )
    soup = BeautifulSoup(조문정보_html.group(0), "html.parser")
    조문_list = soup.find_elements(By.CLASS_NAME, "pgroup")

    print("조문_list", len(조문_list), 조문_list[0])

    current_url = driver.current_url

    content = f"{조문정보}\n\n#url#{current_url}"
    os.makedirs(f"./datas", exist_ok=True)
    with open(f"./datas/{header}.txt", encoding="utf-8", mode="w") as f:
        f.write(content)


if __name__ == "__main__":
    # 드라이버 로드
    driver = webdriver.Chrome()
    driver.get(
        "https://www.law.go.kr/LSW/lsAstSc.do?menuId=391&subMenuId=397&tabMenuId=437&query=#AJAX"
    )
    time.sleep(3)

    # 형사법 페이지 이동 / 예정법령은 제외
    driver.find_element(By.ID, "liLsFd").find_element(By.XPATH, "parent::a").click()
    time.sleep(2)
    driver.find_element(By.ID, "divLsFd").find_element(By.ID, "lsFd09").click()
    time.sleep(2)
    driver.find_element(By.ID, "efCheck").click()
    time.sleep(2)
    driver.execute_script("setEfChk(); return;")

    count = driver.find_element(By.CLASS_NAME, "paging").find_elements(
        By.TAG_NAME, "li"
    )
    # 페이지네이션
    for i in range(0, len(count)):
        paging = driver.find_element(By.CLASS_NAME, "paging").find_elements(
            By.TAG_NAME, "li"
        )
        paging[i].click()
        time.sleep(5)

        main_window = driver.current_window_handle
        법령목록 = driver.find_element(By.TAG_NAME, "tbody").find_elements(
            By.TAG_NAME, "tr"
        )

        # 각 법령 상세페이지 접근
        for 법령 in 법령목록:
            row = 법령.find_element(By.CLASS_NAME, "ctn1").find_element(
                By.TAG_NAME, "a"
            )
            header = row.text
            row.click()
            time.sleep(3)

            # 팝업으로 drive 이동
            for window in driver.window_handles:
                if window != main_window:
                    driver.switch_to.window(window)
                    break

            # 데이터 추출
            get_row_per_page()
            break
            # 팝업 닫기
            driver.close()
            time.sleep(1)
            driver.switch_to.window(main_window)
        break
