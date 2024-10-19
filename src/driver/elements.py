class ClassElement:
    ticket_class = 'rn-bb03'
    seat_array = 'divSeatArray'


class XpathElement:
    login_id = '//*[@id="SMemberID"]'
    login_pw = '//*[@id="SMemberPassword"]'
    login_btn = '//*[@id="btnLogin"]'

    login_captcha_img = '//*[@id="yesCaptchaImage"]'  # 로그인 캡차 이미지
    login_captcha_input = '//*[@id="txtCaptcha"]'     # 로그인 캡차 입력창
    pay_captcha_img = '//*[@id="yesCaptchaImage"]'    # 결제 캡차 이미지
    pay_captcha_input = '//*[@id="txtCaptcha"]'       # 결제 캡차 입력창

    performance_time = '//li[contains(@timeoption, "2")]'  # 공연 시간 리스트

    minimap = '//*[@id="dMapInfo"]/map'  # 미니맵 구역
    seat_select = '//*[@id="btnSeatSelect"]'  # 좌석 선택 버튼
    seat_grade = '//p[contains(@name, "btnGrade")]'  # 좌석 등급 리스트
    seat_area = '//li[contains(@style, "cursor:pointer;") and contains(text(), "구역")]'  # 좌석 구역 리스트
    available_seat = '//*[contains(@name, "tk") and not(contains(@class, "s13"))]'  # 예매 가능 좌석 리스트
    seat_select_complete = '//*[@id="form1"]/div[3]/div[2]/div/div[2]/p[2]/a'  # 좌석 선택 완료 버튼

    step3_next = '//*[@id="StepCtrlBtn03"]/a[2]'   # step3 할인 정보 선택 후 다음 단계 버튼
    step4_next = '//*[@id="StepCtrlBtn04"]/a[2] '  # step4 수령 방법 입력 후 다음 단계 버튼

    bank_select = '//*[@id="selBank"]'           # 은행 선택 드랍 다운 메뉴
    kb_bank = '//*[@id="selBank"]/option[2]'     # 국민은행
    ibk_bank = '//*[@id="selBank"]/option[3]'    # 기업은행
    nh_bank = '//*[@id="selBank"]/option[4]'     # 농협
    sh_bank = '//*[@id="selBank"]/option[5]'     # 신한은행
    woori_bank = '//*[@id="selBank"]/option[6]'  # 우리은행
    post_bank = '//*[@id="selBank"]/option[7]'   # 우체국
    hana_bank = '//*[@id="selBank"]/option[8]'   # 하나은행
    sc_bank = '//*[@id="selBank"]/option[9]'     # SC은행

    account_button = '//*[@id="rdoPays22"]'       # 무통장 입금 라디오 버튼
    all_agree_button = '//*[@id="cbxAllAgree"]'   # 전체 동의 체크박스
    pay_button = '//*[@id="StepCtrlBtn05"]/a[2]'  # 결제하기 버튼
