import requests
import os
import json
from datetime import datetime

def main():
    class VK:
        def __init__(self, access_token, version='5.131'):
            self.token = access_token
            self.version = version
            self.params = {'access_token': self.token, 'v': self.version}

        def get_photo(self, user_id):
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

        def download_photo(self, user_id):
            data = self.get_photo(user_id)
            photo_items = data['items']
            if len(photo_items) == 0:
                return 'У пользователя нет доступных фото.'

            # Создание папки для сохранения фото из VK
            if os.path.exists(dir_photo):
                for f in os.listdir(dir_photo):
                    os.remove(os.path.join(dir_photo, f))
            else:
                os.mkdir(dir_photo)

            # Формирование информации по всем фото
            photo_list_to_json = []
            i = 0

            for item in photo_items:
                max_size = 0
                for size in item['sizes']:
                    if size['height'] >= max_size:
                        max_size = size['height']
                        size_type = size['type']
                        photo_url = size['url']

                likes_photo = item['likes']['count']
                name_photo = f'{likes_photo}.jpg'
                date_photo = datetime.fromtimestamp(item['date']).strftime("%d-%m-%Y")

                for dic in photo_list_to_json:
                    if name_photo == dic['file_name']:
                        name_photo = f'{likes_photo}_{date_photo}.jpg'

                photo_list_to_json.append({'file_name': name_photo, 'size': size_type})

                # Сохранение фотографий
                with open(f'{dir_photo}/%s' % name_photo, 'wb') as file:
                    img = requests.get(photo_url)
                    file.write(img.content)
                i += 1
                print(f'Загружена {i}-я фотография ({name_photo}) в папку {dir_photo}')

            # Создание файла о скачанных фотографиях
            with open('photo_info.json', 'w') as file:
                json.dump(photo_list_to_json, file, indent=2)
            print(f'Создан файл photo_info.json с информацией о сохраненных фото')


    class YA_disk:
        def __init__(self, token: str):
            self.token = token

        def authorization(self):
            return {
                'Content-Type': 'application/json',
                'Authorization': f'OAuth {self.token}'
                }

        def create_folder(self, folder_name):
            url = f'https://cloud-api.yandex.net/v1/disk/resources/'
            params = {'path': f'{folder_name}',
                      'overwrite': 'false'}
            response = requests.put(url=url, headers=self.authorization(), params=params)

            # Обработка ответов
            if response.status_code == 409:
                print('Супер, такая папка уже есть на вашем Яндекс Диске, сохраним фото в неё.')
            elif response.status_code == 201:
                print(f'Папка {folder_name} создана на вашем Яндекс Диске.')
            else: print(f'Что-то пошло не так. Код ошибки: {response.status_code}')

        def upload_photo(self, folder_name, file_path):
            url = f'https://cloud-api.yandex.net/v1/disk/resources/upload'
            photo_list = os.listdir(dir_photo)
            i = 0
            for photo in photo_list:
                params = {'path': f'{folder_name}/{photo}',
                          'overwrite': 'true'}

                # Получение ссылки на загрузку
                response = requests.get(url, headers=self.authorization(), params=params)
                url_for_upload = response.json().get('href', '')

                # Загрузка файла
                with open(f'{file_path}/{photo}', 'rb') as file:
                    uploader = requests.post(url_for_upload, files={"file": file})

                # Обработка ошибок
                if uploader.status_code == 201:
                    i += 1
                    print(f'Загружена {i}-я фотография ({photo}) в папку {folder_name} на Яндекс Диске')
                else: print(f'Ошибка загрузки фото ({photo}). Код ошибки: {uploader.status_code}')


    # Объявление токена и запрос данных у пользователя
    with open('vk_token.txt', 'r') as file_object:
        vk_token = file_object.read().strip()

    dir_photo = 'images_vk'
    user_id = str(input('Введите id пользователя VK: '))
    downloader = VK(vk_token)
    downloader.download_photo(user_id)

    ya_token = str(input('Введите токен Яндекс Диска: '))
    uploader = YA_disk(ya_token)
    folder_name = str(input('Введите имя папки на Яндекс Диске, в которую будем сохранять фото: '))
    uploader.create_folder(folder_name)
    file_path = f'{os.getcwd()}/{dir_photo}'
    uploader.upload_photo(folder_name, file_path)



if __name__ == '__main__':
    main()