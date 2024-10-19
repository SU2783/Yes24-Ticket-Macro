from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.common import NoAlertPresentException

from ..driver import ChromeDriver
from ..driver.elements import ClassElement as CE
from ..driver.elements import XpathElement as XE
from ..helper.seat_checker import is_valid_seat, is_valid_seat_list, is_valid_seat_area, is_valid_seat_grade


class SeatSelector(ChromeDriver):
    def __init__(self,
                 driver: Chrome,
                 wish_grades: list[str] = None,
                 wish_areas: list[str] = None,
                 num_of_tickets: int = 1,
                 adjacent_seats: bool = False,
                 ):
        super().__init__(driver)

        self.wish_grades = wish_grades
        self.wish_areas = wish_areas
        self.num_of_tickets = num_of_tickets
        self.adjacent_seats = adjacent_seats

        self.success = False
        self.current_grade = None

    def select_minimap(self):
        """ 미니맵을 조회하고 좌석을 선택하는 함수 """
        
        # 미니맵이 로드될 때까지 대기
        self.wait_until_minimap_load()

        # 미니맵 선택
        for minimap_area_element in self.driver.find_elements(By.TAG_NAME, 'area'):
            minimap_area = minimap_area_element.get_attribute('id')
            minimap_area_element.click()
            # print('미니맵 구역:', minimap_area)

            # 좌석 선택
            self.select_seat()

            # 좌석 선택이 완료되면 종료
            if self.success:
                return True

        return False

    def select_seat_table(self):
        """ 좌석 테이블을 조회하고 좌석을 선택하는 함수 """

        # 좌석 등급 조회
        for seat_grade_element in self.get_list_elements_by_xpath(XE.seat_grade):
            seat_grade = seat_grade_element.text.split()[0]
            # print('좌석 등급:', seat_grade)

            # 좌석 등급이 유효하지 않으면 다음 좌석 등급 조회
            if not is_valid_seat_grade(seat_grade, self.wish_grades):
                continue

            # 조회된 좌석 등급 탭을 한번 더 클릭하면 좌석 구역 리스트가 숨겨져
            # 좌석 구역을 조회할 수 없는 문제가 있어서
            # 조회한 좌석 등급이 현재 좌석 등급과 다를 때만 좌석 등급 탭 클릭
            if self.current_grade != seat_grade:
                seat_grade_element.click()
                self.current_grade = seat_grade

            # 좌석 구역 선택
            self.select_seat_area()

            if self.success:
                return True

        return False

    def select_seat_area(self):
        """ 좌석 구역을 조회하는 함수 """

        # 좌석 구역 조회
        for seat_area_element in self.get_list_elements_by_xpath(XE.seat_area):
            seat_area = seat_area_element.text
            # print('좌석 구역:', seat_area)

            # 좌석 구역이 유효하지 않으면 다음 좌석 구역 조회
            if not is_valid_seat_area(seat_area, self.wish_areas):
                continue

            # 좌석 구역 선택 후 좌석 선택
            seat_area_element.click()
            self.select_seat()

            if self.success:
                return

    def select_seat(self):
        """ 좌석을 선택하는 함수 """

        # 좌석 선택 창이 로드될 때까지 대기
        seat_array = self.wait_until_element_load(target=CE.seat_array, by=By.ID)

        # 예매 가능한 좌석 리스트 조회
        selected_seat_list = []
        seat_list = seat_array.find_elements(By.XPATH, XE.available_seat)

        for seat in seat_list:
            # 선택한 좌석이 유효하면 좌석 추가
            if is_valid_seat(seat, self.wish_grades, self.wish_areas):
                seat.click()
                seat_title = seat.get_attribute('title')
                selected_seat_list.append(seat_title)
                print(selected_seat_list, "선택됨")

            # 선택한 좌석 리스트가 유효하면 좌석 선택 완료
            if is_valid_seat_list(selected_seat_list, self.num_of_tickets, self.adjacent_seats):
                self.complete_seat_selection()

            # 좌석 선택이 완료되면 종료
            if self.success:
                return

    def wait_until_minimap_load(self):
        """ 미니맵이 로드될 때까지 대기하는 함수 """

        while True:
            if len(self.driver.find_elements(By.TAG_NAME, "area")) >= 1:
                break

            self.driver.implicitly_wait(0.1)

    def complete_seat_selection(self):
        """ 좌석 선택을 완료하는 함수 """

        # 좌석 선택 완료 버튼 클릭
        self.driver.find_element(By.XPATH, XE.seat_select_complete).click()

        # 경고 창 (다른 사람이 결제 중인 좌석입니다.) 뜨면 확인
        try:
            if expected_conditions.alert_is_present():
                self.driver.switch_to.alert.accept()

        # 경고 창이 뜨지 않는다면 예매 완료
        except NoAlertPresentException:
            self.success = True
