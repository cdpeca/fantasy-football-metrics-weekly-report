__author__ = "Wren J. R. (uberfastman)"
__email__ = "uberfastman@uberfastman.dev"

import json
import logging
from asyncio import Future
from datetime import datetime
from pathlib import Path
from typing import Union

from colorama import Fore, Style
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_sdk.web.base_client import SlackResponse

from integrations.base.integration import BaseIntegration
from utilities.logger import get_logger
from utilities.settings import settings

logger = get_logger(__name__, propagate=False)

# Suppress verbose slack debug logging
logging.getLogger("slack.web.slack_response").setLevel(level=logging.INFO)
logging.getLogger("slack.web.base_client").setLevel(level=logging.INFO)


class SlackIntegration(BaseIntegration):

    def __init__(self):
        self.root_dir = Path(__file__).parent.parent
        super().__init__("slack")

    def _authenticate(self) -> None:

        if not settings.integration_settings.slack_auth_token:
            settings.integration_settings.slack_auth_token = input(
                f"{Fore.GREEN}What is your Slack authentication token? -> {Style.RESET_ALL}"
            )
            settings.write_settings_to_env_file(self.root_dir / ".env")

        self.client = WebClient(token=settings.integration_settings.slack_auth_token)

    def api_test(self):
        logger.debug("Testing Slack API.")
        try:
            return self.client.api_test()
        except SlackApiError as e:
            logger.error(f"Slack client error: {e}")

    def _list_channels(self) -> Union[Future, SlackResponse]:
        """Required Slack app scopes: channels:read, groups:read, mpim:read, im:read
        """
        logger.debug("Listing Slack channels.")
        try:
            return self.client.conversations_list(types="public_channel,private_channel")
        except SlackApiError as e:
            logger.error(f"Slack client error: {e}")

    def _get_channel_id(self, channel_name: str) -> str:
        for channel in self._list_channels().get("channels"):
            if channel.get("name") == channel_name:
                return channel.get("id")
        raise ValueError(f"Channel {channel_name} not found.")

    def post_message(self, message: str) -> Union[Future, SlackResponse]:
        logger.debug(f"Posting message to Slack: \n{message}")

        try:
            return self.client.chat_postMessage(
                channel=self._get_channel_id(settings.integration_settings.slack_channel),
                text=f"<!here>:\n{message}",
                username="ff-report",
                # uncomment the icon_emoji parameter if you wish to choose an icon emoji to be your app icon, otherwise
                # it will default to whatever icon you have set for the app
                # icon_emoji=":football:"
            )
        except SlackApiError as e:
            logger.error(f"Slack client error: {e}")

    def upload_file(self, file_path: Path) -> Union[Future, SlackResponse]:
        logger.debug(f"Uploading file to Slack: \n{file_path}")

        try:
            message = (
                f"\nFantasy Football Report for {file_path.name}\n"
                f"Generated {datetime.now():%Y-%b-%d %H:%M:%S}\n"
            )

            file_for_upload: Path = self.root_dir / file_path
            with open(file_for_upload, "rb") as uf:

                if settings.integration_settings.slack_channel_notify_bool:
                    # post message with no additional content to trigger @here
                    self.post_message("")

                response = self.client.files_upload_v2(
                    channel=self._get_channel_id(settings.integration_settings.slack_channel),
                    filename=file_for_upload.name,
                    file=uf.read(),
                    initial_comment=message
                )

            return response
        except SlackApiError as e:
            logger.error(f"Slack client error: {e}")


if __name__ == "__main__":
    reupload_file = Path(__file__).parent.parent / settings.integration_settings.reupload_file_path

    logger.info(f"Re-uploading {reupload_file.name} ({reupload_file}) to Slack...")

    slack_integration = SlackIntegration()

    # logger.info(f"\n{json.dumps(slack_integration.api_test().data, indent=2)}")
    # logger.info(f"{json.dumps(slack_integration.post_message('test message').data, indent=2)}")
    logger.info(f"{json.dumps(slack_integration.upload_file(reupload_file).data, indent=2)}")