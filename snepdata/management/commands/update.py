import requests
from bs4 import BeautifulSoup
from datetime import datetime

from snepdata.models import Certification
from django.utils.timezone import make_aware
from django.conf import settings
from django.core.management.base import BaseCommand

def str_to_datetimedate(str_date):
    if str_date == '':
        return
    return make_aware(datetime.strptime(str_date, '%d/%m/%Y'))

def get_csv_path():
    link = settings.PAGE_LINK
    r = requests.get(link)
    if r.status_code != 200:
        raise ValueError
    soup = BeautifulSoup(r.text, 'html.parser')
    a = soup.find("a", {"class": "btn_red btn_print icon-download"})
    if not a:
        raise ValueError
    return a['href']

def get_csv():
    path = get_csv_path()
    r_csv = requests.get(path)
    if r_csv.status_code != 200:
        raise ValueError
    return r_csv.content.decode('utf-8')

def insert_certification(tmp_cert):
    try:
        current_cert = Certification.objects.get(artist=tmp_cert.artist, title=tmp_cert.title)
        if current_cert.certification_type != tmp_cert.certification_type and\
            tmp_cert.certification_date > current_cert.certification_date:

            current_cert.certification_type = tmp_cert.certification_type
            current_cert.save()
    except Certification.DoesNotExist:
        tmp_cert.save()

def line_to_certification(line):
    item = line.split(';')
    return Certification(
        artist=item[0],
        title=item[1],
        label=item[2],
        release_date=str_to_datetimedate(item[5]),
        category=item[3],
        certification_type=item[4].upper(),
        certification_date=str_to_datetimedate(item[6]),
    )

def insert_csv(csv_content):
    csv_lines = csv_content.replace('\t','').split('\n')
    for line in  csv_lines[1:]:
        if line != '':
            tmp_cert = line_to_certification(line)
            insert_certification(tmp_cert)

class Command(BaseCommand):
    help = 'Update db with current snep certifications'

    def handle(self, *args, **options):
        csv_content = get_csv()
        insert_csv(csv_content)
