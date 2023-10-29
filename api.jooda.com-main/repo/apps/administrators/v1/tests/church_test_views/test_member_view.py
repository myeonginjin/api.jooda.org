from apps.churchs.models import (
    Church,
    ChurchDenomination,
    ChurchMember,
)
from apps.accounts.models import Account
from common.test import test_case
from apps.administrators.v1 import serializers


class ChurchMemberViewsTest(test_case.AdministratorTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.api_url += "churchs/"
        denomination = ChurchDenomination.objects.create(name="테스트 종파")
        self.church = Church.objects.create(name="테스트 교회", denomination=denomination)
        self.administrator.church = self.church
        self.administrator.save(update_fields=["church"])

        for i in range(10):
            account = Account.objects.create(
                name=f"test_name_{i}",
                phone_number=f"0101234123{i}",
                birth_date="19980402",
            )
            if i < 5:
                ChurchMember.objects.create(
                    church=self.church, account=account, state="success"
                )
            else:
                ChurchMember.objects.create(
                    church=self.church, account=account, state="confirm"
                )

    def test_list(self):
        self.api_url += "member/"

        response = self.api_get()

        self.assertValidatePayload(serializers.ChurchMemberInfoSerializer, response)
        payload = self.get_content_from_response(response)
        self.assertEqual(
            payload["total_count"],
            5,
        )
        data = {"keyword": "test_name"}
        response = self.api_get(data)
        payload = self.get_content_from_response(response)
        self.assertEqual(
            payload["total_count"],
            5,
        )
        data = {"keyword": "4"}
        response = self.api_get(data)
        payload = self.get_content_from_response(response)
        self.assertEqual(
            payload["total_count"],
            1,
        )

    def test_kick_out(self):
        self.api_url += "member/kick_out/"
        church_members = ChurchMember.objects.filter(state="success")
        remove_member_ids = [church_members[0].account.id, church_members[1].account.id]
        data = {"member_list": remove_member_ids}
        self.assertEqual(church_members.count(), 5)

        response = self.api_patch(data)
        self.assertEqual(response.status_code, 200)

        changed_church_members = ChurchMember.objects.filter(state="success")
        self.assertEqual(changed_church_members.count(), 3)
        self.assertEqual(
            changed_church_members.filter(id__in=remove_member_ids).count(), 0
        )

    def test_confirm_list(self):
        self.api_url += "confirm/member/"

        response = self.api_get()
        self.assertValidatePayload(serializers.ChurchMemberInfoSerializer, response)

        payload = self.get_content_from_response(response)
        self.assertEqual(
            payload["total_count"],
            5,
        )
        data = {"keyword": "test_name"}
        response = self.api_get(data)
        payload = self.get_content_from_response(response)
        self.assertEqual(
            payload["total_count"],
            5,
        )
        data = {"keyword": "6"}
        response = self.api_get(data)
        payload = self.get_content_from_response(response)
        self.assertEqual(
            payload["total_count"],
            1,
        )

    def test_confirm_patch(self):
        self.api_url += "confirm/member/"
        confirm_members = ChurchMember.objects.filter(state="confirm")
        remove_member_ids = [
            confirm_members[0].account.id,
            confirm_members[1].account.id,
        ]
        success_member_ids = [
            confirm_members[2].account.id,
            confirm_members[3].account.id,
        ]
        reject_data = {"member_list": remove_member_ids, "member_state": "reject"}
        success_data = {"member_list": success_member_ids, "member_state": "success"}
        self.assertEqual(confirm_members.count(), 5)

        response = self.api_patch(reject_data)
        self.assertEqual(response.status_code, 200)

        changed_church_members = ChurchMember.objects.filter(state="reject")
        self.assertEqual(changed_church_members.count(), 2)
        self.assertEqual(
            changed_church_members.filter(id__in=remove_member_ids).count(), 0
        )

        response = self.api_patch(success_data)
        self.assertEqual(response.status_code, 200)
        changed_church_members = ChurchMember.objects.filter(state="success")
        self.assertEqual(changed_church_members.count(), 7)
        self.assertEqual(ChurchMember.objects.filter(state="confirm").count(), 1)
