import json
from django.test import TestCase
from rest_framework.test import APIClient

from snepdata.models import Certification, Token

IP = '0.0.0.0'

class APITestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.token = Token.objects.get_or_create(ip=IP)
        super(APITestCase, cls).setUpClass()

    def setUp(self) -> None:
        self.certification = Certification(artist='artiste', category='category', certification_type='OR')
        self.certification.save()
        self.APIClient =  APIClient()
        self.APIClient.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token[0].token))

    def test_get_token(self) -> None:
        request = self.APIClient.get('/api/token', format='json')
        response = json.loads(request.content)

        self.assertEqual(request.status_code, 200)
        self.assertIsNotNone(response['token'])
        token = response['token']
        Token.objects.get(token=token)

    def test_cetifications(self) -> None:
        request = self.APIClient.get('/api/certifications', format='json')
        response = json.loads(request.content)

        self.assertEqual(request.status_code, 200)
        self.assertEqual(len(response['results']), 1)
        self.assertEqual(response['results'][0]['artist'], self.certification.artist)
        self.assertEqual(response['results'][0]['category'], self.certification.category)

class APIFilterTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super(APIFilterTestCase, cls).setUpClass()
        cls.token = Token.objects.get_or_create(ip=IP)

    def setUp(self) -> None:
        self.APIClient =  APIClient()
        self.APIClient.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token[0].token))

        self.certification1 = Certification(artist='jean', category='album', certification_type='OR')
        self.certification2 = Certification(artist='jean', category='single', certification_type='OR')
        self.certification3 = Certification(artist='didier', category='single', certification_type='OR')
        self.certification4 = Certification(artist='didier', category='album', certification_type='DIAMANT')
        self.certification5 = Certification(artist='didier', category='album', certification_type='DIAMANT')
        self.certification1.save()
        self.certification2.save()
        self.certification3.save()
        self.certification4.save()
        self.certification5.save()

    def test_by_name(self) -> None:
        artist = 'jean'
        request = self.APIClient.get(f'/api/certifications/search?artist={artist}', format='json')
        response = json.loads(request.content)

        self.assertEqual(request.status_code, 200)
        self.assertEqual(len(response['results']), 2)
        for result in response['results']:
            self.assertEqual(result['artist'], artist)

    def test_by_category(self) -> None:
        category = "single"
        request = self.APIClient.get(f'/api/certifications/search?category={category}', format='json')
        response = json.loads(request.content)

        self.assertEqual(request.status_code, 200)
        self.assertEqual(len(response['results']), 2)
        for result in response['results']:
            self.assertEqual(result['category'], category)

    def test_by_certification(self) -> None:
        certification = 'DIAMANT'
        request = self.APIClient.get(f'/api/certifications/search?certification={certification}', format='json')
        response = json.loads(request.content)

        self.assertEqual(request.status_code, 200)
        self.assertEqual(len(response['results']), 2)
        for result in response['results']:
            self.assertEqual(result['certification_type'], certification)