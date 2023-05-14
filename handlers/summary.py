def run(bot):
    @bot.message_handler(commands=["summary"])
    async def summarize(message):
        command = message.text.split(" ")
        if len(command) == 2:
            await bot.send_message(
                message.chat.id,
                command[1]
            )
        else:
            await bot.send_message(
                message.chat.id,
                'Отправьте в формате "/summary <кол-во сообщений>"'
            )
