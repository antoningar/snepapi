from rest_framework.viewsets import ReadOnlyModelViewSet

from snepdata.models import Certification
from snepdata.serializers import CertificationSerializer

class CertificationViewSet(ReadOnlyModelViewSet):
    queryset = Certification.objects.all().order_by('-certification_date')
    serializer_class = CertificationSerializer
    lookup_field = 'certification'
