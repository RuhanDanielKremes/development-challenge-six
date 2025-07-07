import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

URL = "https://qa.medcloud.link/"

@pytest.fixture(scope="session")
def driver():
    driver = webdriver.Edge()
    yield driver
    driver.quit()

def preencher_formulario_contato(driver, nome, email, telefone, mensagem_texto):
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".flex > .flex-col #name"))
    )
    driver.find_element(By.CSS_SELECTOR, ".flex > .flex-col #name").clear()
    driver.find_element(By.CSS_SELECTOR, ".flex > .flex-col #name").send_keys(nome)

    driver.find_element(By.CSS_SELECTOR, ".flex > .flex-col #email").clear()
    driver.find_element(By.CSS_SELECTOR, ".flex > .flex-col #email").send_keys(email)

    driver.find_element(By.CSS_SELECTOR, ".flex > .flex-col #phone").clear()
    driver.find_element(By.CSS_SELECTOR, ".flex > .flex-col #phone").send_keys(telefone)

    driver.find_element(By.ID, "message").clear()
    driver.find_element(By.ID, "message").send_keys(mensagem_texto)

    driver.find_element(By.CSS_SELECTOR, ".xxl\\3Ah-12").click()

def mensagem_sucesso_contato_aparece(driver):
    try:
        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR,
                "#Contact > section > form > div.mt-8.bg-tertiary.border.border-primary.text-secondary.px-4.py-3.rounded.relative > span"))
        )
        return True
    except:
        return False

invalid_data = [
    ("", "teste@email.com", "4299999999", "Mensagem teste"),                
    ("tester", "email-invalido", "4299999999", "Mensagem teste"),           
    ("tester", "", "4299999999", "Mensagem teste"),                         
    ("tester", "teste@email.com", "", "Mensagem teste"),                    
    ("tester", "teste@email.com", "abc999999", "Mensagem teste"),           
    ("tester", "teste@email.com", "011912345678", "Mensagem teste"),       
    ("tester", "teste@email.com", "912345678", "Mensagem teste"),          
    ("tester", "teste@email.com", "4299999999", ""),                        
]

@pytest.mark.parametrize("nome,email,telefone,mensagem", invalid_data)
def test_formulario_contato_dados_invalidos(driver, nome, email, telefone, mensagem):
    driver.get(URL)
    try:
        el = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".xxl\\3Ah-12"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
        time.sleep(1)

        preencher_formulario_contato(driver, nome, email, telefone, mensagem)
        time.sleep(2)

        assert not mensagem_sucesso_contato_aparece(driver), \
            f"Formulário aceitou dados inválidos: nome='{nome}', email='{email}', telefone='{telefone}', mensagem='{mensagem}'"
    except Exception as e:
        pytest.fail(f"Erro ao testar formulário de contato com dados inválidos: {str(e)}", pytrace=False)
