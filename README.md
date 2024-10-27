# Projeto: selenium_factory

Módulo com funções de configuração e geração de WebDriver Selenium em Python. Na versão 1.0.0, apenas a função de geração de WebDriver do Firefox foi implementada.

## Parâmetros de configuração

### Firefox WebDriver

A função de configuração de WebDriver do Firefox ***configure_firefox()*** aceita os seguintes parâmetros:

- **headless:** Indica se o driver deve ser executado em modo headless.
- **http_proxy:** Endereço do proxy HTTP.
- **socks_proxy:** Endereço do proxy SOCKS.
- **download_dir:** Diretório de download.
- **firefox_path:** Localização do executável do Firefox.
- **user_agent:** Agente de usuário.
- **geckodriver_path:** Localização do executável do geckodriver.

## Exemplo de uso

```
from selenium_factory import configure_firefox, get_firefox_driver

configure_firefox(headless=False)

with get_firefox_driver() as driver:
    driver.get("https://www.google.com")

with get_firefox_driver() as driver:
    driver.get("www.duckduckgo.com")
```

Para projetos grandes, basta acionar a função ***configure_firefox()*** na incialização do projeto. Após a configuração inicial, os WebDrivers obtidos à partir da invocação da função ***get_firefox_driver()*** usarão os parâmetros de configuração inicialmente informados.