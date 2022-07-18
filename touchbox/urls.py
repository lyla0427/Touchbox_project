from rest_framework.routers import DefaultRouter

from touchbox import views

router = DefaultRouter()
# router.register(r"competitions", views.competitionList())
from django.urls import path
from django.views.generic import TemplateView

app_name = "touchbox"

urlpatterns = [
    path('', TemplateView.as_view(template_name='touchbox/initial.html')),
    path('about/', TemplateView.as_view(template_name='touchbox/about.html')),
    path('players/', views.playerList),
    path('players/<int:pk>/', views.playerDetail),
    path("competitions/", views.competitionList),
    path('touchmaps/', views.touchMapDetail, name='touchmap-detail')
]
