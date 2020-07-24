from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Printer, Check
from .serializers import CheckCreateSerializer
from django.shortcuts import render
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
        # Создаю html шаблон
        html_temp = render(request, 'client_check.html', context={'order': client_check_obj.order}).content
        django_rq.enqueue(task.convertHtmltoPDF, html_temp, task.create_path(id_order, client), client_check_obj)

        html_temp = render(request, 'kitchen_check.html', context={'order': kitchen_check_obj.order}).content
        django_rq.enqueue(task.convertHtmltoPDF, html_temp, task.create_path(id_order, kitchen), kitchen_check_obj)
        return Response(status=200, data=data_ok)
