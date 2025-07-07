import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

@pytest.fixture(scope="session")
def driver():
    driver = webdriver.Edge()
    driver.get("https://qa.medcloud.link/careers/integration-analyst.html")
    yield driver
    driver.quit()


def gerar_arquivo_vazio():
    caminho = "arquivo_vazio.txt"
    with open(caminho, "wb") as f:
        f.write(b"\0" * 1024)
    return os.path.abspath(caminho)


def test_formulario_curriculo(driver):    
    try:
        el = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "message"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
        time.sleep(1)
        driver.find_element(By.ID, "name").send_keys("tester")
        driver.find_element(By.ID, "lastName").send_keys("tester")
        driver.find_element(By.ID, "email").send_keys("tester@email.com")
        driver.find_element(By.ID, "phone").send_keys("4299999999")
        driver.find_element(By.ID, "message").send_keys("minha mensagem")
        arquivo = gerar_arquivo_vazio()
        input_file = driver.find_element(By.ID, "curriculum")
        input_file.send_keys(arquivo)
        try:
            driver.find_element(By.CSS_SELECTOR, ".text-xs").click()
            mensagem = WebDriverWait(driver, 2).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".sm\\3Ainline"))
            )
        except Exception as e:
            driver.find_element(By.CSS_SELECTOR, ".text-xs").click()
            mensagem = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".sm\\3Ainline"))
            )
        assert "Sua candidatura para a vaga de Analista de Integrações foi efetuada com sucesso!" in mensagem.text
    except Exception as e:
        pytest.fail(f"Erro ao preencher e enviar o formulário de contato: {str(e)}", pytrace=False)
        