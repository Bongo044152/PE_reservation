import requests


def send_to_discord(webhook_url, message):
    requests.post(webhook_url, json={"content": message})
