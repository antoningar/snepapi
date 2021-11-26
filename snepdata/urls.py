from snepdata.views import CertificationViewSet, CertificationFilterViewSet
from snepdata.router import CustomReadOnlyRouter

router = CustomReadOnlyRouter()
router.register('certifications', CertificationViewSet)
router.register('certifications/search',CertificationFilterViewSet)
urlpatterns = router.urls