from django.contrib import admin
from .models import Prod, Choice, Report, ReportChoice
from order.utils import Handler
import json


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 0


class ProdAdmin(admin.ModelAdmin):
    list_display = ['url', 'method']
    inlines = [ChoiceInline]
    actions = ['run']

    def get_actions(self, request):
        actions = super(ProdAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def run(self, request, queryset):
        for query in queryset:
            report = Report(url=query.url)
            report.save()
            for choice in Choice.objects.filter(prod_id=query.id):
                handler = Handler()
                if query.method == 'Get':
                    response = handler.get_rsp_from_url(query.url, params=choice.param)
                    if response.status_code != int(choice.statusCode):
                        choice = ReportChoice(report_id=report.id, result='Code Error', reponse=choice.reponse,
                                              param=choice.param,
                                              statusCode='{}!={}'.format(response.status_code, choice.statusCode))
                        choice.save()
                        continue
                    if response.json() != json.loads(choice.reponse):
                        choice = ReportChoice(report_id=report.id, result='Response Error',
                                              reponse='{}!={}'.format(response.json(), json.loads(choice.reponse)),
                                              param=choice.param, statusCode=choice.statusCode)
                        choice.save()
                        continue
                    choice = ReportChoice(report_id=report.id, result='Pass', reponse=choice.reponse,
                                          param=choice.param, statusCode=choice.statusCode)
                    choice.save()


class ReportChoiceInline(admin.TabularInline):
    model = ReportChoice
    readonly_fields = ('result', 'param', 'reponse', 'statusCode', 'was_published_recently')
    can_delete = False
    extra = 0


class ReportAdmin(admin.ModelAdmin):
    list_display = ['url']
    readonly_fields = ('url',)
    inlines = [ReportChoiceInline]


admin.site.register(Prod, ProdAdmin)
admin.site.register(Report, ReportAdmin)
