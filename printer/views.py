from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Printer, Check
from .serializers import CheckCreateSerializer


class CheckCreateView(APIView):
    """ Создание чека """

    def post(self, request):
        check = CheckCreateSerializer()
        data_error = {
            "error" : "Для данного заказа уже созданы чеки"
        }
        data_error2 = {
            "error": "Для данной точки не настроено ни одного принтера"
        }
        
        #Проверка наличия принтера в данной точке
        try:
            Printer.objects.get(point_id=request.data.get('point_id'))
        except Printer.DoesNotExist:
            return Response(status=400, data=data_error2) 
        
        #Проверка наличия заказа в базе по чекам
        for obj in Check.objects.all():
            if obj.order['id'] == request.data.get('id'):
                return Response(status=400, data=data_error)
        check.create(request.data, 'client')
        check.create(request.datat, 'kitchen')
            
        return Response(status=200)