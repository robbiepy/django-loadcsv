from django.db import models


class ModelWithCSV(models.Model):
    class Meta:
        abstract = True

    class CSV:
        field_delimeter = ","
        line_end = "\n"
        cmd_extra = ""
