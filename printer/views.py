from django.utils.datastructures import MultiValueDictKeyError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Printer, Check
from .serializers import CheckCreateSerializer, CheckListSerializer
from django.shortcuts import render
from django.http import HttpResponse
from . import task
import django_rq


class CheckCreateView(APIView):
    """ Создание чека """

    def post(self, request):
        check_serilizer = CheckCreateSerializer()
        client = 'client'
        kitchen = 'kitchen'
        data_ok = {
            "ok": "Чеки успешно созданы"
        }
        data_error = {
            "error": "Для данного заказа уже созданы чеки"
        }
        data_error2 = {
            "error": "Для данной точки не настроено ни одного принтера"
        }

        # Проверка наличия принтера в данной точке
        try:
            Printer.objects.get(point_id=request.data.get('point_id'))
        except Printer.MultipleObjectsReturned:
            pass
        except Printer.DoesNotExist:
            return Response(status=400, data=data_error2)

        id_order = request.data.get('id')

        # Проверка наличия заказа в базе по чекам
        for obj in Check.objects.all():
            if obj.order['id'] == id_order:
                return Response(status=400, data=data_error)

        # Создание чеков для клиента и кухни
        client_check_obj = check_serilizer.create(request.data, client)
        kitchen_check_obj = check_serilizer.create(request.data, kitchen)

        # Создается задание для воркера
        # Создаю html шаблон для клиента
        html_temp = render(request, 'client_check.html', context={'order': client_check_obj.order}).content
        django_rq.enqueue(task.convertHtmltoPDF, html_temp, task.create_path(id_order, client), client_check_obj)

        # Создаю html шаблон для кухни
        html_temp = render(request, 'kitchen_check.html', context={'order': kitchen_check_obj.order}).content
        django_rq.enqueue(task.convertHtmltoPDF, html_temp, task.create_path(id_order, kitchen), kitchen_check_obj)
        return Response(status=200, data=data_ok)


class AvailableCheckView(APIView):
    """Вывод списка id чеков по принтеру"""

    def get(self, request):
        # Получаю api_key из request
        api_key = request.GET.__getitem__('api_key')

        # Проверка на наличие модели с полученным api_key
        try:
            printer = Printer.objects.get(api_key=api_key)
        except Printer.DoesNotExist:
            return Response(status=401, data={"error": "Ошибка авторизации"})

        # Получение cписка чеков у принтера
        cheks = Check.objects.filter(printer_id=printer, status='new')
        check_serializer = CheckListSerializer(cheks, many=True)
        # Ставлю задачу на смену статуса чеков
        django_rq.enqueue(task.change_of_status, cheks, 'rendered')
        return Response(status=200, data=check_serializer.data)


class CheckView(APIView):
    """Вывод pdf чеков"""
    def get(self, request):
        # Получаю api_key и check_id из request
        try:
            api_key = request.GET.__getitem__('api_key')
            check_id = request.GET.__getitem__('check_id')
        except MultiValueDictKeyError:
            return Response(status=404)
        # Проверки request
        try:
            check = Check.objects.get(pk=check_id)
        except Check.DoesNotExist:
            return Response(status=400, data={"error": "Данного чека не существует"})

        if check.pdf_file is None:
            return Response(status=400, data={"error": "Для данного чека не сгенерирован PDF-файл"})

        try:
            printer = Printer.objects.get(api_key=api_key)
        except Printer.DoesNotExist:
            return Response(status=401, data={"error": "Ошибка авторизации"})
        # Загрузка pdf файла
        pdf_file = open(check.pdf_file.path, 'rb').read()
        # Формирование response
        file_name = check.pdf_file.path.rsplit('/')[len(check.pdf_file.path.rsplit('/'))-1]
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(file_name)
        check.status = 'printed'
        check.save()
        return response



