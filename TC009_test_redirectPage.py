import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(scope="session")
def driver():
    driver = webdriver.Edge()
    yield driver
    driver.quit()

@pytest.mark.parametrize("siteTest, siteTarget, selector_type, selector_value", [
    ("https://qa.medcloud.link/careers/integration-analyst.html", "https://qa.medcloud.link/careers.html", "link", "Ver todas as vagas"),
    ("https://qa.medcloud.link/careers/integration-analyst.html", "https://qa.medcloud.link/careers.html", "css", ".pl-4"),

    ("https://qa.medcloud.link/careers.html", "https://qa.medcloud.link/", "link", "Voltar ao site"),
    ("https://qa.medcloud.link/careers.html", "https://qa.medcloud.link/", "css", ".pl-4"),

    ("https://qa.medcloud.link/about.html", "https://qa.medcloud.link/", "link", "Voltar a página inicial"),
    ("https://qa.medcloud.link/about.html", "https://qa.medcloud.link/", "css", ".pl-4"),
])
def test_redirecionamentos_voltar(driver, siteTest, siteTarget, selector_type, selector_value):    
    driver.get(siteTest)

    try:
        if selector_type == "link":
            el = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.LINK_TEXT, selector_value))
            )
        elif selector_type == "css":
            el = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, selector_value))
            )
        else:
            pytest.fail(f"Tipo de seletor desconhecido: {selector_type}", pytrace=False)

        el.click()

        WebDriverWait(driver, 10).until(lambda d: d.current_url == siteTarget)
        assert driver.current_url == siteTarget
    except Exception as e:
        pytest.fail(f"Erro ao testar {selector_type.upper()} em '{siteTest}': {str(e)}", pytrace=False)
