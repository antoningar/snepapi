from snepdata.views import CertificationViewSet, CertificationFilterViewSet, GetTokenView
from snepdata.router import CustomReadOnlyRouter

from django.urls import path

router = CustomReadOnlyRouter()
router.register('certifications', CertificationViewSet)
router.register('certifications/search',CertificationFilterViewSet)

urlpatterns = router.urls
urlpatterns += [
    path('token', GetTokenView.as_view())
]