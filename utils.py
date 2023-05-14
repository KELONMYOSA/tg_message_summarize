def messages_to_json(messages, description):
    out = []
    keys = []
    for key in description:
        keys.append(key[0])
    for message in messages:
        out.append(dict(zip(keys, message)))
    out.reverse()

    return out
