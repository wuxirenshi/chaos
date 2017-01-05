# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Prod(models.Model):
    class Meta:
        verbose_name_plural = '订单项目管理'
        verbose_name = '项目'

    choice = (('Get', 'Get'), ('Post', 'Post'), ('Delete', 'Delete'), ('Put', 'Put'))

    url = models.CharField(max_length=300)
    method = models.CharField(max_length=10, choices=choice, default='get')

    def __unicode__(self):
        return self.method


class Choice(models.Model):
    class Meta:
        verbose_name_plural = '参数校验组'
        verbose_name = '参数校验'

    prod = models.ForeignKey(Prod)
    param = models.CharField(max_length=500)
    reponse = models.CharField(max_length=500)
    statusCode = models.CharField(max_length=500, default='')


class Report(models.Model):
    url = models.TextField(max_length=1000, default='')


class ReportChoice(models.Model):
    report = models.ForeignKey(Report)
    result = models.CharField(max_length=1000)
    param = models.CharField(max_length=500, default='')
    reponse = models.CharField(max_length=500, default='')
    statusCode = models.CharField(max_length=500, default='')

    def was_published_recently(self):
        return self.result == 'Pass'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'State'


