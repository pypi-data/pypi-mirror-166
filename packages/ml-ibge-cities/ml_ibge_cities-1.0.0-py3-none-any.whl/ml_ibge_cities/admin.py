from django.contrib import admin
from django.shortcuts import render
from django.urls import path

from ml_ibge_cities.ibge import IBGE


class MLIBGECitiesAdmin(admin.ModelAdmin):
    change_form_template = "ml_ibge_cities/ml_ibge_cities_change_form.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path(
                "admin/select/cities/options",
                self._get_cities_options,
                name="select_cities",
            ),
        ]
        return my_urls + urls

    def _get_cities_options(self, request):
        context = {}
        state = request.GET.get("state")
        if state:
            context["cities"] = [city["distrito-nome"] for city in IBGE.get_cities(state)]
        return render(request, "ml_ibge_cities/ml_ibge_cities_options.html", context)
