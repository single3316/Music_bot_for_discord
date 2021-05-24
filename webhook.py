from discord_webhook import DiscordWebhook, DiscordEmbed


def create_webhook(title, text):

    webhook = DiscordWebhook(url='https://discord.com/api/webhooks/839621007614672896/2e1_mmYOTtKKF0uyN42q_eeg9BCyz8tS521jCXBuUqiODM9SfwEzVFQLB85EAExUIuSd')

    embed = DiscordEmbed(title=title, description=text, color=242424)

    webhook.add_embed(embed)

    response = webhook.execute()
    return response
