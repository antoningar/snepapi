from django.test import TestCase
from unittest import mock

from django.conf import settings
import snepdata.management.commands.update as update

def get_csv():
    with open('snepdata/test/resources/data.csv', 'r') as csv_files:
        return csv_files.read()

def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, csv_data, status_code):
            self.content = csv_data.encode('utf-8')
            self.status_code = status_code

    if args[0] == settings.TEST['CSV_PATH']:
        return MockResponse(get_csv(), 200)

    return MockResponse(None, 404)

def mocked_get_csv_path():
    return settings.TEST['CSV_PATH']

class UpdateTestCase(TestCase):
    def setUp(self):
        print('setting up')

    @mock.patch('snepdata.management.commands.update.get_csv_path', side_effect=mocked_get_csv_path)
    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_get_csv(self, mock_update_get_csv, mock_requests_get):
        csv_content = update.get_csv()
        assert csv_content == get_csv()