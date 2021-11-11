from django.test import TestCase
from unittest import mock
from datetime import date

from django.conf import settings
import snepdata.management.commands.update as update

def mocked_get_csv_path():
    return settings.TEST['CSV_PATH']

def get_csv():
    with open('snepdata/test/resources/data.csv', 'r') as csv_files:
        return csv_files.read()

def get_html():
    with open('snepdata/test/resources/page.html', 'r') as page:
        return page.read()

class MockCertification:
    def __init__(self, certification_type, certification_date):
        self.certification_type = certification_type
        self.certification_date = certification_date
        self.artist = None
        self.title = None
        self.save_has_been_called = False

    def save(self):
        self.save_has_been_called = True

def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, status_code):
            self.text = None
            self.content = None
            self.status_code = status_code

    class CsvMockResponse:
        def __init__(self, csv_data, status_code):
            self.content = csv_data.encode('utf-8')
            self.status_code = status_code

    class HtmlMockResponse:
        def __init__(self, text, status_code):
            self.text = text
            self.status_code = status_code

    if args[0] == settings.TEST['CSV_PATH']:
        return CsvMockResponse(get_csv(), 200)
    elif args[0] == settings.PAGE_LINK:
        return HtmlMockResponse(get_html(), 200)

    return MockResponse(500)


mock_certif_or = None

class UpdateTest(TestCase):
    def mock_get_certification(artist, title):
        global mock_certif_or
        return mock_certif_or

    def setUp(self):
        global mock_certif_or
        self.certif_line = 'NEPAL;ADIOS BAHAMAS;ADIOS BAHAMAS;Albums;Or;10/01/2020;25/03/2021'
        self.mock_certif_platine = MockCertification('PLATINE', date(2021, 11, 12))
        mock_certif_or = MockCertification('OR', date(2021, 11, 11))

    @mock.patch('snepdata.management.commands.update.get_csv_path', side_effect=mocked_get_csv_path)
    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_get_csv(self, mock_update_get_csv, mock_requests_get):
        csv_content = update.get_csv()

        assert mock_update_get_csv.called
        assert mock_requests_get.called
        assert csv_content == get_csv()

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_get_csv_path(self, mocked_requests_get):
        csv_path = update.get_csv_path()

        assert mocked_requests_get.called
        assert csv_path == mocked_get_csv_path()

    def test_line_to_certification(self):
        certification = update.line_to_certification(self.certif_line)

        assert certification.artist == self.certif_line.split(';')[0]
        assert certification.title == self.certif_line.split(';')[1]
        assert certification.label == self.certif_line.split(';')[2]
        assert certification.release_date == update.str_to_datetimedate(self.certif_line.split(';')[5])
        assert certification.category == self.certif_line.split(';')[3]
        assert certification.certification_type == self.certif_line.split(';')[4].upper()
        assert certification.certification_date == update.str_to_datetimedate(self.certif_line.split(';')[6])

    @mock.patch('snepdata.management.commands.update.Certification.objects.get', side_effect=mock_get_certification)
    def test_insert_certification_outdate(self, mock_get_certification):
        global mock_certif_or
        self.mock_certif_platine.certification_date = date(2021,10,12)
        update.insert_certification(self.mock_certif_platine)
        self.assertFalse(mock_certif_or.save_has_been_called)

        assert mock_get_certification.called

    @mock.patch('snepdata.management.commands.update.Certification.objects.get', side_effect=mock_get_certification)
    def test_insert_certification(self, mock_get_certification):
        global mock_certif_or
        update.insert_certification(self.mock_certif_platine)

        assert mock_get_certification.called
        self.assertTrue(mock_certif_or.save_has_been_called)



