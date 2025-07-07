import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def driver():
    driver = webdriver.Edge()
    yield driver
    driver.quit()

def preencher_formulario(driver):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "name")))
    driver.find_element(By.ID, "name").send_keys("tester")
    driver.find_element(By.ID, "email").send_keys("tester@email.com")
    driver.find_element(By.ID, "phone").send_keys("4299999999")
    Select(driver.find_element(By.ID, "pos")).select_by_visible_text("Outros")
    driver.find_element(By.CSS_SELECTOR, ".mt-8 > .xxl\\:text-base").click()

def aguardar_mensagem_sucesso(driver):
    span = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//span[contains(text(), 'Trial solicitado com sucesso')]"))
    )
    assert "Trial solicitado com sucesso" in span.text

@pytest.mark.parametrize("cssButton", [
    ".w-1\\/2:nth-child(1) .xxl\\3Atext-base",
    ".sm\\:mt-12 .xxl\\:text-base",
])

def test_formularios(driver, cssButton):
    try:
        driver.get("https://qa.medcloud.link/")
        el = driver.find_element(By.CSS_SELECTOR, cssButton)
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, cssButton))).click()
        preencher_formulario(driver)
        aguardar_mensagem_sucesso(driver)
    except Exception as e:
        pytest.fail(f"Erro ao testar botão '{cssButton}': {str(e)}", pytrace=False)