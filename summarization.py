import openai
import os
import tiktoken

openai.api_key = os.getenv("OPENAI_KEY_NAPOLEON")


def count_tokens(s: str, encoding: tiktoken.core.Encoding) -> int:
    input_ids = encoding.encode(s)
    return len(input_ids)


def add_meta(json: list[dict], encoding: tiktoken.core.Encoding):
    for message_block in json:
        message_block["n_tokens"] = count_tokens(
            f'{message_block["user"]}: {message_block["text"]}',
            encoding,
        )
    return json


def get_plain_text(messages: list[dict]):
    text = ""
    for m in messages:
        text = f'{text}\n{m["user"]}: {m["text"]}'
    return text.strip()


def break_up_messages_to_chunks(
        messages: list[dict],
        chunk_size=2000,
):
    chunks = []

    current_tokens = 0
    current_messages = []
    for m in messages:
        if current_tokens > chunk_size:
            chunks.append(get_plain_text(current_messages))

            current_tokens = current_messages[-1]["n_tokens"]
            current_messages = [current_messages[-1]]

        n_tokens = m["n_tokens"]
        if n_tokens > chunk_size:
            if len(current_messages) != 0:
                chunk_text = get_plain_text(current_messages)
                chunks.append(chunk_text)

            m_1 = m.copy()
            m_2 = m.copy()

            m_1["text"] = m_1["text"][:len(m_1["text"]) // 2]
            chunk_text = get_plain_text([m_1])
            chunks.append(chunk_text)

            m_2["text"] = m_2["text"][len(m_2["text"]) // 2:]
            chunk_text = get_plain_text([m_2])
            chunks.append(chunk_text)

            current_tokens = 0
            current_messages = []

        elif current_tokens + n_tokens > chunk_size:
            chunk_text = get_plain_text(current_messages)
            chunks.append(chunk_text)

            if len(current_messages) == 1:
                current_tokens = n_tokens
                current_messages = [m]
            else:
                current_tokens = current_messages[-1]["n_tokens"] + n_tokens
                current_messages = [current_messages[-1], m]

        else:
            current_tokens += n_tokens
            current_messages.append(m)
    return chunks


def get_summary(json: list[dict], chunk_size: int = 2000):
    encoding = tiktoken.get_encoding("gpt2")

    add_meta(json, encoding)

    chunks = break_up_messages_to_chunks(json, chunk_size)

    intent = "Суммаризируй, что обсуждали в этих сообщениях, чтобы я сразу понял?"
    prompt_requests = [f'{intent}: \n«{chunk}»' for chunk in chunks]

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt_requests,
        temperature=.2,
        max_tokens=500,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    intent = "По сообщениям ниже определи самое важное, о чём говорили в беседе?"
    summaries = "\n".join([r["text"].strip() for r in response["choices"]])
    prompt_request = f'{intent}:\n{summaries}'

    ans = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt_request,
        temperature=.2,
        max_tokens=700,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    return ans["choices"][0]["text"].strip()
