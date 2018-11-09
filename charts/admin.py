from django.contrib import admin

# Register your models here.
from charts import models


admin.site.register(models.PanelCompose)
admin.site.register(models.MeasurementType)
admin.site.register(models.DataSetField)
admin.site.register(models.ChartType)