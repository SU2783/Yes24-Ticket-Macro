import time
from itertools import product

from config import Config
from .selector import MainSelector


class Yes24Macro:
    def __init__(self, **kwargs):
        # 크롬 드라이버 옵션 (src/driver/chrome_driver.py의 ChromeDriverOptions 클래스 참고)
        self.kwargs = kwargs

    def run(self):
        if not Config.wish_times:
            Config.wish_times = [None]

        # 원하는 예매 날짜, 시간 조합으로 예매
        for wish_date, wish_time in product(Config.wish_dates, Config.wish_times):
            main_selector = MainSelector(
                wish_date=wish_date,
                wish_time=wish_time,
                **self.kwargs,
            )
            main_selector.start()
            time.sleep(1)
