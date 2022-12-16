from selenium import webdriver
from selenium.webdriver.chrome.options import Options

if '__main__' == __name__:
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")

    driver = webdriver.Chrome()
    driver.get("https://www.sportytrader.es/pronosticos/baloncesto/usa/nba-306/")
    html = driver.page_source
    driver.quit()

    print(html)
