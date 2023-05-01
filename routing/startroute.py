import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import group
class sathiRoute(AsyncWebsocketConsumer):
    async def connect(self):
        # username = str(self.scope['user'])
        urldata = self.scope["url_route"]["kwargs"]
        self.room_name = str(urldata['sath_id'])
        self.room_group_name = "routing_%s" % str(urldata['sath_id'])

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


    async def disconnect(self, close_code):
        print("socket is disconnect")
        name = str(self.scope['user'])
        await self.channel_layer.group_send(
                self.room_group_name, {"type": "group_send","Event": "disconnected","username" : name}
            )
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)



#     # Receive message from client WebSocket

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(text_data_json)

        eventType = text_data_json['type']
        if eventType == "user_location":
            await self.channel_layer.group_send(
                self.room_group_name, {"type": "group_send","Event": "user_location","username" : text_data_json['username'], "location" : text_data_json['location_data']}
            )

        if eventType == "chat" :
            print(text_data_json)

       





    # Receive message from room group
    async def group_send(self, event):
        # print(event)

        #when user is connected
        if event['Event'] == 'connected' : 
            await self.send(text_data=json.dumps({
                    'type': 'auto',
                    'data': {
                        'message': event['message']
                    }
                }))
            
        if event['Event'] == 'user_location' :
            await self.send(text_data=json.dumps({
                    'type': 'user_location',
                    'data': {
                        'username': event['username'],
                        'location': event['location']
                    }
            }))
            
      