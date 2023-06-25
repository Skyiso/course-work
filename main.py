import requests
from pprint import pprint

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


    with open('vk_token.txt', 'r') as file_object:
        vk_token = file_object.read().strip()

    user_id = str(input('Введите id пользователя VK: '))
    downloader = VK(vk_token)
    downloader.download_photo()



if __name__ == '__main__':
    main()