from django.conf import settings
import requests
from common.singleton_instance import SingletonInstance


class PushNotification(SingletonInstance):
    max_num_partitions = 300

    def __init__(
        self,
        tokens: list,
        accounts: list,
        title: str,
        sub_title: str,
        _type: str,
        _id: str,
        domain: str,
        content: str = "",
        church_id: str = "",
    ) -> None:
        self.uri = f"https://push.jooda.org/api/{domain}/"
        self.tokens = [
            tokens[num * self.max_num_partitions : (num + 1) * self.max_num_partitions]
            for num in range(self.get_num_partitions(tokens))
        ]
        self.accounts = accounts
        self.title = title
        self.sub_title = sub_title
        self.content = content
        self._type = _type
        self._id = _id
        self.church_id = church_id

    def get_num_partitions(self, tokens: list) -> int:
        return (len(tokens) // self.max_num_partitions) + (
            1 if len(tokens) % self.max_num_partitions else 0
        )

    def send_push(self) -> None:
        first = True
        for tokens in self.tokens:
            try:
                requests.post(
                    self.uri,
                    json={
                        "tokens": tokens,
                        "accounts": self.accounts if first else [],
                        "title": self.title,
                        "body": self.sub_title,
                        "content": self.content,
                        "type": self._type,
                        "id": self._id,
                        "church_id": self.church_id,
                        "stage": "dev" if settings.DEBUG else "prod",
                    },
                    headers={"Content-Type": "application/json"},
                    timeout=0.3,
                )
            except requests.exceptions.ReadTimeout:
                pass
            first = False
