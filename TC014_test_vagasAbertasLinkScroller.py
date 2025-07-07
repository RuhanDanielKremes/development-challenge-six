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

def elemento_visivel_na_viewport(driver, elemento, tolerancia_px=200):
    rect = driver.execute_script("""
        var el = arguments[0];
        var r = el.getBoundingClientRect();
        return {top: r.top, bottom: r.bottom};
    """, elemento)
    print(rect)
    return 0 <= rect["top"] <= tolerancia_px and rect["bottom"] >= 0

def test_vagasAbertasLinkScroller(driver):
    try:
        driver.get("https://qa.medcloud.link/careers.html")
        
        el = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.mt-8 > .text-secondary'))
        )
        driver.execute_script("arguments[0].click();", el)
        time.sleep(1.5)
        elemento = driver.find_element(By.CSS_SELECTOR, '.pt-8:nth-child(10)')
        
    except Exception as e:
        pytest.fail(f"Erro ao testar link de imprensa '{'.mt-8 > .text-secondary'}': {str(e)}", pytrace=False)


    if not elemento_visivel_na_viewport(driver, elemento):
        pytest.fail(f"Elemento '.pt-8:nth-child(10)' não visível após clique em '.mt-8 > .text-secondary'", pytrace=False)