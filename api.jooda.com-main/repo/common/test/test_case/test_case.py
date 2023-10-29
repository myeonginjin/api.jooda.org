from django.conf import settings
from django.test import Client, TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from common.test import test_response


class JoodaTestCase(TestCase):
    client = Client()
    image = SimpleUploadedFile(
        name="test.png",
        content=open("static/test_image.png", "rb").read(),
        content_type="image/jpeg",
    )

    def api_get(self, data=None, headers=None):
        return self.client.get(
            self.api_url,
            data,
            **self.headers if headers is None else headers,
        )

    def api_post(self, data=None, headers=None):
        return self.client.post(
            self.api_url,
            data,
            **self.headers if headers is None else headers,
        )

    def api_patch(self, data=None, headers=None):
        return self.client.patch_multipart(
            self.api_url,
            data,
            **self.headers if headers is None else headers,
        )

    def get_content_from_response(self, response) -> any:
        return test_response.get_content_from_response(response)

    def assertValidatePayload(self, serializer_class, response) -> None:
        self.assertTrue(
            test_response.check_payload_validate_value(serializer_class, response)
        )
