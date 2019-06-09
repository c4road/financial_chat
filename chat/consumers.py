import asyncio
import json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async

from .models import Thread, ChatMessage
from .tasks import get_stock_code


class ChatConsumer(AsyncConsumer):

    async def websocket_connect(self, event):

        print("connected", event)
        print(self.channel_layer.valid_channel_names)

        # username matches routing regex
        thread_pk = self.scope['url_route']['kwargs']['pk']
        me = self.scope['user']
        thread_object = await self.get_thread(thread_pk)
        self.thread_object = thread_object
        chat_room = 'thread_{}'.format(thread_object.id)
        self.chat_room = chat_room

        await self.channel_layer.group_add(
            chat_room,
            self.channel_name
        )

        await self.send({
            "type": "websocket.accept"
        })

    async def websocket_receive(self, event):

        print("receive", event)
        front_text = event.get('text', None)

        if front_text is not None:

            loaded_dict_data = json.loads(front_text)
            msg = loaded_dict_data.get('message')
            user = self.scope['user']
            username = 'default'


            if '/stock=' in msg:
            	ticker = msg.replace('/stock=', '').strip()
            	get_stock_code.delay(self.chat_room, ticker)
            else:
	            if user.is_authenticated:
	                username = user.username
	            response = {
	                'message': msg,
	                'username': username
	            }
	            await self.create_chat_message(user, msg)
	            await self.channel_layer.group_send(
	                self.chat_room,
	                {
	                    'type': 'chat_message',
	                    'text': json.dumps(response)
	                }
	            )

    async def chat_message(self, event):
        await self.send({
                        'type': 'websocket.send',
                        'text': event['text']
                        })

    # async def stock_quotes(self, event):
    # 	await self.send({
    # 					'type': 'websocket.send',
    # 					'text': event['text']
    # 					})

    async def websocket_disconnect(self, event):

        print("disconnected", event)


    @database_sync_to_async
    def get_thread(self, id):

        return Thread.objects.get(id=id)

    @database_sync_to_async
    def create_chat_message(self, me, msg):
        thread_object = self.thread_object
        return ChatMessage.objects.create(thread=thread_object,
                                          user=me, message=msg)

