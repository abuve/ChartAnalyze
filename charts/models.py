from django.db import models

# Create your models here.


class ChartType(models.Model):
    name = models.CharField(verbose_name=u'图表类型', max_length=35)

    class Meta:
        verbose_name = "图表类型"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return "{0}".format(self.name)

    __str__ = __unicode__


class MeasurementType(models.Model):
    name = models.CharField(verbose_name=u'类型', max_length=100)
    value = models.CharField(verbose_name=u'表达式', max_length=100)

    class Meta:
        verbose_name = "度量聚合类型"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return "{0}".format(self.name)

    __str__ = __unicode__


class DataSetField(models.Model):
    field = models.CharField(verbose_name=u'字段名称', max_length=100)
    alias = models.CharField(verbose_name=u'转换名称', max_length=100, blank=True, null=True)
    field_type_choices = (
        ('dis', 'dis'),
        ('mst', 'mst'),
    )
    field_type = models.CharField(choices=field_type_choices, verbose_name=u'字段类型', max_length=100)
    mst_type = models.ForeignKey(MeasurementType, verbose_name=u'度量聚合', on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        verbose_name = "数据集字段表"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return "{0}".format(self.field)

    __str__ = __unicode__


class PanelCompose(models.Model):
    chart_type = models.ForeignKey(ChartType, verbose_name='图表类型', on_delete=models.SET_NULL, null=True)
    name = models.CharField(verbose_name=u'图表名称', max_length=200)
    dis = models.ManyToManyField(DataSetField, verbose_name='维度', related_name='dis')
    mst = models.ManyToManyField(DataSetField, verbose_name='度量', related_name='mst')
    data_src = models.CharField(verbose_name=u'数据源表', max_length=200)
    procedure = models.CharField(verbose_name=u'过滤条件', max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = "仪表盘"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return "{0}".format(self.name)

    __str__ = __unicode__