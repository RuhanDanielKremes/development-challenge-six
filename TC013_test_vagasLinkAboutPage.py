import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def driver():
    driver = webdriver.Edge()
    yield driver
    driver.quit()

def test_vagas_link(driver):
    try:
        driver.get("https://qa.medcloud.link/about.html")
        
        el = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.sm\\3Amy-0'))
        )
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.sm\\3Amy-0')))
        driver.execute_script("arguments[0].click();", el)
        WebDriverWait(driver, 10).until(lambda d: "https://qa.medcloud.link/careers.html" in d.current_url)
        assert "https://qa.medcloud.link/careers.html" in driver.current_url, f"'{'.sm\\3Amy-0'}' abriu {driver.current_url}, esperava conter https://qa.medcloud.link/careers.html"
    except Exception as e:
        pytest.fail(f"Erro ao testar link de imprensa '{'.sm\\3Amy-0'}': {str(e)}", pytrace=False)
