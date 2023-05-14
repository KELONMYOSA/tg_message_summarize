from dao import get_messages_from_chat
from summarization import get_summary


def run(bot):
    @bot.message_handler(commands=["summary"])
    async def summarize(message):
        command = message.text.split(" ")
        if len(command) == 2:
            try:
                await bot.send_message(message.chat.id, 'Processing..')

                messages_list = get_messages_from_chat(message.chat.id, int(command[1]))
                summary = get_summary(messages_list)

                await bot.send_message(message.chat.id, summary)
            except Exception as e:
                print(e)
                await bot.send_message(
                    message.chat.id,
                    'Отправьте в формате "/summary <кол-во сообщений>"'
                )
        else:
            await bot.send_message(
                message.chat.id,
                'Отправьте в формате "/summary <кол-во сообщений>"'
            )
