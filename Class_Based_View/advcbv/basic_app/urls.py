from django.urls import path
from . import views

# this enables the template for eg: base.html to use template tagging to refer {% url 'basic_app:list'%}
app_name = 'basic_app'

# reason for giving it a name, for url template tag
# so basic_app:list reference in base.html
urlpatterns = [
    path('', views.SchoolListView.as_view(), name='list'),
    path('<int:pk>/', views.SchoolDetailedView.as_view(), name='detail'),
    path('create/', views.SchoolCreateView.as_view(), name='create'),
    path('update/<int:pk>/', views.SchoolUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', views.SchoolDeleteView.as_view(), name='delete')
]
