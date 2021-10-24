from django.db import models

# Create your models here.

class Certification(models.Model):
    CERTIFICATION_TYPES = (
        ('O', 'OR'),
        ('P', 'PLATINE'),
        ('DP', 'DOUBLE PLATINE'),
        ('TP', 'TRIPLE PLATINE'),
        ('D', 'DIAMANT'),
        ('DD', 'DOUBLE DIAMANT'),
        ('TD', 'TRIPLE DIAMANT'),
        ('QD', 'QUADRUPLE DIAMANT'),
    )

    artist = models.CharField(max_length=150)
    title = models.CharField(max_length=150)
    label = models.CharField(max_length=150)
    release_date = models.DateField()

    category = models.CharField(max_length=50)
    certification_type = models.CharField(max_length=2, choices=CERTIFICATION_TYPES)
    certificaion_date = models.DateField()