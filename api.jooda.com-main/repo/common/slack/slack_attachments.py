from common.slack import Slack
from django.conf import settings
from apps.accounts.models import Account
from apps.churchs.models import Church


class SlackAttachments(Slack):
    base_url = (
        f"http://dev-api.jooda.org/admin-jooda/"
        if settings.DEBUG
        else f"http://api.jooda.org/admin-jooda/"
    )

    def request_registering_church(self, church: Church) -> None:
        attachment = [
            {
                "title": "[🥳 교회 등록 요청 🚩]",
                "fields": [
                    {
                        "title": "교회 명",
                        "value": church.name,
                        "short": True,
                    },
                    {
                        "title": "담당자 연락처",
                        "value": church.contact_number,
                        "short": True,
                    },
                    {
                        "title": "교회 주소",
                        "value": church.address,
                    },
                ],
                "fallback": "교회 등록 요청이 들어왔습니다!",
                "color": "#5400DD",
                "attachment_type": "default",
                "actions": [
                    {
                        "name": "pioneer",
                        "text": "교회 검수하기",
                        "type": "button",
                        "url": f"{self.base_url}churchs/",
                    },
                ],
            }
        ]
        self.slack_post_attachments(attachment)

    def duplicated_phone_number(
        self, wait_for_account: Account, in_active_account: Account
    ) -> None:
        attachment = [
            {
                "title": "[😶‍🌫️ 같은 전화번호 계정 발생👾]",
                "fields": [
                    {
                        "title": "중복된 전화 번호",
                        "value": in_active_account.phone_number,
                    },
                    {
                        "title": "비활성화 된 계정",
                        "value": in_active_account.name,
                        "short": True,
                    },
                    {
                        "title": "비활성화 된 계정, 생년월일",
                        "value": in_active_account.birth_date,
                        "short": True,
                    },
                    {
                        "title": "비활성화 된 계정, 회원가입 날짜",
                        "value": str(in_active_account.created_at),
                        "short": True,
                    },
                    {
                        "title": "비활성화 된 계정, 회원 상태",
                        "value": in_active_account.state,
                        "short": True,
                    },
                    {
                        "title": "등록 대기 중인 계정",
                        "value": wait_for_account.name,
                    },
                    {
                        "title": "등록 대기 중인 계정, 생년월일",
                        "value": wait_for_account.birth_date,
                    },
                    {
                        "title": "등록 대기 중인 계정, 회원가입 날짜",
                        "value": str(wait_for_account.created_at),
                    },
                    {
                        "title": "등록 대기 중인 계정, 회원 상태",
                        "value": wait_for_account.state,
                    },
                ],
                "fallback": "같은 전화번호의 계정이 생겼어요 !",
                "color": "#5400DD",
                "attachment_type": "default",
                "actions": [
                    {
                        "name": "pioneer",
                        "text": "계정 검수하기",
                        "type": "button",
                        "url": f"{self.base_url}accounts/",
                    },
                ],
            }
        ]
        self.slack_post_attachments(attachment)
