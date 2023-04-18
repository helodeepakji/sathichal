import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import authenticate
from requests import request

class routConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print(self.scope)
        # create connection
        await self.accept()

        # response to client, that we are connected.
        await self.send(text_data=json.dumps({
            'type': 'connection',
            'data': {
                'message': "Connected"
            }
        }))

    async def disconnect(self, close_code):
        print("socket is disconnect")
        await self.send(text_data=json.dumps({
            'type': 'connection',
            'data': {
                'message': "Disconnected"
            }
        }))



#     # Receive message from client WebSocket

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        # print(text_data_json)

        eventType = text_data_json['type']

        if eventType == 'login':
            print(eventType)
            name = text_data_json['data']['name']
            print(name)
            # write code here

            await self.send(text_data=json.dumps({
                'type': 'call_received',
                'data': "Sandeep",
            }))
        
        if eventType == 'call':
            name = text_data_json['data']['name']
            print(self.my_name, "is calling", name);
            # print(text_data_json)

            self.send(text_data=json.dumps({
                'type': 'call_received',
                'data': "Deepak",
            }))



    # Receive message from room group
    async def all_user(self, event):
        message = event["message"]
        print(message)
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
                'type': 'auto',
                'data': {
                    'message': "message"
                }
            }))