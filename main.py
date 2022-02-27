import asyncio
import random

from telethon import TelegramClient
from telethon import functions, types
import questionary

from report_text import generate_text

api_id = int(questionary.password('Api ID:').ask())
api_hash = questionary.password('Api hash:').ask()



client = TelegramClient('session_new', api_id, api_hash)
client.start()

print('Bot started')


async def main():
    number_of_channels_rep = 150

    telegram_list = open('telegram_db', 'r').readlines()
    random.shuffle(telegram_list)

    for (i,telegram_channel) in enumerate(telegram_list[:number_of_channels_rep]):
        if "https://" in telegram_channel:
            telegram_channel = telegram_channel.split('/')[-1]
        elif '@' in telegram_channel:
            telegram_channel = telegram_channel[1:]
        print(i+1, telegram_channel.strip())
        try:
            result = await client(functions.account.ReportPeerRequest(
                peer=telegram_channel,
                reason=types.InputReportReasonSpam(),
                message=generate_text())
            )
            print(result)
        except ValueError:
            print("Channel not found")
        await asyncio.sleep(10 + 2 * random.random())
with client:

    client.loop.run_until_complete(main())

