from django.urls import path
from . import views

app_name = 'member'

urlpatterns = [
    path('', views.MemberList.as_view(), name="all"),
    path("new/", views.CreateMember.as_view(), name="create"),
    path("by/<username>/", views.UserMember.as_view(), name="for_user"),
    path("by/<username>/<int:pk>/", views.MemberDetail.as_view(), name="single"),
    path("delete/<int:pk>/", views.DeleteMember.as_view(), name="delete"),
]
