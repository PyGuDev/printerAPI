from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase
from .models import Check, Printer
import time


class CreateCheckTests(APITestCase):
    def setUp(self):
        # Создаю url запроса
        self.url = reverse('create_checks')
        # Создаю две модели принтера
        Printer.objects.create(
            name="printer 1",
            api_key='key1',
            check_type='client',
            point_id=1
        )
        Printer.objects.create(
            name="printer 2",
            api_key='key2',
            check_type='kitchen',
            point_id=1
        )
        # Создаю правильный и не верный заказ
        self.data_ok = {
            "id": 4,
            "price": 780,
            "items": [
                {
                    "name": "Вкусная пицца",
                    "quantity": 2,
                    "unit_price": 250
                },
                {
                    "name": "Не менее вкусные роллы",
                    "quantity": 1,
                    "unit_price": 280
                }
            ],
            "address": "г. Уфа, ул. Ленина, д. 42",
            "client": {
                "name": "Иван",
                "phone": 9173332222
            },
            "point_id": 1
        }
        self.data_error = {
            "id": 4,
            "price": 780,
            "items": [
                {
                    "name": "Вкусная пицца",
                    "quantity": 2,
                    "unit_price": 250
                },
                {
                    "name": "Не менее вкусные роллы",
                    "quantity": 1,
                    "unit_price": 280
                }
            ],
            "address": "г. Уфа, ул. Ленина, д. 42",
            "client": {
                "name": "Иван",
                "phone": 9173332222
            },
            "point_id": 5
        }

    def test_response_status(self):
        # Отправляю pos запрос на сервер и получаю ответ
        # Правильный запрос
        response = self.client.post(self.url, self.data_ok, format='json')
        # Запрос с ошибкой точки
        response_error = self.client.post(self.url, self.data_error, format='json')
        # Запрос с ошибкой на уже созданный чек
        response_error_2 = self.client.post(self.url, self.data_ok, format='json')
        # Проверка статуса ответа
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_error.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_error_2.status_code, status.HTTP_400_BAD_REQUEST)
        # Проверка возврата ошибки
        self.assertEqual(response_error.data, {"error": "Для данной точки не настроено ни одного принтера"})
        self.assertEqual(response_error_2.data, {"error": "Для данного заказа уже созданы чеки"})

    def test_create_models(self):
        response = self.client.post(self.url, self.data_ok, format='json')
        # Проверка на создание модели чека
        self.assertEqual(Check.objects.count(), 2)
        self.assertEqual(Check.objects.all()[0].order, self.data_ok)
        self.assertEqual(Check.objects.all()[1].order, self.data_ok)


class ReturnChecksListTests(APITestCase):
    def setUp(self):
        # Создаю url запрос
        self.url = reverse('new_checks')
        # Создаю ключи запроса
        self.api_key_ok = '?api_key=key1'
        self.api_key_error = '?api_key=key4'
        # Создаю модели принтера
        Printer.objects.create(
            name="printer 1",
            api_key='key1',
            check_type='client',
            point_id=1
        )
        Printer.objects.create(
            name="printer 2",
            api_key='key2',
            check_type='kitchen',
            point_id=1
        )
        # Создаю заказ
        self.data_ok = {
            "id": 4,
            "price": 780,
            "items": [
                {
                    "name": "Вкусная пицца",
                    "quantity": 2,
                    "unit_price": 250
                },
                {
                    "name": "Не менее вкусные роллы",
                    "quantity": 1,
                    "unit_price": 280
                }
            ],
            "address": "г. Уфа, ул. Ленина, д. 42",
            "client": {
                "name": "Иван",
                "phone": 9173332222
            },
            "point_id": 1
        }

    def test_response_status(self):
        # Проверка статуса ответа
        response = self.client.get(self.url+self.api_key_ok, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(self.url+self.api_key_error)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # Проверка ответа
        self.assertEqual(response.data, {"error": "Ошибка авторизации"})

    def test_response_data(self):
        # Отправляем запрос на создание чеков
        self.client.post(reverse('create_checks'), self.data_ok, format='json')
        # Получаем ответ ввиде списка чеков
        response = self.client.get(self.url + self.api_key_ok)
        # Проверка ответа
        self.assertEqual(response.data, {"checks": [{"id": 5}]})