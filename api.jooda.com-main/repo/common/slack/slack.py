import requests, json
import logging

from django.conf import settings
from common.enums import SlackChannel
from common.singleton_instance import SingletonInstance


logger = logging.getLogger("api")


class Slack(SingletonInstance):
    def __init__(self, channel=None):
        self.slack_post_uri = "https://slack.com/api/chat.postMessage"
        self.headers = {"Authorization": "Bearer " + settings.SLACK_TOKEN}
        self.channel = SlackChannel.DEV if settings.DEBUG else channel

    def slack_post_texts(self, text=None):
        try:
            requests.post(
                self.slack_post_uri,
                headers=self.headers,
                data=self.create_data(self.channel, text=text),
            )

        except Exception as e:
            logger.error(
                f"slack post message error occur, (channel : {self.channel}, text : {text}, error : {e})"
            )

    def slack_post_attachments(self, attachments=None):
        try:
            if not settings.TEST:
                requests.post(
                    self.slack_post_uri,
                    headers=self.headers,
                    data=self.create_data(self.channel, attachments=attachments),
                )

        except Exception as e:
            logger.error(
                f"slack post message error occur, (channel : {self.channel}, error : {e})"
            )

    def set_channel(self, channel):
        self.channel = channel

    @staticmethod
    def create_data(channel, text=None, attachments=None) -> json:
        result = {"channel": channel, "text": text}

        if attachments:
            result["attachments"] = json.dumps(attachments)
        return result
