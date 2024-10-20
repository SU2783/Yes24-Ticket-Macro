import sys
from threading import Thread

from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException, NoSuchElementException, UnexpectedAlertPresentException


class ChromeDriver(Thread):
    def __init__(self,
                 driver: Chrome = None,
                 **kwargs,
                 ):
        super().__init__()

        if driver is None:
            driver = Chrome(
                service=Service(ChromeDriverManager().install()),
                options=ChromeDriverOptions(**kwargs),
            )

        self.driver = driver

    def check_if_element_exists(self, by: str, target: str):
        """
        웹페이지의 특정 element가 존재하는지 확인하는 함수

        Args:
            by (str): 원하는 요소의 식별자
            target (str): 원하는 요소의 locator (By.XPATH, By.ID 등등)

        Returns:
            element: 원하는 웹페이지의 element 객체.
                     만약 요소가 존재하지 않으면 None 반환.
                     경고창이 뜨면 'alert' 반환.
        """

        try:
            return self.driver.find_element(by, target)

        except NoSuchElementException:
            return None

        except UnexpectedAlertPresentException:
            return 'alert'

    def wait_until_element_load(self,
                                target: str,
                                by: str,
                                timeout: float = 5.0,
                                retry: int = sys.maxsize,
                                ):
        """
        웹페이지의 특정 element가 로드될 때까지 대기하는 함수

        Args:
            target (str): 원하는 요소의 식별자
            by (str): 원하는 요소의 locator (By.XPATH, By.ID 등등)
            timeout (float): 대기 시간
            retry (int): 재시도 횟수

        Returns:
            element: 원하는 웹페이지의 element 객체
        """

        element = None
        method = expected_conditions.presence_of_element_located((by, target))

        while retry:
            try:
                element = WebDriverWait(self.driver, timeout).until(method)
                break

            except TimeoutException:
                print("시간 초과")
                self.driver.refresh()
                retry -= 1

        return element

    def get_list_elements_by_xpath(self, xpath: str):
        """
        웹페이지의 여러 요소들을 가져오는 제너레이터

        Args:
            xpath (str): 원하는 요소의 xpath 식별자

        Returns:
            generator: 원하는 요소 객체
        """

        for xpath_element in self.driver.find_elements(By.XPATH, xpath):
            yield xpath_element

    def switch_window(self, window_index: int):
        """
        웹페이지의 창을 전환하는 함수

        Args:
            window_index (int): 전환할 창의 인덱스
        """

        reservation_window = self.driver.window_handles[window_index]
        self.driver.switch_to.window(reservation_window)


class ChromeDriverOptions(ChromeOptions):
    # 참고: https://with-kwang.tistory.com/82

    def __init__(self,
                 headless: bool = False,
                 disable_gpu: bool = False,
                 maximize_window: bool = False,
                 secret_mode: bool = False,
                 ):
        super().__init__()

        self.add_argument('--no-sandbox')              # Chrome의 샌드박스 기능을 비활성화
        self.add_argument('--disable-dev-shm-usage')   # 리눅스에서 /dev/shm(공유 메모리)를 사용하지 않도록 설정
        self.add_argument('--disable-extensions')      # 확장 프로그램 비활성화
        self.add_argument('--disable-notifications')   # 브라우저 알림 비활성화
        self.add_argument('--disable-popup-blocking')  # 팝업 차단 비활성화
        self.add_argument("--disable-blink-features=AutomationControlled")  # 자동화 제어 관련 기능 비활성화
        self.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Whale/3.28.266.14 Safari/537.36")  # User-Agent 설정

        if headless:
            self.add_argument('--headless')     # headless 모드 설정
            self.add_argument('--disable-gpu')  # GPU 비활성화

        if disable_gpu:
            self.add_argument('--disable-gpu')  # GPU 비활성화

        if maximize_window:
            self.add_argument("--start-maximized")  # Chrome 창 최대화

        if secret_mode:
            self.add_argument("--incognito")  # 시크릿 모드
