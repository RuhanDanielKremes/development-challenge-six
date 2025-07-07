import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

@pytest.fixture(scope="session")
def driver():
    driver = webdriver.Edge()
    yield driver
    driver.quit()

@pytest.mark.parametrize("url", [  
    "https://qa.medcloud.link/",
    "https://qa.medcloud.link/about.html",
    "https://qa.medcloud.link/careers/integration-analyst.html",
    "https://qa.medcloud.link/careers.html",
])
def test_botao_email(driver, url):
    try:
        driver.get(url)

        match url:
            case "https://qa.medcloud.link/":
                botao = driver.find_element(By.LINK_TEXT, "contato@medcloud.com.br")
                href = botao.get_attribute("href")
                assert href.startswith("mailto:"), f"O botão não possui um link mailto. href encontrado: {href}"
                assert "contato@medcloud.com.br" in href, f"Email errado no link: {href}"

            case "https://qa.medcloud.link/about.html":
                botao = driver.find_element(By.LINK_TEXT, "Entre em contato")
                href = botao.get_attribute("href")
                assert href.startswith("mailto:"), f"O botão não possui um link mailto. href encontrado: {href}"
                assert "mpp@medcloud.com.br" in href, f"Email errado no link: {href}"

            case "https://qa.medcloud.link/careers/integration-analyst.html":
                botao = driver.find_element(By.LINK_TEXT, "contato@medcloud.com.br")
                href = botao.get_attribute("href")
                assert href.startswith("mailto:"), f"O botão não possui um link mailto. href encontrado: {href}"
                assert "contato@medcloud.com.br" in href, f"Email errado no link: {href}"

            case "https://qa.medcloud.link/careers.html":
                botao = driver.find_element(By.LINK_TEXT, "contato@medcloud.com.br")
                href = botao.get_attribute("href")
                assert href.startswith("mailto:"), f"O botão não possui um link mailto. href encontrado: {href}"
                assert "contato@medcloud.com.br" in href, f"Email errado no link: {href}"

    except Exception as e:
        pytest.fail(f"Erro ao testar botão de email: {str(e)}", pytrace=False)
