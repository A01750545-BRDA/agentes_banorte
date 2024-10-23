from conversation.remote.database import db
from typing import Optional

key_map = {
        'summary': 'summary',
        'human': 'human',
        'AI': 'AI',
        'messages': 'messages',
        'last_message': 'last_message',
    }

def retrieve_remote_history(user_id: str) -> dict:
    assert isinstance(user_id, str)

    if user_id not in db:
        raise KeyError
    
    return db[user_id]


def update_remote_history(user_id: str, new_summary: Optional[str] = None,
                          new_last_message: Optional[int] = None,
                          new_messages: Optional[dict[str, str]] = None):
    if new_summary:
        db[user_id][key_map['summary']] = new_summary

    if new_last_message:
        db[user_id][key_map['last_message']] = new_last_message

    if new_messages:
        messages = {key_map['human']: new_messages['input'], key_map['AI']: new_messages['output']}
        db[user_id][key_map['messages']].append(messages)