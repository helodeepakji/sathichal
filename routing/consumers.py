import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import authenticate
from requests import request
from home.models import sathiUser
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async , async_to_sync
from django.core import serializers
from home.models import sathiUser
from .models import group
from datetime import datetime
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


        if eventType == 'success':
            name = text_data_json['username']
            user_location = text_data_json['location_data']
            await self.channel_layer.group_send(
                self.room_group_name, {"type": "all_user","Event": "success","username" : name, "location": user_location}
            )
        
        # confirm user event type
        if eventType == 'sendConfirm':
            
            date = datetime.now().date()
            time = datetime.now().time()
            
            # to save group
            created_group = group(group_name=self.room_group_name, added_by_user=text_data_json['sender'], added_user=text_data_json['reciver'], date=date, time=time)
            await database_sync_to_async(created_group.save)()
            
            # to get group
            temp_group = await database_sync_to_async(list)(group.objects.filter(group_name=self.room_group_name,date = date))
            sendgroup = []
            
            # for differece between time
            for i in temp_group:
                temp_obj = {}
                timeDiff = datetime.combine(date.today(), i.time) - datetime.combine(date.today(), datetime.now().time())
                timeDiffHours = timeDiff.days * 24 + timeDiff.seconds / 3600.0
                if timeDiffHours < 1 and i.date == datetime.now().date():
                    temp_obj['added_by_user'] = i.added_by_user
                    temp_obj['added_user'] = i.added_user
                    temp_obj['date'] = str(i.date)
                    temp_obj['time'] = str(i.time)
                    temp_obj['group_name'] = i.group_name
                    sendgroup.append(temp_obj)
            
            
            print(sendgroup)
            await self.channel_layer.group_send(
                self.room_group_name, {"type": "all_user","Event": "confirmed","group":sendgroup}   
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


        #when success all users    
        if event['Event'] == 'success' :
            user_data = await database_sync_to_async(self.get_user)(event['username']) 
            # print(user_data)

            await self.send(text_data=json.dumps({
                    'type': 'success',
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
        
        if event['Event'] == 'confirmed' :
            await self.send(text_data=json.dumps({
                    'type': 'confirmed',
                    'data': {
                        'group' : event['group']
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
    
    # get sathi
    def get_sathi(self,username):
        user_data = sathiUser.objects.get(username = username)
        
        return user_data


# hellodeepakji
# deepak
