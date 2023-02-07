from telethon.sync import TelegramClient, events

client: TelegramClient = None


def create_client(phone, api_id, api_hash):
    global client
    client = TelegramClient(phone, api_id, api_hash)
    return client
