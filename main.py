from telethon import TelegramClient, events
import openai
import dotenv
import os


dotenv.load_dotenv()


api_id = os.environ.get("TELEGRAM_API_ID")
api_hash = os.environ.get("TELEGRAM_API_HASH")
api_key = os.environ.get("OPENAI_API_KEY")
product_info = """Astron - bu o'zbek tilidagi qulay va sifatli abiturentlar uchun mobil ilova.
Qulaylikar:
- Tayyor savollar ombori
- Qulay interfeys
- Hamyonbop tariflar
- Oson to'lov jarayoni. PayMe yokida UPay to'lov tizimlari orqali
- Kunlik eslatmalar
Narxlar:
- 99 ming so'm yillik

Foydalanuvchi: %s
"""

client = TelegramClient('session_name', api_id, api_hash)
openai_client = openai.OpenAI(api_key=api_key)


async def main():
    await client.start()

    me = await client.get_me()
    print(f'Logged in as {me.first_name}')


@client.on(events.NewMessage(from_users=["@astron_corp", "@alistreetworkout", "@mbicc"]))
async def handler(event: events.NewMessage.Event):
    content = product_info % event.message.message
    chat = openai_client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": content
            },
        ],
        model="chatgpt-4o-latest"
    )
    await event.reply(chat.choices[0].message.content)

with client:
    client.loop.run_until_complete(main())
    client.run_until_disconnected()
