import requests
import time
import json
from json.decoder import JSONDecodeError


def get_message_from_user(event, context):
    message = json.loads(event['body'])
    print('Users request: ', message)
    
    if (user_message := message['message'].get('text')):  # Проверим, есть ли текст в сообщении
        check_message(message['message']['chat']['id'], user_message) # Отвечаем
    if (user_location := message['message'].get('location')):  # Проверим, если ли location в сообщении
        mag_field = magnetic_field_responce(user_location['latitude'], user_location['longitude'])
        print(f'mag_fielg: {mag_field}')
        if mag_field:
            dip_angle = mag_field['inclination']
            total_field = mag_field['totalintensity']
            latitude = user_location['latitude']
            longitude = user_location['longitude']
            send_message(message['message']['chat']['id'], f'DIP angle = {dip_angle} \nTotal field = {total_field}' 
            f'\nLatitude = {latitude} \nLongtitude = {longitude}')
        else:
            send_message(message['message']['chat']['id'], 'Сервер временно недоступен')
    

def check_message(chat_id, message):
    if message.lower() in ['hello']:
        send_message(chat_id, 'Hello')
    elif message == '/start':
        send_message(chat_id, 'Hi! Please, send me your location!')
    else:
        send_message(chat_id, 'Invalid request! Please, send me your location!')

def magnetic_field_responce(latitude, longitude):
    try:
        data = requests.get('https://www.ngdc.noaa.gov/geomag-web/calculators/calculateIgrfwmm',
                            params={'key': '****', 'lat1': latitude, 'lon1': longitude,
                                    'model': 'IGRF', 'resultFormat': 'json'}).json()  # делаем запрос магнитных составляющих
    except JSONDecodeError:
        print('Ошибка сервера')
        return False
    print('Ответ сервера Geomag-web: ', data)
    return data['result'][0]
    

def send_message(chat_id, text):
    URL = 'https://api.telegram.org/bot'
    TOKEN = '*******'
    requests.get(f'{URL}{TOKEN}/sendMessage?chat_id={chat_id}&text={text}')
    URL = 'https://api.telegram.org/bot'
    TOKEN = ''
    requests.get(f'{URL}{TOKEN}/sendMessage?chat_id={chat_id}&text={text}')
