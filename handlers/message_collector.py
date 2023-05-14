from dao import add_message


def run(bot):
    @bot.message_handler(func=lambda message: not message.text.startswith("/summary"))
    async def collect(message):
        if not message.from_user.is_bot:
            add_message(message)
