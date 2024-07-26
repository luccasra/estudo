from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Função para obter o valor, realizar as operações e retornar os resultados
def obter_valor(url):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    max_tentativas = 3
    tentativas = 0

    while tentativas < max_tentativas:
        try:
            driver.get(url)

            wait = WebDriverWait(driver, 10)
            acesso_automatico_link = wait.until(EC.element_to_be_clickable((By.ID, 'acessoAutomatico')))
            acesso_automatico_link.click()

            valor_campo = wait.until(EC.presence_of_element_located((By.ID, 'valorSP')))

            if valor_campo:
                valor = float(valor_campo.text.replace('R$', '').replace('.', '').replace(',', '.').strip())
                multiplicacao = valor * 4.5
                divisao = multiplicacao / 2

                driver.quit()
                return multiplicacao, divisao
            else:
                print('Campo não encontrado.')
        except Exception as e:
            print(f'Ocorreu um erro: {e}')

        tentativas += 1
        if tentativas < max_tentativas:
            print('Tentando novamente...')
            time.sleep(1)

    print('Número máximo de tentativas alcançado. Não foi possível acessar o site.')
    driver.quit()
    return None, None

# Solicita o mês e o ano de referência da competência
mes = input('Digite o mês de referência (MM): ')
ano = input('Digite o ano de referência (AAAA): ')

# Loop principal para solicitar códigos e processar
while True:
    numero = input('Digite o código do procedimento (ou "sair" para encerrar): ')

    if numero.lower() == 'sair':
        print('Encerrando o programa.')
        break

    url = f'http://sigtap.datasus.gov.br/tabela-unificada/app/sec/procedimento/exibir/{numero}/{mes}/{ano}'

    resultado_multiplicacao, resultado_divisao = obter_valor(url)

    print('_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ __ _ _ _ _ _ _ _ ')
    print()
    if resultado_multiplicacao is not None and resultado_divisao is not None:
        print(f'Valor já Multiplicado: {resultado_multiplicacao}')
        print(f'50% do Valor: {resultado_divisao}')
    else:
        print('Não foi possível obter os resultados.')
    print('_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ __ _ _ _ _ _ _ _')

    print('Pronto para o próximo código...')
