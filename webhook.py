from discord_webhook import DiscordWebhook, DiscordEmbed
from discord import Webhook, AsyncWebhookAdapter
import aiohttp


def send_webhook(title, text, url):
    webhook = DiscordWebhook(url=url)

    embed = DiscordEmbed(title=title, description=text, color=242424)

    webhook.add_embed(embed)

    response = webhook.execute()
    return response
