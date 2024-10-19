from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from ..driver import ChromeDriver
from ..driver.elements import XpathElement as XE


class DateTimeSelector(ChromeDriver):
    def __init__(self, driver: Chrome):
        super().__init__(driver)
        self.success = False

    def select_date_time(self, wish_date: str, wish_time: str = None):
        """
        공연 날짜와 시간 선택 함수

        Args:
            wish_date (str): 원하는 날짜
            wish_time (str): 원하는 시간대

        Returns:
            performance_date (str): 선택한 날짜
            performance_time (str): 선택한 시간대
        """

        # 공연 날짜 선택
        performance_date = self.select_date(wish_date)
        if not performance_date:
            print(f'해당 날짜 ({wish_date})에 공연이 없습니다.')
            return None, None

        # 공연 시간 선택
        performance_time = self.select_time(wish_time)
        if not performance_time:
            print(f'해당 시간 ({wish_time})에 공연이 없습니다.')
            return None, None

        return performance_date, performance_time

    def select_date(self, wish_date: str):
        """
        공연 날짜 선택 함수

        Args:
            wish_date (str): 원하는 날짜

        Returns:
            performance_date (str): 선택한 날짜
        """

        try:
            performance_date_xpath = f'//*[@id="{wish_date}"]'
            performance_date_element = self.driver.find_element(By.XPATH, performance_date_xpath)
        except NoSuchElementException:
            return False

        performance_date = performance_date_element.get_attribute('title')

        if performance_date != wish_date:
            return False

        performance_date_element.click()
        return performance_date

    def select_time(self, wish_time: str = None):
        """
        공연 시간 선택 함수

        Args:
            wish_time (str): 원하는 시간대

        Returns:
            performance_time (str): 선택한 시간대
        """

        for performance_time_element in self.get_list_elements_by_xpath(XE.performance_time):
            performance_time = performance_time_element.get_attribute('timeinfo')
            if wish_time and wish_time != performance_time:
                continue

            # 선택한 시간대 클릭
            performance_time_element.click()

            # 좌석 선택 버튼 클릭
            self.wait_until_element_load(XE.seat_select, By.XPATH)
            self.driver.find_element(By.XPATH, XE.seat_select).click()

            # 좌석 선택 IFrame 이동
            iframe = self.wait_until_element_load(target="ifrmSeatFrame", by=By.NAME)
            self.driver.implicitly_wait(1)
            self.driver.switch_to.frame(iframe)  # 예매 iframe으로 이동

            return performance_time
