import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def driver():
    driver = webdriver.Edge()
    yield driver
    driver.quit()

@pytest.mark.parametrize("element, siteTarget", [  
    (".max-w-sm:nth-child(1) > .xxl\\3Apy-8", "https://medicinasa.com.br/telerradiologia-medcloud/"),
    (".max-w-sm:nth-child(2) > .xxl\\3Apy-8", "https://www.terra.com.br/noticias/dino/medcloud-recebe-premio-da-frost-sullivan-por-sua-plataforma-de-exames-em-nuvem,f0c3cc1da7b987b4b7e0fdee3d27b46eypvhry1w.html"),
    (".max-w-sm:nth-child(3) > .xxl\\3Apy-8", "https://news.microsoft.com/pt-br/com-aplicativo-para-exames-e-prontuarios-online-microsoft-ajuda-medcloud-a-inovar-no-segmento-de-saude/"),
    (".max-w-sm:nth-child(4) > .xxl\\3Apy-8", "spr.org.br"),
    (".max-w-sm:nth-child(5) > .xxl\\3Apy-8", "spr.org.br"),
])
def test_imprensa_link(driver, element, siteTarget):
    try:
        driver.get("https://qa.medcloud.link/about.html")
        
        el = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, element))
        )
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, element)))

        abas_antes = driver.window_handles
        aba_original = driver.current_window_handle
        driver.execute_script("arguments[0].click();", el)

        time.sleep(2)

        abas_depois = driver.window_handles
        abas_novas = list(set(abas_depois) - set(abas_antes))
        if not abas_novas:
            pytest.fail(f"Nenhuma nova aba foi aberta ao clicar em '{element}'", pytrace=False)

        nova_aba = abas_novas[0]
        driver.switch_to.window(nova_aba)

        WebDriverWait(driver, 10).until(lambda d: siteTarget in d.current_url)
        assert siteTarget in driver.current_url, f"'{element}' abriu {driver.current_url}, esperava conter '{siteTarget}'"

        driver.close()
        driver.switch_to.window(aba_original)

    except Exception as e:
        pytest.fail(f"Erro ao testar link de imprensa '{element}': {str(e)}", pytrace=False)
