from django.test import TestCase
from rest_framework.test import APIClient

import json

from snepdata.models import Certification

class APITestCase(TestCase):
    def setUp(self) -> None:
        self.certification = Certification(artist='artiste', category='category', certification_type='OR')
        self.certification.save()
        self.APIClient =  APIClient()

    def test_cetifications(self):
        request = self.APIClient.get('/api/certifications', format='json')
        response = json.loads(request.content)

        self.assertEqual(request.status_code, 200)
        self.assertEqual(len(response['results']), 1)
        self.assertEqual(response['results'][0]['artist'], self.certification.artist)
        self.assertEqual(response['results'][0]['category'], self.certification.category)