# Projeto: selenium_factory

Módulo com funções de configuração e geração de WebDriver Selenium em Python. Na versão 1.0.0, apenas a função de geração de WebDriver do Firefox foi implementada.

## Instalação

O módulo pode ser instalado a partir do repositório Github. Para instalar, use o comando:

```pip install git+https://github.com/eisimoes/selenium_factory```

Para instalar uma versão específica:

```pip install git+https://github.com/eisimoes/selenium_factory@1.0.0```

## Parâmetros de configuração

### Firefox WebDriver

A função de configuração de WebDriver do Firefox ***configure_firefox_driver()*** aceita os seguintes parâmetros:

- **headless:** Indica se o driver deve ser executado em modo headless.
- **http_proxy:** Endereço do proxy HTTP.
- **socks_proxy:** Endereço do proxy SOCKS.
- **download_dir:** Diretório de download.
- **firefox_path:** Localização do executável do Firefox.
- **user_agent:** Agente de usuário.
- **geckodriver_path:** Localização do executável do geckodriver.

## Exemplo de uso

```
from selenium_factory import configure_firefox_driver, get_firefox_driver

configure_firefox_driver(headless=False)

with get_firefox_driver() as driver:
    driver.get("https://www.google.com")

with get_firefox_driver() as driver:
    driver.get("www.duckduckgo.com")
```

Para projetos grandes, basta acionar a função ***configure_firefox_driver()*** na incialização do projeto. Após a configuração inicial, os WebDrivers obtidos à partir da invocação da função ***get_firefox_driver()*** usarão os parâmetros de configuração inicialmente informados.