import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

@pytest.fixture(scope="session")
def driver():
    driver = webdriver.Edge()
    driver.get("https://qa.medcloud.link/")
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

@pytest.mark.parametrize("idHeader,idSection", [
    ("headerRis", "RIS"),
    ("headerPacs", "PACS"),
    ("headerPortal", "Portal"),
    ("headerPlans", "Plans"),
    ("headerContact", "Contact"),
    ("headerHome", "Home")
])

def test_header_section_visibility(driver, idHeader, idSection):
    try:
        driver.find_element(By.ID, idHeader).click()
        time.sleep(1.5)
        elemento = driver.find_element(By.ID, idSection)
    except Exception as e:
        pytest.fail(f"Erro ao clicar ou encontrar {idHeader} → {idSection}: {str(e)}", pytrace=False)

    if not elemento_visivel_na_viewport(driver, elemento):
        pytest.fail(f"Elemento '{idSection}' não visível após clique em '{idHeader}'", pytrace=False)
