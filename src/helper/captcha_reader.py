import time
import torch
from easyocr import Reader

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By

from ..driver import ChromeDriver
from ..driver.elements import XpathElement as XE


class CaptchaReader(ChromeDriver):
    def __init__(self, driver: Chrome):
        super().__init__(driver)

        gpu = torch.cuda.is_available()
        self.reader = Reader(lang_list=['en'], gpu=gpu)

    def read_ocr(self, image: bytes):
        """
        OCR로 이미지를 읽는 함수

        Args:
            image (bytes): 이미지 바이트 데이터

        Returns:
            str: 이미지에서 읽은 텍스트

        """

        result = self.reader.readtext(image)
        return result[0][1]

    def process_captcha_image(self, captcha_image_xpath: str, captcha_input_xpath: str):
        """
        캡챠 이미지를 찾아서 처리하는 함수

        Args:
            captcha_image_xpath (str): 캡챠 이미지 xpath
            captcha_input_xpath (str): 캡챠 입력창 xpath

        Returns:
            None
        """

        # 캡챠 이미지 찾기
        captcha_image_element = self.driver.find_element(By.XPATH, captcha_image_xpath)

        # OCR로 캡챠 이미지 읽기
        captcha_number = self.read_ocr(captcha_image_element.screenshot_as_png)

        # 캡챠 번호 입력
        self.driver.find_element(By.XPATH, captcha_input_xpath).send_keys(captcha_number)

    def check_login_captcha(self):
        """ 로그인 캡챠 이미지 처리 함수 """

        # 캡챠 이미지가 있으면
        while self.check_if_element_exists(By.XPATH, XE.login_captcha_img):
            # 캡챠 이미지 처리
            self.process_captcha_image(XE.login_captcha_img, XE.login_captcha_input)

            # 로그인 버튼 클릭
            self.driver.find_element(By.XPATH, XE.login_btn).click()
            time.sleep(1)

    def check_pay_captcha(self):
        """ 결제 캡챠 이미지 처리 함수 """

        # 캡챠 이미지가 있으면 처리
        if self.check_if_element_exists(By.XPATH, XE.pay_captcha_img):
            self.process_captcha_image(XE.pay_captcha_img, XE.pay_captcha_input)

        # 결제 버튼 클릭
        self.driver.find_element(By.XPATH, XE.pay_button).click()
        time.sleep(1)
