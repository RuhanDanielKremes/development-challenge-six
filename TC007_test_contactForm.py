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
        el = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".xxl\\3Ah-12"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, ".flex > .flex-col #name").send_keys("tester")
        driver.find_element(By.CSS_SELECTOR, ".flex > .flex-col #email").send_keys("tester@email.com")
        driver.find_element(By.CSS_SELECTOR, ".flex > .flex-col #phone").send_keys("4299999999")
        driver.find_element(By.ID, "message").send_keys("minha mensagem")
        driver.find_element(By.CSS_SELECTOR, ".xxl\\3Ah-12").click()
        mensagem = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#Contact > section > form > div.mt-8.bg-tertiary.border.border-primary.text-secondary.px-4.py-3.rounded.relative > span"))
        ) 
        assert "Mensagem enviada com sucesso" in mensagem.text
    except Exception as e:
        pytest.fail(f"Erro ao preencher e enviar o formulário de contato: {str(e)}", pytrace=False)
        