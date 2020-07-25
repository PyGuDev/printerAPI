from rest_framework import serializers
from .models import Printer, Check


class CheckCreateSerializer(serializers.ModelSerializer):
    """Сериалайзер чеков и создание их"""

    class Meta:
        model = Check
        fields = "__all__"

    def create(self, validated_data, check_type):
        # Поиск модели принтера
        printer = Printer.objects.get(
            point_id=validated_data.get('point_id', None),
            check_type=check_type)
        # Создание модели чека
        check = Check.objects.create(
            type=check_type,
            order=validated_data,
            status='new',
            pdf_file=None,
            printer_id=printer
        )
        return check


class CheckListSerializer(serializers.ModelSerializer):
    """Сериалайзер списка чеков"""
    class Meta:
        model = Check
        fields = ['pk']



