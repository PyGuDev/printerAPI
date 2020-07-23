from django.db import models
from django.contrib.postgres.fields import JSONField


CHECK_TYPE  = [
        ('kitchen', 'kitchen'),
        ('client', 'client'),
    ]


class Printer(models.Model):
    """ Модель принтеров для печати чека"""
    name = models.CharField('Название принтера', max_length=30)
    api_key = models.CharField(max_length=255)
    check_type = models.CharField('Тип чека', max_length=8, choices=CHECK_TYPE)
    point_id = models.IntegerField('Точка')

    def __str__(self):
        return self.name
    
    
    class Meta:
        verbose_name = 'Принтер'
        verbose_name_plural = 'Принтеры'
    

class Check(models.Model):
    """Модель чека"""
    STATUS = [
        ('new', 'new'),
        ('rendered', 'rendered'),
        ('printed', 'printed'),
    ]

    printer_id = models.ForeignKey("Printer", on_delete=models.CASCADE)
    type = models.CharField('Тип чека', max_length=8, choices=CHECK_TYPE)
    order = JSONField('Информация заказа')
    status = models.CharField('Статус', max_length=10, choices=STATUS)
    pdf_file = models.FileField('PDF', upload_to='pdf/', blank=True)


    class Meta:
        verbose_name = 'Чек'
        verbose_name_plural = 'Чеки'