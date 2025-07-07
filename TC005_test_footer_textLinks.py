import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse
import time

@pytest.fixture
def driver():
    driver = webdriver.Edge()
    yield driver
    driver.quit()

@pytest.mark.parametrize("elements, expected_path", [
    ("Sobre", "/about.html"),
    ("Carreiras", "/careers.html"),
    ("Política de privacidade", "https://qa.medcloud.link/pdfs/Medcloud-Privacy-Policy.pdf"),
    ("Termos de uso", "https://qa.medcloud.link/pdfs/Medcloud-Terms-Use.pdf")
])
     
def test_footerlinks(driver, elements, expected_path):  
    try:
        driver.get("https://qa.medcloud.link/")
        el = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, elements))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.LINK_TEXT, elements)))
        abas_antes = driver.window_handles
        aba_original = driver.current_window_handle
        driver.execute_script("arguments[0].click();", el)
        time.sleep(2)
        abas_depois = driver.window_handles
        if len(abas_depois) > len(abas_antes):
            nova_aba = list(set(abas_depois) - set(abas_antes))[0]
            driver.switch_to.window(nova_aba)
            WebDriverWait(driver, 10).until(lambda d: expected_path in d.current_url)
            assert expected_path in driver.current_url, f"'{elements}' abriu {driver.current_url}, esperava conter '{expected_path}'"
            driver.close()
            driver.switch_to.window(aba_original)
        else:
            WebDriverWait(driver, 10).until(lambda d: expected_path in d.current_url)
            assert expected_path in driver.current_url, f"'{elements}' redirecionou para {driver.current_url}, esperava conter '{expected_path}'"

    except Exception:
        url = driver.current_url
        parsed = urlparse(url)
        path = parsed.path if parsed.path else parsed.netloc
        pytest.fail(f"Erro ao testar link '{elements}': redirecionou para '{path}', esperava '{expected_path}'", pytrace=False)