import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import authenticate
from requests import request
from home.models import sathiUser
from channels.db import database_sync_to_async
from django.db.models import Q
# from asgiref.sync import sync_to_async , async_to_sync
# from django.core import serializers
from home.models import sathiUser
from .models import group
from datetime import datetime,  timedelta
import random
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
            sathiid = text_data_json['sathiID']
            # if sathi id is not empty
            if sathiid == '':
                sathiid = "SATHI"+str(random.randint(10000, 99999))
                is_sathi_id = await database_sync_to_async(group.objects.filter(sathi_id=sathiid).exists)()
                print("is sathi id",is_sathi_id)
                # if sathi id is already exist
                while is_sathi_id == True:
                    print("sathi id",sathiid)
                    sathiid = "SATHI"+str(random.randint(10000, 99999))
            
            
            # to save group
            created_group = group(group_name=self.room_group_name, added_by_user=text_data_json['sender'], added_user=text_data_json['reciver'], status = 'P' ,date=date, time=time, sathi_id=sathiid)
            await database_sync_to_async(created_group.save)()
            
            print("group created",created_group)

            added_by_user = await database_sync_to_async(self.get_user)(text_data_json['sender']) 
            added_user = await database_sync_to_async(self.get_user)(text_data_json['reciver']) 
            
            # to get group
            temp_group = await database_sync_to_async(list)(group.objects.filter(Q(added_by_user = text_data_json['sender']) | Q(added_by_user = text_data_json['sender']),group_name=self.room_group_name,date = date, status = 'P'))
            print(temp_group)
            sendgroup = []
            
            # for differece between time
            for i in temp_group:
                temp_obj = {}
                timeDiff = datetime.combine(datetime.today(), datetime.now().time()) - datetime.combine(datetime.today(), i.time)
                print(timeDiff)
                # print(type(datetime.now().time()),type(i.time))
                print(timeDiff<timedelta(minutes=60) and i.date == datetime.now().date())
                
                # timeDiffHours = timeDiff.days * 24 + timeDiff.seconds / 3600.0
                
                if timeDiff <= timedelta(minutes=60) and i.date == datetime.now().date() and i.status == 'P':
                    temp_obj['added_by_user'] = i.added_by_user
                    temp_obj['added_user'] = i.added_user
                    temp_obj['date'] = str(i.date)
                    temp_obj['time'] = str(i.time)
                    temp_obj['group_name'] = i.group_name
                    temp_obj['sathi_id'] = i.sathi_id
                    sendgroup.append(temp_obj)
            
            
            print(sendgroup)
            await self.channel_layer.group_send(
                self.room_group_name, {"type": "all_user","Event": "confirmed","group":sendgroup,"sender":added_by_user,"reciver":added_user,"Sathi_Id" : sathiid}   
            )

        # start now routing 
        if eventType == 'startnow' :
            sathiid = text_data_json['sathiID']
            await self.channel_layer.group_send(
                self.room_group_name, {"type": "all_user","Event": "startnow","sathid" : sathiid}
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
                        'group' : event['group'],
                        'added_by_user' : event['sender'],
                        'added_user' : event['reciver']
                    },
                    'Sathi_Id' : event['Sathi_Id']
                }))

        if event['Event'] == 'startnow' :
            await self.send(text_data=json.dumps({
                    'type': 'startnow',
                    'Sathi_Id' : event['sathid']
                }))



    def get_user(self,username):
        user_data = sathiUser.objects.filter(username = username)

        if user_data[0].profile_pic:
            send_data = {'username':user_data[0].username,'first_name':user_data[0].first_name,'last_name':user_data[0].last_name,'profile_pic':user_data[0].profile_pic.url}
        # if user profile pic is not set then send None
        else:
            send_data = {'username':user_data[0].username,'first_name':user_data[0].first_name,'last_name':user_data[0].last_name,'profile_pic':None}
        
        return send_data
    


# helodeepakji
# deepak
