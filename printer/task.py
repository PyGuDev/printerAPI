import json
import requests
import base64
import os
from django.core.files.base import ContentFile
from django.conf import settings

URL = 'http://localhost:32770'


def create_path(id, type_check):
    """Создаем имя для pdf"""
    folder = os.path.join(settings.MEDIA_ROOT, 'pdf')
    file = str(id) + '_' + type_check + '.pdf'
    return os.path.join(folder, file)


def convertHtmltoPDF(html, to_pdf, obj):
    """Функция отправки html на wkthmltopdf"""
    data = {
        'contents': str(base64.b64encode(html), 'utf-8'),
    }
    headers = {'Content-Type': 'application/json', }
    response = requests.post(URL, data=json.dumps(data), headers=headers)
    file = ContentFile(response.content)
    obj.pdf_file.save(to_pdf, file, save=True)


def change_of_status(objects, status):
    """Функция смены статуса объектов"""

    for obj in objects:
        obj.status = status
        obj.save()
