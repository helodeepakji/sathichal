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

        if eventType == "chat" :
            await self.channel_layer.group_send(
                self.room_group_name, {"type": "group_send","Event": "chat","message": text_data_json['message'] ,"sender" : text_data_json['sender']}
            )


        if eventType == "getLocation":
            await self.channel_layer.group_send(
                self.room_group_name, {"type": "group_send","Event": "getLocation","username" : text_data_json['username'],"loc_user" : text_data_json['loc_user']}
            )

        if eventType == "sendlocation":
            await self.channel_layer.group_send(
                self.room_group_name, {"type": "group_send","Event": "sendLocation","username" : text_data_json['username'], "location" : text_data_json['location_data'],"loc_user" : text_data_json['loc_user']}
            )

       





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

        if event['Event'] == 'getLocation' :
            if event['loc_user'] != event['username'] :
                await self.send(text_data=json.dumps({
                        'type': 'getLocation',
                        'data': {
                            'loc_user' : event['loc_user'],
                            'username': event['username'],
                        }
                }))

        if event['Event'] == 'sendLocation' :
            await self.send(text_data=json.dumps({
                    'type': 'sendLocation',
                    'data': {
                        'username': event['username'],
                        'loc_user': event['loc_user'],
                        'location': event['location']
                    }
            }))

        if event['Event'] == 'chat' :
            await self.send(text_data=json.dumps({
                    'type': 'chat',
                    'data': {
                        'message': event['message'],
                        'sender': event['sender']
                    }
            }))
            
      