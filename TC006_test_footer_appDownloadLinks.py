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
    (".sm\\3Aw-full:nth-child(5) li:nth-child(1) > a", "apps.apple.com/br/app/medcloud/"),
    (".sm\\3Aw-full:nth-child(5) li:nth-child(2) > a", "play.google.com/store/apps/details?id=co.medcloud.android")
])
def test_footerlinks(driver, elements, expected_domain):  
    try:
        driver.get("https://qa.medcloud.link/")
        el = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, elements))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
        abas_antes = driver.window_handles
        driver.execute_script("arguments[0].click();", el)
        WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > len(abas_antes))
        nova_aba = list(set(driver.window_handles) - set(abas_antes))[0]
        driver.switch_to.window(nova_aba)
        WebDriverWait(driver, 10).until(lambda d: expected_domain in d.current_url)
        assert expected_domain in driver.current_url, f"Esperava '{expected_domain}', mas foi para '{driver.current_url}'"
        driver.close()
        driver.switch_to.window(abas_antes[0])
    except Exception:
        url = driver.current_url
        pytest.fail(f"Erro ao testar '{elements}': redirecionou para '{url}', esperava conter '{expected_domain}'", pytrace=False)