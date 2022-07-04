from django.db import models

from user_management.models import Users


class DocumentSourceTable(models.Model):
    """定义文献来源表

    """
    liter_name = models.CharField(
        max_length=200,
        verbose_name="文档名称",
        help_text="文档的名称，200个字符以内",
    )
    created_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name="上传时间",
    )
    iter_type = models.CharField(
        max_length=10,
        verbose_name="文件类型",
        help_text="文件类型名称，例如：pdf、xml等"
    )
    pub = models.CharField(
        max_length=100,
        verbose_name="文献出版商",
        null=True,
        blank=True,
    )
    remark = models.CharField(
        max_length=1000,
        verbose_name="备注",
        help_text="对该文献的备注，1000个字符以内。"
    )
    upload = models.FileField(
        upload_to='uploads/',
    )
    creator = models.ForeignKey(
        Users,
        on_delete=models.PROTECT,
        verbose_name="上传者ID",
        help_text="上传者的ID作为外键",
    )

    class Meta:
        db_table = 'db_documents_source_table'
        verbose_name = "文献来源表"
        verbose_name_plural = verbose_name


class LiteratureDataTable(models.Model):
    """定义文献抽取的数据表

    """
    mat_entity = models.CharField(
        max_length=100,
        verbose_name="材料实体名称",
    )
    enha_name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="增强体名称",
    )
    enha_value = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="增强体值",
    )
    perf = models.CharField(
        max_length=100,
        verbose_name="性能名称",
    )
    perf_value = models.CharField(
        max_length=100,
        verbose_name="性能值",
    )
    process = models.CharField(
        max_length=1000,
        verbose_name="工艺",
        null=True,
        blank=True,
    )
    liter = models.ForeignKey(
        DocumentSourceTable,
        on_delete=models.PROTECT,
    )
    user = models.ForeignKey(
        Users,
        on_delete=models.PROTECT,
    )

    class Meta:
        db_table = 'db_literature_data_table'
        verbose_name = "文献数据表"
        verbose_name_plural = verbose_name


class UserLexicon(models.Model):
    """定义用户自定义词库表

    """
    describle = models.CharField(
        max_length=1000,
        verbose_name="中文描述",
        help_text="材料实体的中文描述",
    )
    entity = models.CharField(
        max_length=1000,
        verbose_name="材料实体英文描述",
    )
    user = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table = 'db_user_lexicon'
        verbose_name = "用户词库表"
        verbose_name_plural = verbose_name
