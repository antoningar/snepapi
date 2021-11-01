from django.contrib import admin
from snepdata.models import Certification


class CertificationAdmin(admin.ModelAdmin):
    search_fields = ['artist','title','release_date','category','certification_type','certification_date']
    ordering = ('-certification_date',)

    class Meta:
        Model = Certification

admin.site.register(Certification, CertificationAdmin)