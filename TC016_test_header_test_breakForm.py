import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

URL = "https://qa.medcloud.link/"

invalid_inputs = [
    {"name": "", "email": "teste@email.com", "phone": "4299999999", "campo": "nome vazio"},
    {"name": "tester", "email": "email-invalido", "phone": "4299999999", "campo": "email inválido"},
    {"name": "tester", "email": "teste@email.com", "phone": "abc123", "campo": "telefone com letras"},
    {"name": "tester", "email": "", "phone": "4299999999", "campo": "email vazio"},
    {"name": "tester", "email": "teste@email.com", "phone": "", "campo": "telefone vazio"},
]

@pytest.fixture
def driver():
    driver = webdriver.Edge()
    driver.get(URL)
    yield driver
    driver.quit()

@pytest.mark.parametrize("data", invalid_inputs)
def test_formulario_com_dados_invalidos(driver, data):
    try:
        driver.refresh()
        time.sleep(1)

        driver.find_element(By.CSS_SELECTOR, ".h-full > .text-white").click()
        time.sleep(1)

        driver.find_element(By.ID, "name").send_keys(data["name"])
        driver.find_element(By.ID, "email").send_keys(data["email"])
        driver.find_element(By.ID, "phone").send_keys(data["phone"])
        Select(driver.find_element(By.ID, "pos")).select_by_visible_text("Outros")
        driver.find_element(By.CSS_SELECTOR, ".mt-8 > .xxl\\:text-base").click()
        time.sleep(2)
        success_message_xpath = "//span[contains(text(), 'Trial solicitado com sucesso')]"
        mensagem_aparece = False
        try:
            WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, success_message_xpath)))
            mensagem_aparece = True
        except:
            pass

        assert not mensagem_aparece, f"Falha: formulário aceitou {data['campo']}"

    except Exception as e:
        pytest.fail(f"Erro inesperado ao testar {data['campo']}: {str(e)}", pytrace=False)
