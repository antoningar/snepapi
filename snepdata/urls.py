from django.urls import path, include
from snepdata.views import CertificationViewSet
from snepdata.router import CustomReadOnlyRouter

router = CustomReadOnlyRouter()
router.register('certifications', CertificationViewSet)
urlpatterns = router.urls