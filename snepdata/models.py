from django.db import models

# Create your models here.

CERTIFICATION_TYPES = (
    ('OR', 'OR'),
    ('PLATINE', 'PLATINE'),
    ('DOUBLE PLATINE', 'DOUBLE PLATINE'),
    ('TRIPLE PLATINE', 'TRIPLE PLATINE'),
    ('DIAMANT', 'DIAMANT'),
    ('DOUBLE DIAMANT', 'DOUBLE DIAMANT'),
    ('TRIPLE DIAMANT', 'TRIPLE DIAMANT'),
    ('QUADRUPLE DIAMANT', 'QUADRUPLE DIAMANT'),
)

class Certification(models.Model):
    id = models.BigAutoField(primary_key=True)
    artist = models.CharField(max_length=150)
    title = models.CharField(max_length=150, null=True, blank=True)
    label = models.CharField(max_length=150,null=True, blank=True)
    release_date = models.DateTimeField(null=True, blank=True)

    category = models.CharField(max_length=50)
    certification_type = models.CharField(max_length=20, choices=CERTIFICATION_TYPES)
    certification_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.artist} | {self.title} | {self.certification_type} | {self.certification_date}'