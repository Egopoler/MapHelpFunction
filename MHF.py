import sys
from io import BytesIO
import requests
from PIL import Image


def get_coord(text):
    """Получает координаты по адресу объекта
    text - адресс
    return x, y"""
    x, y = None, None
    toponym_to_find = text

    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_to_find,
        "format": "json"
    }
    response = requests.get(geocoder_api_server, params=geocoder_params)
    if not response:
        return x, y
    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    toponym_coodrinates = toponym["Point"]["pos"]
    x, y = toponym_coodrinates.split(" ")
    return x, y


def open_map_imge(coord):
    """coord - координаты объекта
    открывает картинку по нужным координатам
    :return None"""
    try:
        toponym_longitude, toponym_lattitude = coord

        delta = "0.005"
        map_params = {
            "ll": ",".join([toponym_longitude, toponym_lattitude]),
            "spn": ",".join([delta, delta]),
            "l": "map"
        }
        map_api_server = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(map_api_server, params=map_params)
        map_file = "map.png"
        with open(map_file, "wb") as file:
            file.write(response.content)
        return map_file
    except Exception:
        print("ошибка")
        return None

