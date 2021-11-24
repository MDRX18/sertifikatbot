from django.conf.urls import url
from django.shortcuts import render
from django.http import HttpResponse
from main.credetionals import *
from django.views.decorators.csrf import csrf_exempt
from main.models import *
import json
import requests
# Create your views here.
def index(request):
    return HttpResponse('salom')
@csrf_exempt
def getpost(request):
    if request.method == 'POST':
        response = json.loads(request.body)
        print(response)
        try:
            message = response['message']
        except:
            try:
                message = response['callback_query']
            except:
                pass
        try:
            user = User.objects.get(userid=message['from']['id'])
        except:
            user = User.objects.create(userid=message['from']['id'], username=message['from']['username'])
        try:
            message = response['callback_query']
            sethandler(user, message)
        except:
            try:
                message = response['message']
                
                set_handler(user, message)
            except:
                pass
        
    return HttpResponse(f'alik, {request}')

def sethandler(user, message):
    request_to_bot('deleteMessage', {
        'chat_id': user.userid,
        'message_id': message['message']['message_id']
    })
    if message['data'] == 'get_sertifikat':
        get_ser(user, message)
    elif message['data'] == "post_sertifikat":
        add_ser(user, message)
    

def get_ser(user, message):
    message = 'Sertifikatning 6 raqamdan iborat nomerini kiriting. Faqat sonda misol uchun 000001'
    user.user_status = 'get1'
    user.save()
    sentmessage(user, message, markup={'keyboard': [['Chiqish']],'resize_keyboard': True})

def add_ser(user, message):
    user.user_status = 'add1'
    user.save()
    message = "Marhamat Sertifikat faylini jo'nating"
    sentmessage(user, message, markup={'keyboard': [['Chiqish']],'resize_keyboard': True})

def check_admin(user, message):
    if user.user_dagree == 'superuser':
        return {'keyboard': [['Sertifikatni olish'], ["Sertifikat qo'shish"]],'resize_keyboard': True}
    else:
        return {'keyboard': [['Sertifikatni olish']],'resize_keyboard': True}
    
def set_handler(user, message):
    try:
        if message['text'] == 'Chiqish':
            message = 'Assosiy menyu'
            sentmessage(user, message, markup=check_admin(user, message))
            user.user_status = ""
            user.save()
    except:
        pass
    if user.user_status == '0':
        if message['text'] == '1221':
            message = 'Siz endi superusersiz.'
            user.user_status = '1'
            user.user_dagree = "superuser"
            user.save()
            sentmessage(user, message, markup=check_admin(user, message))
            message = 'Birini tanlang.'
            markup = {
                'inline_keyboard': [[
                {
                    'text': 'Sertifikatni olish',
                    'callback_data': 'get_sertifikat'
                }], [
                {
                    'text': "Sertifikat qo'shish",
                    'callback_data': 'post_sertifikat'
                }]]
            } 
            sentmessage(user, message, markup)
            
                
        else:
            message = "Parol nato'g'ri:"
            sentmessage(user, message, markup={})
    elif user.user_status == 'add1':
        try:
            fayl_id = message['document']
            print(fayl_id['file_id'])
            try:
                ser = Sertificats.objects.get(ser_fayl_id=fayl_id['file_id'])
                message = 'Bu fayl oldin ishlatilgan'
            except:
                ser = Sertificats.objects.create(ser_fayl_id=fayl_id['file_id'])
                message = "Sertifikat raqamini jo'nating. Faqat sonlarda."
            user.user_status='add2'
            user.save()                
        except:
            message = "Sertifikat fayli jo'natilmagan. Iltimos fayl jo'nating."
        sentmessage(user, message, markup={'keyboard': [['Chiqish']],'resize_keyboard': True})
    elif user.user_status == 'add2':
        ser = Sertificats.objects.get(ser_id='1')
        try:
            ser1 = Sertificats.objects.get(ser_id=message['text']) 
            message = 'Bunday raqamli sertifikat oldin kiritilgan.'
            sentmessage(user, message, markup={})
        except:
            ser.ser_id = message['text']
            ser.save()
            user.user_status=''
            user.save()
            message = "Sertifikat muffaqiyatli qo'shildi"
            sentmessage(user, message, markup=check_admin(user, message))
    elif user.user_status == 'get1':
        try:
            ser = Sertificats.objects.get(ser_id=message['text'])
            print(ser.ser_fayl_id)
            request_to_bot('sendDocument', {
                'chat_id': user.userid,
                'document': ser.ser_fayl_id,
                'reply_markup': json.dumps(check_admin(user, message))
            })
            user.user_status = ''
            user.save()
        except:
            sentmessage(user, message='Bunday nomerli Sertifikat mavjud emas.Iltimos yaxshilab tekshirib qaytadan kiriting.', markup={})
    else:        
        get_handler(user, message)

def get_handler(user, message):
    message1 = message['text']
    print(message1)
    if message1 == '/start':
        message = f'Assalomu alaykum {message["from"]["first_name"]} Azizbek Khabibullayev kanalining botiga hush kelibsiz.Bu bot orqali o"z sertifikatingizni olishingiz yoki haqiqiyligini tekshirishiz mumkin.'
        markup = {
            'keyboard': [['Sertifikatni olish']],
            'resize_keyboard': True
        }
        sentmessage(user, message=message, markup=markup)
        message = f'Sertifikatni olish uchun bosing.'
        markup = {
            'inline_keyboard': [[
            {
                'text': 'Sertifikatni olish',
                'callback_data': 'get_sertifikat'
            }
        ]]
        }
        sentmessage(user, message=message, markup=markup)
    elif message1 == '/admin2001':
        message = 'Parolni kiriting:'
        user.user_status = '0'
        user.save()
        markup = {
            'keyboard': [['Chiqish']],
            'resize_keyboard': True
        }
        sentmessage(user, message, markup)
    elif message1 == "Sertifikat qo'shish":
        add_ser(user, message)
    elif message1 == "Sertifikatni olish":
        print('ssss')
        get_ser(user, message)
            
def sentmessage(user, message, markup):
    request_to_bot('sendMessage', {
        'chat_id': user.userid,
        'text': message,
        'reply_markup': json.dumps(markup)
    })

def request_to_bot(type, data):
    return requests.post(BOT_API + type, data)

def setwebhook(request):
    response = requests.post(BOT_API + 'setwebhook?url=' + URL).json()
    return HttpResponse(f'{response}')