from typing import List

korean = ['가', '나', '다', '라', '마', '바', '사', '아', '자', '차', '카', '타', '파', '하']
english = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

string_to_number = {k: i for i, k in enumerate(korean, 1)}
string_to_number.update({k: i for i, k in enumerate(english, 1)})


def is_valid_seat(seat, wish_grades: List[str] = None, wish_areas: List[int] = None):
    """
    좌석 정보가 유효한지 확인하는 함수
    선택한 좌석의 정보가 없거나,
    원하는 좌석 등급이 아니거나,
    원하는 좌석 구역이 아닌 경우 False를 리턴

    Args:
        seat: 좌석 WebElement
        wish_grades (List[str]): 원하는 좌석 등급 리스트
        wish_areas (List[str]): 원하는 좌석 구역 리스트

    Returns:
        bool: 좌석 정보가 유효한 경우 True, 그렇지 않은 경우 False

    """
    seat_title = seat.get_attribute('title')
    seat_grade = seat.get_attribute('grade')

    # 좌석 정보가 없는 경우 리턴
    if not seat_title or not seat_grade:
        print("좌석 정보가 없습니다")
        return False

    # 원하는 좌석 등급이 아닌 경우 리턴
    if not is_valid_seat_grade(seat_grade, wish_grades):
        print(f"원하는 좌석 등급이 아닙니다. 선택 좌석 등급: {seat_grade} | 원하는 좌석 등급: {wish_grades}")
        return False

    # 원하는 좌석 구역이 아닌 경우 리턴
    floor, seat_area, seat_number = seat_title.split(" ")

    if '구역' in floor or '블록' in floor:
        seat_area = floor
    elif '구역' in seat_area or '블록' in seat_area:
        seat_area = seat_area

    if not is_valid_seat_area(seat_area, wish_areas):
        print(f"원하는 좌석 구역이 아닙니다. 선택 좌석 구역: {seat_area} | 원하는 좌석 구역: {wish_areas}")
        return False

    return True


def is_valid_seat_list(seat_list, num_of_tickets: int, adjacent_seats: bool):
    """
    선택한 좌석 리스트가 유효한지 확인하는 함수
    선택한 좌석의 수가 원하는 좌석 수보다 적거나,
    인접한 좌석을 원하는데 인접한 좌석이 아닌 경우 False를 리턴

    Args:
        seat_list (List[str]): 선택한 좌석 리스트
        num_of_tickets (int): 원하는 좌석 수
        adjacent_seats (bool): 인접한 좌석 여부

    Returns:
        bool: 선택한 좌석 리스트가 유효한 경우 True, 그렇지 않은 경우 False
    """

    # 선택한 좌석이 원하는 좌석 수보다 적은 경우 리턴
    if len(seat_list) < num_of_tickets:
        return False

    # 인접한 좌석을 원하는 경우
    if adjacent_seats:
        selected_seat_area = None
        selected_seat_number = None

        for i, seat_title in enumerate(seat_list):
            floor, seat_area, seat_number = seat_title.split(" ")
            seat_number = int(seat_number.replace("번", ""))

            if i != 0:
                # 좌석 구역 체크 (같은 구역 및 열이 아닌 경우 리턴)
                if selected_seat_area != seat_area:
                    print("좌석 구역 및 열이 다릅니다", seat_list)
                    return False

                # 좌석 번호 체크 (인접한 좌석이 아닌 경우 리턴)
                if abs(seat_number - selected_seat_number) != 1:
                    print("인접한 좌석이 아닙니다", seat_list)
                    return False

            selected_seat_area = seat_area
            selected_seat_number = seat_number
            continue

    return True

def is_valid_seat_grade(seat_grade: str, wish_grades: List[str] = None):
    """
    선택한 좌석 등급이 유효한지 확인하는 함수

    Args:
        seat_grade (str): 선택한 좌석 등급
        wish_grades (List[str]): 원하는 좌석 등급 리스트

    Returns:
        bool: 선택한 좌석 등급이 원하는 좌석 등급이면 True, 그렇지 않으면 False
    """

    if not wish_grades:
        return True

    if seat_grade not in wish_grades:
        return False

    return True

def is_valid_seat_area(seat_area: str, wish_areas: List[int] = None):
    """
    선택한 좌석 구역이 유효한지 확인하는 함수

    Args:
        seat_area (str): 선택한 좌석 구역
        wish_areas (List[int]): 원하는 좌석 구역 리스트

    Returns:
        bool: 선택한 좌석 구역이 원하는 좌석 구역이면 True, 그렇지 않으면 False
    """

    if not wish_areas:
        return True

    # 좌석 구역 전처리
    seat_area = seat_area.split("구역")[0]
    seat_area = seat_area.split("블록")[0]
    seat_area = seat_area.lower()

    # 구역명이 문자열로 되어 있는 경우 숫자로 변환
    seat_area = string_to_number.get(seat_area, seat_area)
    seat_area = int(seat_area)

    # 원하는 좌석 구역이 아닌 경우 리턴
    if seat_area not in wish_areas:
        return False

    return True
