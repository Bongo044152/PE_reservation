# modules/discord.py
# Discord 通知模組，用來發送訊息到 Discord Webhook
# 預設會使用 user_config 裡面的 discord_webhook 清單
# 當然也可以自行建立 DiscordNotifier 物件來使用，或修改預設的 discord_notifier

import requests
import logging
from user_config import discord_webhooks

logger = logging.getLogger(__name__)


class DiscordNotifier:
    def __init__(self, webhook_urls: list[str]):
        self.webhook_urls = webhook_urls

    def send_message(self, message: str) -> bool:
        """
        發送訊息到 Discord Webhook，可以有多個 webhook URL。

        NOTE: 只要有一個 webhook 發送失敗就回傳 False，並且排列在後面的 webhook 將不會嘗試繼續發送。

        Args:
            message (str): 要發送的訊息內容
        Returns:
            bool: 發送是否成功
        """
        try:
            for url in self.webhook_urls:
                response = requests.post(url, json={"content": message})
                response.raise_for_status()
                logger.debug(
                    f"Message sent to Discord webhook: {url}, response status: {response.status_code}, message sendt: {message}"
                )
        except Exception as e:
            logger.error(
                f"Exception occurred while sending message to Discord: {str(e)}"
            )
            return False
        return True

    def __repr__(self) -> str:
        return f"DiscordNotifier(webhook_urls={self.webhook_urls})"


# 預設的 discord_notifier，使用 user_config 裡的 webhook 清單
discord_notifier = DiscordNotifier(discord_webhooks)


def get_discord_notifier() -> DiscordNotifier:
    return discord_notifier


def set_discord_notifier(new_notifier: DiscordNotifier) -> None:
    global discord_notifier
    logger.debug(
        f"Setting new discord_notifier: {new_notifier}, old: {discord_notifier}"
    )
    discord_notifier = new_notifier


def send_to_discord(message: str) -> bool:
    """
    快速發送訊息到 Discord Webhook，使用預設的 discord_notifier。

    NOTE: 只要有一個 webhook 發送失敗就回傳 False，並且排列在後面的 webhook 將不會嘗試繼續發送。

    Args:
        message (str): 要發送的訊息內容
    Returns:
        bool: 發送是否成功
    """
    return discord_notifier.send_message(message)
