from django.db import models
from loadcsv.models import ModelWithCSV


class SimpleTable1(models.Model):
    a = models.CharField(max_length=255)
    b = models.CharField(max_length=255)
    c = models.CharField(max_length=255)

    class Meta:
        db_table = 'test1'


class SimpleTable2(ModelWithCSV):
    a = models.CharField(max_length=255)
    b = models.CharField(max_length=255)
    c = models.CharField(max_length=255)

    class Meta:
        db_table = 'test2'

    class CSV(ModelWithCSV.CSV):
        field_delimeter = ";"
        cmd_extra = "(a, @d, c)"
