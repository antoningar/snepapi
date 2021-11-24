from django.test import TestCase
from unittest import mock
from re import compile

import snepdata.management.commands.update as update

# https://gist.github.com/gruber/8891611
REGEX_URL = "((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*"

def get_wrong_html():
    with open('snepdata/test/resources/wrong_page.html', 'r') as page:
        return page.read()

class Response:
    def __init__(self, text, status_code):
        self.text = text
        self.status_code = status_code

def mocked_get_csv(*args, **kwargs):
    return Response(get_wrong_html(), 200)

def mocked_get_wrong_url(*args, **kwargs):
    return Response('okletsgo', 500)

class WebSnepTestCase(TestCase):
    def test_url_snep(self):
        url = update.get_csv_path()
        pattern = compile(REGEX_URL)
        assert pattern.match(url)

    @mock.patch('requests.get', side_effect=mocked_get_csv)
    def test_class_missing(self, mocked_get_csv):
        with self.assertRaises(ValueError):
            update.get_csv_path()

        assert mocked_get_csv.called

    @mock.patch('requests.get', side_effect=mocked_get_wrong_url)
    def test_wrong_url(self, mocked_get_wrong_url):
        with self.assertRaises(ValueError):
            update.get_csv_path()

        assert mocked_get_wrong_url.called

        with self.assertRaises(ValueError):
            update.get_csv()