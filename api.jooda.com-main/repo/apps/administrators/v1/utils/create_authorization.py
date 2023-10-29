from django.utils import timezone
from common import slack, enums
from common.utils import secure


def create_authorization(data):
    try:
        return secure.encrypte_data(data + str(timezone.now()))
    except Exception as e:
        slacks = slack.Slack(enums.SlackChannel.ERROR_LOG)
        slacks.slack_post_texts(f"관리자 계정 토큰 생성 실패, error : {e}")
        return "temporary_token"
