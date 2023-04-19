import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import authenticate
from requests import request

class routConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        username = str(self.scope['user'])
        urldata = self.scope["url_route"]["kwargs"]
        self.room_name = urldata['src_lat']+'/'+urldata['src_lng']+'/'+urldata['dest_lat']+'/'+urldata['dest_lng']
        self.room_name = str(self.room_name)
        group = self.room_name.replace(".", "_")
        group = group.replace("/", "_")
        self.room_name = group
        self.room_group_name = "routing_%s" % group

        print(self.room_name)
        print(self.room_group_name)

        #join group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        # create connection
        await self.accept()

        # response to client, that we are connected.
        await self.send(text_data=json.dumps({
            'type': 'connection',
            'data': {
                'message': "Connected"
            }
        }))

        await self.channel_layer.group_send(
            self.room_group_name, {"type": "all_user", "message": "Jion new "+username}
        )

    async def disconnect(self, close_code):
        print("socket is disconnect")
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        await self.send(text_data=json.dumps({
            'type': 'connection',
            'data': {
                'message': "Disconnected"
            }
        }))



#     # Receive message from client WebSocket

    async def receive(self, text_data):
        # text_data_json = json.loads(text_data)
        # # print(text_data_json)

        # eventType = text_data_json['type']

        # if eventType == 'login':
        #     print(eventType)
        #     name = text_data_json['data']['name']
        #     print(name)
        #     # write code here

        #     await self.send(text_data=json.dumps({
        #         'type': 'call_received',
        #         'data': "Sandeep",
        #     }))
        
        # if eventType == 'call':
        #     name = text_data_json['data']['name']
        #     print(self.my_name, "is calling", name);
        #     # print(text_data_json)

        #     self.send(text_data=json.dumps({
        #         'type': 'call_received',
        #         'data': "Deepak",
        #     }))
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "all_user", "message": "Recive_message"}
        )



    # Receive message from room group
    async def all_user(self, event):
        message = event["message"]
        print(message)
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
                'type': 'auto',
                'data': {
                    'message': message
                }
            }))