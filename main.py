import requests
import os
from pprint import pprint
from datetime import datetime

def main():
    class VK:
        def __init__(self, access_token, version='5.131'):
            self.token = access_token
            self.version = version
            self.params = {'access_token': self.token, 'v': self.version}

        def get_photo(self):
            url = 'https://api.vk.com/method/photos.get'
            params = {'owner_id': user_id,
                      'album_id': 'profile',
                      'rev': '1',
                      'extended': '1',
                      'photo_sizes': '1',
                      'count': '5'
                      }
            res = requests.get(url, params={**self.params, **params}).json()
            return res['response']

        def download_photo(self):
            data = self.get_photo()
            pprint(data)
            photo_items = data['items']
            if len(photo_items) == 0:
                return 'У пользователя нет доступных фото.'

            # Создание папки для сохранения фото из VK
            if os.path.exists('images_vk'):
                for f in os.listdir('images_vk'):
                    os.remove(os.path.join('images_vk', f))
            else:
                os.mkdir('images_vk')

            # Формирование информации по всем фото
            photo_list_to_json = []
            i = 0

            for item in photo_items:
                max_size = 0
                for size in item['sizes']:
                    if size['height'] >= max_size:
                        max_size = size['height']
                        size_type = size['type']

                likes_photo = item['likes']['count']
                name_photo = f'{likes_photo}.jpg'
                print(name_photo)

                date_photo = datetime.fromtimestamp(item['date']).strftime("%d-%m-%Y")
                print(date_photo)

                for dic in photo_list_to_json:
                    if name_photo == dic['file_name']:
                        name_photo = f'{likes_photo}_{date_photo}.jpg'

                photo_list_to_json.append({'file_name': name_photo, 'size': size_type})
            pprint(photo_list_to_json)

    # Объявление токена и запрос данных у пользователя
    with open('vk_token.txt', 'r') as file_object:
        vk_token = file_object.read().strip()

    user_id = str(input('Введите id пользователя VK: '))
    downloader = VK(vk_token)
    downloader.download_photo()



if __name__ == '__main__':
    main()