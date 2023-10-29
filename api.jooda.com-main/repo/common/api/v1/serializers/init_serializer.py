from apps.accounts.models import Account
from apps.churchs.models import ChurchMember
from common import enums


class InitSerializer:
    def __new__(self, account, church_member):
        payload = {}
        payload["account_info"] = self.get_account_info(account)
        payload["church_info"] = self.get_church_info(church_member)

        return payload

    def get_account_info(account: Account) -> dict:
        return {
            "account_state": getattr(account, "state", enums.ChurchMemberState.VISITOR),
            "account_name": getattr(account, "name", None),
            "account_gender": getattr(account, "gender", None),
            "account_birth_date": getattr(account, "birth_date", None),
            "account_phone_number": getattr(account, "phone_number", None),
        }

    def get_church_info(church_member_list: ChurchMember) -> list:
        return [
            {
                "church_id": church_member.church.id,
                "member_state": church_member.state,
            }
            for church_member in church_member_list
        ]
