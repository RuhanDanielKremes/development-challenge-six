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

def test_vaga_redirecter(driver):
    try:
        driver.get("https://qa.medcloud.link/careers.html")
        
        
        el = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.mt-8 > .text-secondary'))
        )
        driver.execute_script("arguments[0].click();", el)
        time.sleep(1.5)
        elemento = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.w-1\/3:nth-child(1) .shadow-around'))
        )
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.w-1\/3:nth-child(1) .shadow-around')))
        driver.execute_script("arguments[0].click();", elemento)
        WebDriverWait(driver, 10).until(lambda d: "https://qa.medcloud.link/careers/integration-analyst.html" in d.current_url)
        assert "https://qa.medcloud.link/careers/integration-analyst.html" in driver.current_url, f"'{'.w-1\/3:nth-child(1) .shadow-around'}' abriu {driver.current_url}, esperava conter https://qa.medcloud.link/careers/integration-analyst.html"
    except Exception as e:
        pytest.fail(f"Erro ao testar link de imprensa '.w-1\/3:nth-child(1) .shadow-around': {str(e)}", pytrace=False)