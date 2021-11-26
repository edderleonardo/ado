
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic.base import TemplateView


class HomeTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "pages/home.html"


class PassengersView(LoginRequiredMixin, TemplateView):
    template_name = "pages/passengers.html"


class DriversView(LoginRequiredMixin, TemplateView):
    template_name = "pages/drivers.html"


class RoutesView(LoginRequiredMixin, TemplateView):
    template_name = "pages/routes.html"


class BusesView(LoginRequiredMixin, TemplateView):
    template_name = "pages/buses.html"


class SalesView(LoginRequiredMixin, TemplateView):
    template_name = "pages/sales.html"
