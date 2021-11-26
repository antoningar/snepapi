from rest_framework.viewsets import ReadOnlyModelViewSet

from snepdata.models import Certification
from snepdata.serializers import CertificationSerializer

class CertificationViewSet(ReadOnlyModelViewSet):
    queryset = Certification.objects.all().order_by('-certification_date')
    serializer_class = CertificationSerializer
    lookup_field = 'certification'

class CertificationFilterViewSet(CertificationViewSet):
    def get_queryset(self):
        queryset = Certification.objects.all().order_by('-certification_date')
        artist = self.request.query_params.get('artist')
        category = self.request.query_params.get('category')
        certification = self.request.query_params.get('certification')
        
        if artist:
            queryset = queryset.filter(artist__icontains=artist)
        if category:
            queryset = queryset.filter(category__iexact=category)
        if certification:
            queryset = queryset.filter(certification_type__iexact=certification)
        
        return queryset