import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

URL = "https://qa.medcloud.link/careers/integration-analyst.html"
TEST_FILES_DIR = os.path.abspath("test_files")  # pasta onde os arquivos de teste estão

@pytest.fixture(scope="session")
def driver():
    driver = webdriver.Edge()
    yield driver
    driver.quit()

def preencher_formulario_com_arquivo(driver, nome, lastName, email, telefone, mensagem, caminho_arquivo):


    driver.find_element(By.ID, "name").clear()
    driver.find_element(By.ID, "name").send_keys(nome)

    driver.find_element(By.ID, "lastName").clear()
    driver.find_element(By.ID, "lastName").send_keys(lastName)

    driver.find_element(By.ID, "email").clear()
    driver.find_element(By.ID, "email").send_keys(email)

    driver.find_element(By.ID, "phone").clear()
    driver.find_element(By.ID, "phone").send_keys(telefone)

    driver.find_element(By.ID, "message").clear()
    driver.find_element(By.ID, "message").send_keys(mensagem)

    file_input = driver.find_element(By.ID, "curriculum")
    file_input.send_keys(caminho_arquivo)

    driver.find_element(By.CSS_SELECTOR, ".text-xs").click()

def mensagem_sucesso_upload_aparece(driver):
    try:
        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".sm\\3Ainline"))
        )
        return True
    except:
        return False

arquivos_teste = [
    ("teste.pdf", True),   
    ("teste.jpg", False),  
    ("teste.txt", False),  
    ("teste.exe", False),  
]

@pytest.mark.parametrize("nome_arquivo,deve_aceitar", arquivos_teste)
def test_formulario_upload_arquivo(driver, nome_arquivo, deve_aceitar):
    driver.get(URL)
    
    try:
        driver.find_element(By.CSS_SELECTOR, ".xxl\\3Atext-base:nth-child(2)").click()
    except Exception as e:
        print()
    try:
        el = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "message"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
        time.sleep(1)
        caminho_arquivo = os.path.join(TEST_FILES_DIR, nome_arquivo)
        assert os.path.exists(caminho_arquivo), f"Arquivo de teste não encontrado: {caminho_arquivo}"
        preencher_formulario_com_arquivo(
            driver,
            nome="tester",
            lastName="tester",
            email="tester@email.com",
            telefone="4299999999",
            mensagem="Teste de upload",
            caminho_arquivo=caminho_arquivo
        )

        time.sleep(1)
        sucesso = mensagem_sucesso_upload_aparece(driver)

        if deve_aceitar:
            assert sucesso, f"PDF válido foi rejeitado: {nome_arquivo}"
        else:
            assert not sucesso, f"Arquivo inválido foi aceito: {nome_arquivo}"

    except Exception as e:
        pytest.fail(f"Erro ao testar upload com '{nome_arquivo}': {str(e)}", pytrace=False)