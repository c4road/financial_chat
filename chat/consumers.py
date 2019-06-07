import asyncio
import json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async

from .models import Thread, ChatMessage 

class ChatConsumer(AsyncConsumer):

	async def websocket_connect(self, event):

		print("connected", event)

		await self.send({
			"type": "websocket.accept"
		})

		other_user = self.scope['url_route']['kwargs']['username'] # username matches routing regex
		me = self.scope['user']
		thread_object = await self.get_thread(me, other_user)

		print(other_user, me)
		print(thread_object)



	async def websocket_receive(self, event):

		print("receive", event)
		front_text = event.get('text', None)

		if front_text is not None:

			loaded_dict_data = json.loads(front_text)
			msg = loaded_dict_data.get('message')
			print(msg)
			await self.send({
				"type": "websocket.send",
				"text": msg
			})


	async def websocket_disconnect(self, event):

		print("disconnected", event)

	# Obligatorio cada vez que voy a pedir algo de la base de datos 
	@database_sync_to_async
	def get_thread(self,user,other_username):

		return Thread.objects.get_or_create(user,other_username)[0]