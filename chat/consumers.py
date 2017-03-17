import json

from channels import Group
from channels.sessions import channel_session


# Connected to websocket.connect
from chat.models import ChatUser


@channel_session
def ws_add(message):
    # Accept connection
    message.reply_channel.send({"accept": True})
    # Add them to the right group
    Group("chat").add(message.reply_channel)


# Connected to websocket.receive
@channel_session
def ws_message(message):
    message_json = json.loads(message['text'])
    user_id = message_json['user_name']
    message_type = message_json['type']
    message.channel_session['user'] = user_id

    if message_type == 'connect':
        print('connect')
        ChatUser(user_id=user_id).save()

    Group("chat").send({
        "text": message['text']
    })


# Connected to websocket.disconnect
@channel_session
def ws_disconnect(message):
    print('disconnect')
    user_id = message.channel_session['user']
    obj = ChatUser.objects.filter(user_id=user_id)
    obj.delete()
    context = {
        'type': 'disconnect',
        'text': '',
        'user_name': user_id
    }
    Group("chat").discard(message.reply_channel)
    Group("chat").send({
        "text": json.dumps(context)
    })
