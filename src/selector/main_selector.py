import time
from datetime import datetime, timedelta

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.common import NoSuchElementException

from config import Config
from ..driver import ChromeDriver
from ..driver.elements import ClassElement as CE
from ..driver.elements import XpathElement as XE

from ..helper.captcha_reader import CaptchaReader
from ..selector import DateTimeSelector, SeatSelector


class MainSelector(ChromeDriver):
    def __init__(self,
                 driver: Chrome = None,
                 wish_date: str = None,
                 wish_time: str = None,
                 **kwargs,
                 ):
        super().__init__(driver, **kwargs)

        self.date_time_controller = DateTimeSelector(self.driver)
        self.seat_controller = SeatSelector(
            self.driver,
            wish_grades=Config.wish_grades,
            wish_areas=Config.wish_areas,
            num_of_tickets=Config.num_of_tickets,
            adjacent_seats=Config.adjacent_seats,
        )
        self.captcha_reader = CaptchaReader()

        self.wish_date = wish_date
        self.wish_time = wish_time

    def run(self):
        # 로그인
        self.login()

        # 예매 페이지로 이동
        self.driver.get(Config.ticket_page_url)

        # 예매 버튼 대기
        ticket_button = self.wait_until_ticket_open(ready_seconds=3)

        # 예매 버튼 클릭
        ticket_button.click()

        # 예매 창 대기
        self.wait_until_reservation_window_open()

        # 예매 창으로 전환
        self.switch_to_reservation_window()

        # 예매 진행
        self.make_reservation()

    def make_reservation(self):
        """ 예매 진행 함수 """

        # 공연 날짜 및 시간 선택
        perform_date, perform_time = self.date_time_controller.select_date_time(self.wish_date, self.wish_time)
        if not perform_date or not perform_time:
            return

        print('공연 날짜:', perform_date, '공연 시간:', perform_time)

        # 좌석 선택
        use_minimap = self.driver.find_elements(By.XPATH, XE.minimap)
        while True:
            # 미니맵 선택
            if use_minimap:
                success = self.seat_controller.select_minimap()

            # 구역 선택
            else:
                success = self.seat_controller.select_seat_table()

            # 좌석 선택 완료 시 결제 진행
            if success:
                self.pay()
                break

    def login(self):
        """ 로그인 함수 """

        # 로그인 정보
        yes24_id = Config.yes24_id
        yes24_pw = Config.yes24_pw

        # 로그인 페이지 이동
        self.driver.get('https://www.yes24.com/Templates/FTLogin.aspx?')

        # 로그인 정보 입력
        self.driver.find_element(By.XPATH, XE.login_id).send_keys(yes24_id)
        self.driver.find_element(By.XPATH, XE.login_pw).send_keys(yes24_pw)
        self.driver.find_element(By.XPATH, XE.login_btn).click()

        # 캡챠 이미지가 뜨는지 확인
        try:
            # 캡챠 이미지가 뜨면
            while self.driver.find_element(By.XPATH, XE.login_captcha_img):
                # 캡챠 이미지 찾기
                captcha_image_element = self.driver.find_element(By.XPATH, XE.login_captcha_img)

                # OCR로 캡챠 이미지 읽기
                captcha_number = self.captcha_reader.read(captcha_image_element.screenshot_as_png)

                # 캡챠 번호 입력
                self.driver.find_element(By.XPATH, XE.login_captcha_input).send_keys(captcha_number)

                # 로그인 버튼 클릭
                self.driver.find_element(By.XPATH, XE.login_btn).click()
                time.sleep(1)

        # 캡챠 이미지가 뜨지 않을 경우 NoSuchElementException 발생
        except NoSuchElementException:
            self.driver.implicitly_wait(1)

    def pay(self):
        """ 좌석 선택 완료 후 결제 진행 함수 """

        # default iframe으로 이동
        self.driver.switch_to.default_content()
        time.sleep(1)

        # step3 할인 정보 선택
        self.driver.find_element(By.XPATH, XE.step3_next).click()
        time.sleep(3)

        # step4 수령 방법 선택 (주문자 정보와 배송지 정보를 미리 입력 해두지 않을 경우 다음 단계로 넘어가지 않을 수도 있음)
        self.driver.find_element(By.XPATH, XE.step4_next).click()
        time.sleep(3)

        # step5 결제 정보 입력
        # 무통장 입금 선택
        self.driver.find_element(By.XPATH, XE.account_button).click()
        time.sleep(1)

        # 은행 선택 드랍 다운 메뉴 클릭
        self.driver.find_element(By.XPATH, XE.bank_select).click()
        time.sleep(1)

        # 은행 선택
        self.driver.find_element(By.XPATH, XE.woori_bank).click()
        time.sleep(1)

        # 전체 동의 버튼 클릭
        self.driver.find_element(By.XPATH, XE.all_agree_button).click()
        time.sleep(1)

        # 결제 버튼 클릭
        self.driver.find_element(By.XPATH, XE.pay_button).click()

        # 캡챠 이미지가 뜨는지 확인
        try:
            while self.driver.find_element(By.XPATH, XE.pay_captcha_img):
                # 캡챠 이미지 찾기
                captcha_image_element = self.driver.find_element(By.XPATH, XE.pay_captcha_img)

                # OCR로 캡챠 이미지 읽기
                captcha_number = self.captcha_reader.read(captcha_image_element.screenshot_as_png)

                # 캡챠 번호 입력
                self.driver.find_element(By.XPATH, XE.pay_captcha_input).send_keys(captcha_number)

                # 결제 버튼 클릭
                self.driver.find_element(By.XPATH, XE.pay_button).click()
                time.sleep(1)

        # 캡챠 이미지가 뜨지 않을 경우 NoSuchElementException 발생
        except NoSuchElementException:
            self.driver.implicitly_wait(1)

        # # 예매 완료 메시지
        # notice_message(
        #     title='예매 완료',
        #     text='예매가 완료되었습니다. 예매 내역을 확인해 주세요.',
        # )

        # 크롬 드라이버 종료
        self.driver.quit()


    def wait_until_ticket_open(self, ready_seconds: int = 3):
        """ 예매 버튼이 활성화 될 때까지 대기하는 함수 """
        ticket_open_date = Config.ticket_open_date
        ticket_open_time = Config.ticket_open_time

        while True:
            current_time = datetime.utcnow() + timedelta(hours=9)
            ready_time = current_time + timedelta(seconds=ready_seconds)
            ticket_time = datetime.strptime(f'{ticket_open_date} {ticket_open_time}', '%Y-%m-%d %H:%M:%S')

            if  ready_time >= ticket_time:
                break

        self.driver.get(Config.ticket_page_url)
        self.driver.implicitly_wait(1)

        ticket_button = self.wait_until_element_load(CE.ticket_class, By.CLASS_NAME)
        return ticket_button

    def wait_until_reservation_window_open(self):
        """ 새로운 예매 창이 뜰 때까지 대기하는 함수 """
        while True:
            if len(self.driver.window_handles) >= 2:
                break

            self.driver.implicitly_wait(1)

    def switch_to_reservation_window(self):
        """ 새로운 예매 창으로 전환하는 함수 """
        reservation_window = self.driver.window_handles[1]
        self.driver.switch_to.window(reservation_window)
        time.sleep(1)