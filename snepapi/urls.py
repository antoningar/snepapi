from django.contrib import admin
from django.urls import path, include

import snepdata.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(snepdata.urls)),
]
