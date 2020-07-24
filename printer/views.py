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
        check = CheckCreateSerializer()
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
        client_check = check.create(request.data, 'client')
        kitchen_check = check.create(request.data, 'kitchen')
        django_rq.enqueue(task.convertHtmltoPDF, render(request, 'client_check.html').content, task.create_path(id_order, 'client'), client_check)
        django_rq.enqueue(task.convertHtmltoPDF, render(request, 'kitchen_check.html').content, task.create_path(id_order, 'kitchen'), kitchen_check)
        return Response(status=200, data=data_ok)
