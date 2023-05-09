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
from .models import group, feedback, chat
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
            print(self.room_group_name)
            date = datetime.now().date()
            time = datetime.now().time()
            sathi_id = text_data_json.get('sathiId','') #['sathiID']
            temp_sathi_id = None
            is_temp_sathi_id = await database_sync_to_async(group.objects.filter(Q(user=text_data_json['sender']) |Q(user=text_data_json['reciver']),status='P',group_name=self.room_group_name).exists)()
            print("is_temp_sathi_id",is_temp_sathi_id)
            # if sathi id is empty and group is already exist for sender or reciver then use that group id
            if sathi_id == '' and is_temp_sathi_id:
                temp_sathi_id = await database_sync_to_async(list)(group.objects.filter(Q(user=text_data_json['sender'])|Q(user=text_data_json['reciver']),status='P',group_name=self.room_group_name))
                print("tarun sathi id",temp_sathi_id[0].sathi_id)
                try:
                    sathi_id = temp_sathi_id[0].sathi_id
                except:
                    pass

            # if sathi id is not empty
            if temp_sathi_id == None:
                sathiid = "SATHI"+str(random.randint(10000, 99999))
                # if sathi id is already exist
                while await database_sync_to_async(group.objects.filter(sathi_id=sathiid).exists)():
                    print("sathi id in while loop",sathiid)
                    sathiid = "SATHI"+str(random.randint(10000, 99999))
                sathi_id = sathiid

            
            print("sathi id before saving group",sathi_id)
            # to save group
            is_group_exist_user1 = await database_sync_to_async(group.objects.filter(user=text_data_json['sender'],status='P',group_name=self.room_group_name).exists)()
            created_group1 = None
            if not is_group_exist_user1:
                created_group1 = group(group_name=self.room_group_name,user=text_data_json['sender'], status = 'P' ,date=date, time=time, sathi_id=sathi_id)
                await database_sync_to_async(created_group1.save)()
            
            print("group created",created_group1)
            
            is_group_exist_user2 = await database_sync_to_async(group.objects.filter(user=text_data_json['reciver'],status='P',group_name=self.room_group_name).exists)()
            created_group2 = None
            if not is_group_exist_user2:
                created_group2 = group(group_name=self.room_group_name, user=text_data_json['reciver'], status = 'P' ,date=date, time=time, sathi_id=sathi_id)
                await database_sync_to_async(created_group2.save)()
            
            print("group created",created_group2)

            added_by_user = await database_sync_to_async(self.get_user)(text_data_json['sender']) 
            added_user = await database_sync_to_async(self.get_user)(text_data_json['reciver']) 
            
            # to get group
            temp_group = await database_sync_to_async(list)(group.objects.filter(sathi_id = sathi_id, status = 'P',group_name=self.room_group_name))
            # print(temp_group[0])
            for i in temp_group:
                print("temp group",i.sathi_id)
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
                    temp_obj['user'] = i.user
                    temp_obj['date'] = str(i.date)
                    temp_obj['time'] = str(i.time)
                    temp_obj['group_name'] = i.group_name
                    temp_obj['sathi_id'] = i.sathi_id
                    sendgroup.append(temp_obj)
            
            
            print('send Group ',sendgroup)
            await self.channel_layer.group_send(
                self.room_group_name, {"type": "all_user","Event": "confirmed","group":sendgroup,"sender":added_by_user,"reciver":added_user,"Sathi_Id" : sathi_id}   
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
            user_rating = await database_sync_to_async(self.get_user_rating)(event['username'])
            # print(user_data)
            # user rating 
            # name of attribute is 'rating' in user_data
            user_data['rating'] = user_rating
            print(user_data)
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
    
    def get_user_rating(self,username):
        user_feedbacks = feedback.objects.filter(user = username)
        max_rating = user_feedbacks.__len__() * 5
        print(max_rating)
        total_rating = 0
        for i in user_feedbacks:
            total_rating = total_rating + i.rating
        
        if max_rating == 0:
            return 0
        else:
            return (total_rating/max_rating)*100

# helodeepakji
# deepak

# feedback
# sathi id
# username
# feedback 1-5
# rating

# chat
# sathi id
# username
# chat
# date
# time