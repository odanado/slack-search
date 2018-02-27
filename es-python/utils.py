def convert_message(data):
    if data['type'] != 'message':
        return None
    if data.get('subtype', '') == 'pinned_item':
        return None

    if data.get('subtype', '') == 'bot_message':
        user = data['bot_id']

    elif 'user' not in data:
        # 添付ファイルの場合
        from pprint import pprint
        if 'file' not in data:
            pprint(data)
        user = data['file']['user']
    else:
        user = data['user']

    return {'user': user, 'text': data['text'],
            'timestamp': data['ts']}
