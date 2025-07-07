import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

@pytest.fixture(scope="session")
def driver():
    driver = webdriver.Edge()
    driver.get("https://qa.medcloud.link/")
    yield driver
    driver.quit()

def test_formulario_contato(driver):
    try:
        driver.find_element(By.CSS_SELECTOR, ".h-full > .text-white").click()
        time.sleep(1)
        driver.find_element(By.ID, "name").send_keys("tester")
        driver.find_element(By.ID, "email").send_keys("tester@email.com")
        driver.find_element(By.ID, "phone").send_keys("4299999999")
        Select(driver.find_element(By.ID, "pos")).select_by_visible_text("Outros")
        driver.find_element(By.CSS_SELECTOR, ".mt-8 > .xxl\\:text-base").click()
        time.sleep(1)
        mensagem = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//span[contains(text(), 'Trial solicitado com sucesso')]"))
        )
        assert "Trial solicitado com sucesso" in mensagem.text
    except Exception as e:
        pytest.fail(f"Erro ao preencher e enviar o formulário de contato: {str(e)}", pytrace=False)
