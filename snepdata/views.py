from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response

from snepdata.models import Certification, Token
from snepdata.serializers import CertificationSerializer
from snepdata.permissions import BearerTokenPermissions

class CertificationViewSet(ReadOnlyModelViewSet):
    queryset = Certification.objects.all().order_by('-certification_date')
    serializer_class = CertificationSerializer
    lookup_field = 'certification'
    permission_classes = (BearerTokenPermissions,)

class CertificationFilterViewSet(CertificationViewSet):
    def get_queryset(self):
        queryset = Certification.objects.all().order_by('-certification_date')
        artist = self.request.query_params.get('artist')
        category = self.request.query_params.get('category')
        certification = self.request.query_params.get('certification')

        queryset = queryset.filter(artist__icontains=artist) if artist else None
        queryset = queryset.filter(category__iexact=category) if category else None
        queryset = queryset.filter(certification_type__iexact=certification) if certification else None
        
        return queryset

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    ip = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')
    return ip

class GetTokenView(APIView):
    def get(self, request):
        token, created = Token.objects.get_or_create(ip=get_client_ip(request))

        return Response({
            'token': token.token
        })