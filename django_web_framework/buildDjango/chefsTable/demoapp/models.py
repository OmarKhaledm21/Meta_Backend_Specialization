from django.db import models

# Create your models here.


class Employees(models.Model):
    id = models.CharField(primary_key=True, max_length=200)

    class Meta:
        db_table = 'Employees'
