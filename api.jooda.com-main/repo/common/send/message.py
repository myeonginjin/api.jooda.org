# -*- coding: utf-8 -*-
import requests
from django.conf import settings


# -> 실패 : {'result_code': -101, 'message': '받는이가 설정되지 못하였습니다.', 'error_cnt': 1}
# -> 성공 : {'result_code': '1', 'message': 'success', 'msg_id': '550820695', 'success_cnt': 1, 'error_cnt': 0, 'msg_type': 'SMS'}

send_url = "https://apis.aligo.in/send/"
MESSAGE_SERVER_KEY = "corx8nbta7v64eg75oepd62go40854sy"
MESSAGE_SERVER_ID = "uptenofficial"
MESSAGE_SENDER = "07080982535"
TEST_MODE = "Y" if settings.TEST else "N"


def authentication_message(receiver, authentication_number):
    msg = f"[주다] 회원가입 인증번호 [{authentication_number}]를 입력해 주세요."
    sms_data = {
        "key": MESSAGE_SERVER_KEY,
        "userid": MESSAGE_SERVER_ID,
        "sender": MESSAGE_SENDER,
        "receiver": receiver,  # 수신번호 (,활용하여 1000명까지 추가 가능)
        "msg": msg,
        "msg_type": "SMS",
        "testmode_yn": TEST_MODE,  # 테스트모드 적용 여부 Y/N
    }
    send_response = requests.post(send_url, data=sms_data).json()
    if send_response.get("message", None) != "success":
        raise ValueError
    return send_response
