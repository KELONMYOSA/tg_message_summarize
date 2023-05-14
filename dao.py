import sqlite3 as db

from utils import messages_to_json


def add_message(message):
    con = db.connect('messages.db')

    sql = 'INSERT INTO messages (chat_id, message_id, user, username, user_id, text, date) values (?, ?, ?, ?, ?, ?, ?)'

    chat = message.chat
    user = message.from_user
    data = (chat.id, message.message_id, f"{user.first_name} {user.last_name}",
            user.username, user.id, message.text, message.date)

    con.execute(sql, data)
    con.commit()


def get_messages_from_chat(chat_id, n_messages):
    con = db.connect('messages.db')

    sql = f'SELECT * FROM messages WHERE chat_id = {chat_id} ORDER BY date DESC, message_id DESC LIMIT {n_messages}'

    cursor = con.execute(sql)
    description = cursor.description
    messages = cursor.fetchall()

    return messages_to_json(messages, description)
