from django.contrib import admin
from django.db.models.aggregates import Avg
from django.http import HttpResponse
from django.shortcuts import render
from restrecommender.models import Restaurantdata
from django.views.generic import TemplateView
from django.db.models import Count


class MyAdminSite(admin.AdminSite):

    def stats(self, request):  # your custom view function
        qs1 = (Restaurantdata.objects
               .values('cluster_label')
               .annotate(dcount=Count('cluster_label'))
               .order_by()
               )
        qs2 = (Restaurantdata.objects.values(
            'cluster_label').annotate(dcount=Avg('cost')).order_by())
        return render(request, "admin/statistics.html",  {'user': request.user, 'site_header': mysite.site_header, 'has_permission': mysite.has_permission(request), 'site_url': mysite.site_url, 'qs1': qs1, 'qs2': qs2})

    def get_urls(self):
        from django.urls import path

        urlpatterns = super().get_urls()
        urlpatterns += [
            path('stats/', self.admin_view(self.stats)),
        ]
        return urlpatterns
    pass


mysite = MyAdminSite()
