from django.urls import path, include
from django.shortcuts import redirect
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('companies', views.CompanyViewSet, basename='company')
router.register('contacts', views.ContactViewSet, basename='contact')
router.register('reports', views.ReportViewSet, basename='report')

urlpatterns = [
    path('home/', views.dashboard, name='home_page'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('companies/', views.company_list, name='company_list'),
    path('companies/add/', views.add_company, name='add_company'),
    path('companies/<int:pk>/edit/', views.edit_company, name='edit_company'),
    path('companies/<int:pk>/', views.company_detail, name='company_detail'),
    path('contacts/', views.contact_list, name='contact_list'),
    path('contacts/add/', views.add_contact, name='add_contact'),
    path('reports/', views.report_list, name='report_list'),
    path('reports/add/', views.add_report, name='add_report'),
    path('', views.dashboard, name='dashboard'),
    path('', lambda request: redirect('dashboard')),
    path('api/', include(router.urls)),
]
