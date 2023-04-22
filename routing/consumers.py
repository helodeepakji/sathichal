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
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        await self.send(text_data=json.dumps({
            'type': 'disconnection',
            'data': {
                'message': "Disconnected"
            }
        }))



#     # Receive message from client WebSocket

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        # print(text_data_json)

        eventType = text_data_json['type']
        
        if eventType == 'user_location':
            name = text_data_json['username']
            user_location = text_data_json['location_data']
            await self.channel_layer.group_send(
                self.room_group_name, {"type": "all_user","Event": "user_location","username" : name, "location": user_location}
            )

        # write code here
        
        # for request incompelete
        
        # if eventType == 'request':
        #     to_name = text_data_json['to_username']
        #     from_name = text_data_json['from_username']
        #     channel_name = text_data_json['channel_name']
        #     await self.send(channel_name=channel_name,text_data=json.dumps({'Event':'request','data':{'to_username':to_name,'from_username':from_name,'channel_name':channel_name}}))
            



    # Receive message from room group
    async def all_user(self, event):
        # print(event)
        if event['Event'] == 'connected' : 
        # Send message to WebSocket
            await self.send(text_data=json.dumps({
                    'type': 'auto',
                    'data': {
                        'message': event['message']
                    }
                }))
            
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
            

    def get_user(self,username):
        user_data = sathiUser.objects.filter(username = username)

        if user_data[0].profile_pic:
            send_data = {'username':user_data[0].username,'first_name':user_data[0].first_name,'last_name':user_data[0].last_name,'profile_pic':user_data[0].profile_pic.url,'channel_name':self.channel_name}
        # if user profile pic is not set then send None
        else:
            send_data = {'username':user_data[0].username,'first_name':user_data[0].first_name,'last_name':user_data[0].last_name,'profile_pic':None,'channel_name':self.channel_name}
        
        return send_data