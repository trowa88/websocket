import json

from channels import Channel, Group
from channels.sessions import channel_session, enforce_ordering
from channels.auth import channel_session_user, channel_session_user_from_http


# Connected to websocket.connect
from chat.models import ChatUser


@channel_session_user_from_http
def ws_add(message):
    # Accept connection
    message.reply_channel.send({"accept": True})
    # Add them to the right group
    Group("chat").add(message.reply_channel)


# Connected to websocket.receive
@channel_session_user
def ws_message(message):
    message_json = json.loads(message['text'])
    user_id = message_json['user_name']
    message_type = message_json['type']

    if message_type == 'connect':
        print('connect')
        ChatUser(user_id=user_id).save()
    elif message_type == 'disconeect':
        print('disconnect')
        obj = ChatUser.objects.filter(user_id=user_id)
        obj.delete()
    else:
        pass
    Group("chat").send({
        "text": message['text']
    })


# Connected to websocket.disconnect
@channel_session_user
def ws_disconnect(message):

    Group("chat").discard(message.reply_channel)
