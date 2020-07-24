import json
import requests
import base64
from django.core.files.base import ContentFile

URL = 'http://localhost:32770'


def create_path(id, type_check):
    """Создаем имя для pdf"""
    file = str(id) + '_' + type_check + '.pdf'
    return file


def convertHtmltoPDF(html, to_pdf, obj):
    """Функция отправки html на wkthmltopdf"""
    data = {
        'contents': str(base64.b64encode(html), 'utf-8'),
    }
    headers = {'Content-Type': 'application/json', }
    response = requests.post(URL, data=json.dumps(data), headers=headers)
    file = ContentFile(response.content)
    obj.pdf_file.save(to_pdf, file, save=True)
