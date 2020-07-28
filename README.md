# Printer API
![alt text](https://github.com/smenateam/assignments/blob/master/backend/images/arch.png)
---
 Сервис по обработки печати чеков. Принимаент запрос от ERP на создание чеков заказа, ставит задачу воркеру на генерацию pdf файла с шаблона html, заносит pdf файл
 в базу. Принимает запрос от приложения на вывод списка готовых чеков для печати, а также принимает запрос от приложения на получение pdf файла чека.
### Сервис работает на 
* Django 1.11
* Django Rest Framework 3.11
* Python 3.6
### Инфроструктурные вещи запускаются через docker-compose
* Redis
* Postgresql 9.6
* wkhtmltopdf
##### Для их запуска используйте файл docker-compose.yml
### Методы для ERP
[POST]  /create_checks/ Принимает запрос с json данными
### Методы для приложения
[GET] /new_checks/?api_key=key1 Принимает запрос с ключом api_key принтера и отправляет список чеков готовых для печати у данного принтера
***
[GET] /checks/?api_key=key&check_id=1 Принимает запрос с ключами api_key и check_id возвращает pdf файл чека
 
