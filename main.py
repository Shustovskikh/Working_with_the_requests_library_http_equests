# ЗАДАЧА № 1. Кто самый умный супергерой?

import requests
import json

url = 'https://cdn.jsdelivr.net/gh/akabab/superhero-api@0.3.0/api/all.json'
heroes_list = ["Hulk", "Captain america", "Thanos"]
response = requests.get(url)
response_json = response.json()
intelligence = 0
smartest_hero = ""

for hero in response_json:
    if hero["name"] in heroes_list:
        hero_intelligence = int(hero["powerstats"]["intelligence"])
        if hero_intelligence > intelligence:
            intelligence = hero_intelligence
            smartest_hero = hero["name"]

print(f"Самый интелектуальный герой - {smartest_hero}, интелект: {intelligence}")

# ЗАДАЧА № 2. Файл сохранить на Яндекс.Диск

from pprint import pprint
import requests

with open('token.txt', 'r') as file_object:
    token = file_object.read().strip()

class YaUploader:

    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def get_files_list(self):
        files_url = 'https://cloud-api.yandex.net/v1/disk/resources/files'
        headers = self.get_headers()
        response = requests.get(files_url, headers=headers)
        return response.json()

    def _get_upload_link(self, disk_file_path):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.get_headers()
        params = {"path": disk_file_path, "overwrite": "true"}
        response = requests.get(upload_url, headers=headers, params=params)
        pprint(response.json())
        return response.json()

    def upload_file_to_disk(self, disk_file_path, filename):
        href_json = self._get_upload_link(disk_file_path=disk_file_path)
        href = href_json["href"]
        response = requests.put(href, data=open(filename, 'rb'))
        response.raise_for_status()
        if response.status_code == 201:
            print("Файл успешно загружен на Диск.")
        else:
            print('Произошла ошибка при загрузке файла.')

if __name__ == "__main__":
    ya = YaUploader(token=token)
    ya.upload_file_to_disk(r"F:\фото\test.txt")