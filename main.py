from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd


def start_driver():

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    return driver


def login_to_website(driver):

    username = driver.find_element(By.ID,"username")
    password = driver.find_element(By.ID,"password")

    username.send_keys("admin")
    password.send_keys("admin")

    login_btn = driver.find_element(By.CLASS_NAME,"btn")
    login_btn.click()


def collect_quotes(driver):

    WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.CLASS_NAME,"quote"))
    )

    data = []

    while True:

        quotes = driver.find_elements(By.CLASS_NAME,"quote")

        for quote in quotes:

            text = quote.find_element(By.CLASS_NAME,"text").text
            author = quote.find_element(By.CLASS_NAME,"author").text
            tags = quote.find_elements(By.CLASS_NAME,"tag")

            tag_list = [tag.text for tag in tags]

            data.append({
                "Text":text,
                "Author":author,
                "Tags":tag_list
            })

        try:
            next_btn = driver.find_element(By.CSS_SELECTOR,".next a")
            next_btn.click()
        except:
            break

    return data


def save_data(data):

    df = pd.DataFrame(data)

    df.to_csv("quotes.csv",index=False)
    df.to_excel("quotes.xlsx",index=False)


def main():

    driver = start_driver()

    driver.get("https://quotes.toscrape.com/login")

    login_to_website(driver)

    data = collect_quotes(driver)

    save_data(data)

    driver.quit()


if __name__ == "__main__":
    main()