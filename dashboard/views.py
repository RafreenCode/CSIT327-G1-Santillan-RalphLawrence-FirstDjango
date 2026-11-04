from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView
from accounts.models import CustomUser


def home(request):
    return HttpResponse("Dashboard is working.")

class AdminPanelView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "dashboard/admin_panel.html"

    def test_func(self):
        user = self.request.user
        return user.can_access_admin_panel

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["member_count"] = CustomUser.objects.count()
        context["student_count"] = CustomUser.objects.filter(role=CustomUser.Role.STUDENT).count()
        context["instructor_count"] = CustomUser.objects.filter(role=CustomUser.Role.INSTRUCTOR).count()
        context["admin_count"] = CustomUser.objects.filter(role=CustomUser.Role.ADMIN).count()
        context["recent_members"] = CustomUser.objects.order_by("-date_joined", "-pk")[:8]
        return context

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["member_count"] = CustomUser.objects.count()
        context["is_admin"] = self.request.user.can_access_admin_panel
        return context
