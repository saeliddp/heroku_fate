from django.urls import path
from . import views

# home is where the survey actually takes place
# update refreshes the home page and sends data to server
urlpatterns = [
    path('', views.consent, name='version2-consent'),
    path('demographics/', views.demographics, name='version2-demographics'),
    path('instructions<int:respondent_id>/', views.instructions, name='version2-instructions'),
    path('home<int:id>/', views.home, name='version2-home'),
    path('thanks<int:respondent_id>/', views.thanks, name='version2-thanks'),
]