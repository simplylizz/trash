from django.urls import path

from . import views


urlpatterns = [
    path('slot/add/', views.AvailabilitySlotCreateView.as_view()),
    path('slot/', views.PersonsAvailabilitySlotListView.as_view()),
    path('interview/add/', views.InterviewCreateView.as_view()),
]
