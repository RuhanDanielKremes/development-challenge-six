import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

URL = "https://qa.medcloud.link/"

@pytest.fixture(scope="session")
def driver():
    driver = webdriver.Edge()
    yield driver
    driver.quit()

def preencher_formulario(driver, nome, email, telefone):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "name")))
    driver.find_element(By.ID, "name").clear()
    driver.find_element(By.ID, "name").send_keys(nome)
    driver.find_element(By.ID, "email").clear()
    driver.find_element(By.ID, "email").send_keys(email)
    driver.find_element(By.ID, "phone").clear()
    driver.find_element(By.ID, "phone").send_keys(telefone)
    Select(driver.find_element(By.ID, "pos")).select_by_visible_text("Outros")
    driver.find_element(By.CSS_SELECTOR, ".mt-8 > .xxl\\:text-base").click()

def mensagem_sucesso_aparece(driver):
    try:
        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, "//span[contains(text(), 'Trial solicitado com sucesso')]"))
        )
        return True
    except:
        return False

invalid_data = [
    ("", "teste@email.com", "4299999999"),
    ("tester", "email-invalido", "4299999999"),
    ("tester", "", "4299999999"),
    ("tester", "tester@email.com", ""),
    ("tester", "tester@email.com", "abc999999"), 
]
    # ("tester", "tester@email.com", "011912345678"),       # DDD inválido (0)
    # ("tester", "tester@email.com", "119123456789"),       # Dígitos a mais
    # ("tester", "tester@email.com", "91234-5678"),         # Sem DDD

botoes = [
    ".w-1\\/2:nth-child(1) .xxl\\3Atext-base",
    ".sm\\:mt-12 .xxl\\:text-base"
]

@pytest.mark.parametrize("nome,email,telefone", invalid_data)
@pytest.mark.parametrize("botao_css", botoes)
def test_formulario_invalido(driver, botao_css, nome, email, telefone):
    driver.get(URL)
    try:
        el = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, botao_css))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
        time.sleep(1.5)
        driver.execute_script("arguments[0].click();", el)
        preencher_formulario(driver, nome, email, telefone)
        time.sleep(2)
        assert not mensagem_sucesso_aparece(driver), f"Formulário aceitou dados inválidos: {nome}, {email}, {telefone}"
    except Exception as e:
        pytest.fail(f"Erro ao testar botão '{botao_css}' com dados inválidos: {str(e)}", pytrace=False)
