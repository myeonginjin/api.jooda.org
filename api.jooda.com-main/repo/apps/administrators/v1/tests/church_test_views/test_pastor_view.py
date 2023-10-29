from apps.churchs.models import Church, ChurchPastor, ChurchDenomination
from common.test import test_case
from apps.administrators.v1 import serializers


class ChurchPastorViewsTest(test_case.AdministratorTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.api_url += "churchs/pastor/"
        denomination = ChurchDenomination.objects.create(name="테스트 종파")
        self.church = Church.objects.create(name="테스트 교회", denomination=denomination)
        self.administrator.church = self.church
        self.administrator.save(update_fields=["church"])
        self.church_pastor = ChurchPastor.objects.create(
            church=self.church, name="test", order=9999
        )
        self.church_pastor1 = ChurchPastor.objects.create(
            church=self.church, name="test1", role="디자이너", order=19999
        )
        self.church_pastor2 = ChurchPastor.objects.create(
            church=self.church, name="test2", role="디자이너", order=29999
        )
        self.church_pastor3 = ChurchPastor.objects.create(
            church=self.church, name="test3", role="디자이너", order=39999
        )

    def test_list(self):
        response = self.api_get()
        self.assertValidatePayload(serializers.ChurchPastorSerializer, response)

    def test_create(self):
        data = {
            "pastor_list": [
                {
                    "name": "김태정",
                    "role": "디자이너",
                },
                {
                    "name": "김태정2",
                    "role": "비서",
                    "image_state": "update",
                },
            ],
            "image_list": [self.image, self.image],
        }

        response = self.api_post(data=data)
        self.assertEqual(response.status_code, 200)

        pastors = ChurchPastor.objects.all()
        # is_image 가 false일때 이미지가 안들어가는거 체크
        self.assertEqual(pastors.get(name="김태정").image, "")
        # is_image 가 true일때 이미지가 들어가는거 체크
        self.assertTrue(len(pastors.get(name="김태정2").image.url) > 1)

        self.assertEqual(pastors.get(name="김태정").order, 49999)
        self.assertEqual(pastors.get(name="김태정2").order, 59999)

    def test_patch(self):
        data = {
            "pastor_list": [
                {
                    "church_pastor_id": f"{self.church_pastor1.id}",
                    "name": "김태정1",
                    "image_state": "update",
                },
                {
                    "church_pastor_id": f"{self.church_pastor3.id}",
                    "role": "비서",
                    "image_state": "remove",
                },
            ],
            "image_list": [self.image, self.image],
        }
        response = self.api_patch(data=data)
        self.assertEqual(response.status_code, 200)

        church_pastors = ChurchPastor.objects.all().order_by("order")

        def compare_pastors(pastor1, pastor2):
            self.assertEqual(pastor1.name, pastor2.name)
            self.assertEqual(pastor1.role, pastor2.role)
            self.assertEqual(pastor1.order, pastor2.order)

        compare_pastors(self.church_pastor, church_pastors[0])
        compare_pastors(self.church_pastor2, church_pastors[2])
        self.assertEqual(church_pastors[1].name, "김태정1")
        self.assertTrue(len(church_pastors[1].image.url) > 1)
        self.assertEqual(church_pastors[3].name, "test3")
        self.assertEqual(church_pastors[3].role, "비서")
        self.assertEqual(church_pastors[3].image, "")

    def test_delete(self):
        self.api_url += "delete/"
        data = {
            "pastor_list": [
                f"{self.church_pastor1.id}",
                f"{self.church_pastor.id}",
            ]
        }

        response = self.api_post(data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(ChurchPastor.objects.all()), 2)

    def test_change_order(self):
        self.api_url += "change_order/"
        data = {
            "church_pastor_id": f"{self.church_pastor3.id}",
            "index": 0,
        }
        response = self.api_post(data=data)

        self.assertEqual(response.status_code, 200)

        # 마지막 index 확인
        data = {
            "church_pastor_id": f"{self.church_pastor1.id}",
            "index": 4,
        }
        self.api_post(data=data)

        data = {
            "church_pastor_id": f"{self.church_pastor1.id}",
            "index": 1,
        }

        # order 초기화 확인
        for _ in range(14):
            self.api_post(data=data)
        for index, church_pastor in enumerate(
            ChurchPastor.objects.all().order_by("order")
        ):
            self.assertEqual(church_pastor.order, (index + 1) * 10000)
