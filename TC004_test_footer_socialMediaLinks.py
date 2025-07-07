import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse

@pytest.fixture(scope="session")
def driver():
    driver = webdriver.Edge()
    yield driver
    driver.quit()

@pytest.mark.parametrize("elements, expected_domain", [
    (".space-x-6 > a:nth-child(1)", "open.spotify.com"),
    (".space-x-6 > a:nth-child(2)", "instagram.com"),
    (".space-x-6 > a:nth-child(3)", "facebook.com"),
    ("a:nth-child(4)", "x.com"),
    ("a:nth-child(5)", "youtube.com"),
    ("a:nth-child(6)", "linkedin.com"),
])
def test_footerlinks(driver, elements, expected_domain):  
    try:
        driver.get("https://qa.medcloud.link/")
        el = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, elements))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
        driver.execute_script("arguments[0].click();", el)
        WebDriverWait(driver, 10).until(lambda d: expected_domain in d.current_url)
    except Exception:
        url = driver.current_url
        dominio = urlparse(url).netloc
        pytest.fail(f"Erro ao testar '{elements}': redirecionou para '{dominio}', esperava '{expected_domain}'", pytrace=False)
