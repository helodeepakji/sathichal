import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import authenticate
from requests import request
from home.models import sathiUser
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async , async_to_sync
from django.core import serializers

class routConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # username = str(self.scope['user'])
        urldata = self.scope["url_route"]["kwargs"]
        self.room_name = urldata['src_lat']+'/'+urldata['src_lng']+'/'+urldata['dest_lat']+'/'+urldata['dest_lng']
        self.room_name = str(self.room_name)
        group = self.room_name.replace(".", "_")
        group = group.replace("/", "_")
        self.room_name = group
        self.room_group_name = "routing_%s" % group

        # print(self.room_name)
        # print(self.room_group_name)

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
                self.room_group_name, {"type": "all_user","Event": "disconnected","username" : name}
            )
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)



#     # Receive message from client WebSocket

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        # print(text_data_json)

        eventType = text_data_json['type']

        # when type is user_location
        if eventType == 'user_location':
            name = text_data_json['username']
            user_location = text_data_json['location_data']
            await self.channel_layer.group_send(
                self.room_group_name, {"type": "all_user","Event": "user_location","username" : name, "location": user_location}
            )

        # when user send request
        if eventType == 'sendRequest':
            await self.channel_layer.group_send(
                self.room_group_name, {"type": "all_user","Event": "sendRequest","sender" : text_data_json['sender'], "reciver": text_data_json['reciver']}
            )






    # Receive message from room group
    async def all_user(self, event):
        # print(event)

        #when user is connected
        if event['Event'] == 'connected' : 
            await self.send(text_data=json.dumps({
                    'type': 'auto',
                    'data': {
                        'message': event['message']
                    }
                }))
            
        #when user is disconnected
        if event['Event'] == 'disconnected' : 
            await self.send(text_data=json.dumps({
                    'type': 'disconnected',
                    'username': event['username']
                }))
            
        #when share your location all users    
        if event['Event'] == 'user_location' :
            user_data = await database_sync_to_async(self.get_user)(event['username']) 
            # print(user_data)

            await self.send(text_data=json.dumps({
                    'type': 'auto',
                    'event' : 'user_location',
                    'data': {
                        'username' : event['username'],
                        'user_data' : user_data,
                        'location': event['location']
                    }
                }))

        #when user send request    
        if event['Event'] == 'sendRequest' :
            user_data = await database_sync_to_async(self.get_user)(event['sender']) 
            # print(user_data)
            await self.send(text_data=json.dumps({
                    'type': 'sendRequest',
                    'data': {
                        'sender' : event['sender'],
                        'user_data' : user_data,
                        'reciver': event['reciver']
                    }
                }))



    def get_user(self,username):
        user_data = sathiUser.objects.filter(username = username)

        if user_data[0].profile_pic:
            send_data = {'username':user_data[0].username,'first_name':user_data[0].first_name,'last_name':user_data[0].last_name,'profile_pic':user_data[0].profile_pic.url}
        # if user profile pic is not set then send None
        else:
            send_data = {'username':user_data[0].username,'first_name':user_data[0].first_name,'last_name':user_data[0].last_name,'profile_pic':None}
        
        return send_data