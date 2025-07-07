import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

@pytest.fixture(scope="session")
def driver():
    driver = webdriver.Edge()
    yield driver
    driver.quit()

@pytest.mark.parametrize("url", [  
    "https://qa.medcloud.link/careers/integration-analyst.html",
    "https://qa.medcloud.link/careers.html",
    "https://qa.medcloud.link/about.html",
    "https://qa.medcloud.link/"
])
def test_goToTop(driver, url):    
    driver.get(url)
    try:
        el = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#cookie-notice > .xxl\3Atext-base"))
        )
        el.click()
    except Exception as e:
        return
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time(2)
        botao_topo = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".CookiesNotice_backBtn__1tfUj"))
        )
        botao_topo.click()
        WebDriverWait(driver, 5).until(
            lambda d: d.execute_script("return window.scrollY") < 50
        )
        assert driver.execute_script("return window.scrollY") < 50, " A página não voltou ao topo após o clique."
    except Exception as e:
        pytest.fail(f"Erro ao testar botão de voltar ao topo na página '{url}': {str(e)}", pytrace=False)
