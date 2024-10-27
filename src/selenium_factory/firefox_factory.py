"""
Método Factory para geração de driver Selenium do Firefox
"""

from contextlib import contextmanager
from typing import Callable, Dict, Optional, Type, TypeVar
from threading import Lock

from selenium.common.exceptions import WebDriverException
from selenium.webdriver import Firefox
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.webdriver import WebDriver


T = TypeVar('T')
lock = Lock()


def singleton(cls: Type[T]) -> Callable[[], T]:
    """
    Decorator para tornar uma classe um singleton.

    Args:
        cls (Type[T]): A classe a ser tornada um singleton.

    Retorna:
        Callable[[], T]: Uma função que retorna a instância singleton da classe.
    """
    instances: Dict[Type[T], T] = {}

    def instance() -> T:
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return instance


@singleton
class FirefoxWebDriverFactory:
    """
    Classe Factory responsável por criar o WebDriver do Firefox.
    """

    def __init__(self) -> None:
        """
        Inicializa a instância da classe.
        """
        self._options: Options | None = None
        self._service: Service | None = None

    def configure_options(
        self,
        headless: bool = True,
        http_proxy: Optional[str] = None,
        socks_proxy: Optional[str] = None,
        download_dir: Optional[str] = None,
        firefox_path: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> None:
        """
        Configura as Opções do WebDriver do Firefox.

        Args:
            headless (bool): Indica se o driver deve ser executado em modo headless.
            http_proxy (str): Endereço do proxy HTTP.
            socks_proxy (str): Endereço do proxy SOCKS.
            download_dir (str): Diretório de download.
            firefox_path (str): Localização do executável do Firefox.
            user_agent (str): Agente de usuário.
        """
        self._options = Options()

        if headless:
            self._options.add_argument("--headless")

        if http_proxy or socks_proxy:
            proxy_config = {
                "proxyType": ProxyType.MANUAL,
                "socksVersion": 5,
            }
            if http_proxy:
                proxy_config.update({"httpProxy": http_proxy, "sslProxy": http_proxy})
            if socks_proxy:
                proxy_config.update({"socksProxy": socks_proxy})
            self._options.proxy = Proxy(proxy_config)

        if download_dir:
            self._options.set_preference("browser.download.folderList", 2)
            self._options.set_preference("browser.download.manager.showWhenStarting", False)
            self._options.set_preference("browser.download.dir", download_dir)
            self._options.set_preference(
                "browser.helperApps.neverAsk.saveToDisk",
                "text/plain, text/csv, application/x-iso9660-image, application/octet-stream",
            )

        if firefox_path:
            self._options.binary_location = firefox_path

        if user_agent:
            self._options.set_preference("general.useragent.override", user_agent)

    def configure_service(self, geckodriver_path: Optional[str] = None) -> None:
        """
        Configura o Serviço do WebDriver do Firefox.

        Args:
            geckodriver_path (str): Localização do executável do geckodriver.
        """
        if geckodriver_path:
            self._service = Service(executable_path=geckodriver_path)
        else:
            self._service = Service()

    def create_driver(self) -> WebDriver:
        """
        Cria o WebDriver do Firefox com as opções configuradas.

        Returns:
            WebDriver: O WebDriver criado.

        Raises:
            WebDriverException: Se o WebDriver não puder ser criado.
        """
        try:
            if self._options is None:
                self.configure_options()

            if self._service is None:
                self.configure_service()

            driver = Firefox(service=self._service, options=self._options)

            return driver

        except WebDriverException as e:
            raise WebDriverException(f"Erro ao criar o WebDriver do Firefox: {e}") from e


def configure_firefox(
    headless: bool = True,
    http_proxy: Optional[str] = None,
    socks_proxy: Optional[str] = None,
    download_dir: Optional[str] = None,
    firefox_path: Optional[str] = None,
    user_agent: Optional[str] = None,
    geckodriver_path: Optional[str] = None,
) -> None:
    """
    Configura as opções do WebDriver do Firefox.

    Args:
        headless (bool): Indica se o driver deve ser executado em modo headless.
        http_proxy (str): Endereço do proxy HTTP.
        socks_proxy (str): Endereço do proxy SOCKS.
        download_dir (str): Diretório de download.
        firefox_path (str): Localização do executável do Firefox.
        user_agent (str): Agente de usuário.
        geckodriver_path (str): Localização do executável do geckodriver.
    """
    firefox_webdriver_factory = FirefoxWebDriverFactory()
    firefox_webdriver_factory.configure_options(
        headless=headless,
        http_proxy=http_proxy,
        socks_proxy=socks_proxy,
        download_dir=download_dir,
        firefox_path=firefox_path,
        user_agent=user_agent,
    )

    firefox_webdriver_factory.configure_service(geckodriver_path=geckodriver_path)


@contextmanager
def get_firefox_driver():
    """
    Context Manager para criar e gerenciar o WebDriver do Firefox.

    Este contexto manager cria um WebDriver do Firefox com as opções configuradas
    e o fecha automaticamente ao final do escopo.

    Yields:
        WebDriver: O WebDriver criado.

    Raises:
        Exception: Se o WebDriver não puder ser criado.
    """
    with lock:
        try:
            firefox_webdriver_factory = FirefoxWebDriverFactory()
            driver = firefox_webdriver_factory.create_driver()

            yield driver

        except WebDriverException as e:
            raise Exception(f"Failed to create Firefox WebDriver: {e}") from e

        finally:
            if driver:
                driver.quit()
