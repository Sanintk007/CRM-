from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Count
from django.utils.timezone import now, timedelta
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Company, Contact, Report
from .forms import SignUpForm, CompanyForm, ContactForm, ReportForm

# API imports
from rest_framework import viewsets, permissions
from .serializers import CompanySerializer, ContactSerializer, ReportSerializer


@login_required
def home(request):
    companies = Company.objects.filter(owner=request.user)
    contacts = Contact.objects.filter(user=request.user)
    reports = Report.objects.filter(owner=request.user)
    return render(request, 'dashboard.html', {
        'companies': companies,
        'contacts': contacts,
        'reports': reports
    })


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/')

@login_required
def company_list(request):
    companies = Company.objects.all().order_by('id')
    paginator = Paginator(companies, 10)  # Show 10 companies per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'company_list.html', {'page_obj': page_obj})


@login_required
def company_detail(request, pk):
    company = get_object_or_404(Company, pk=pk, owner=request.user)
    contacts = Contact.objects.filter(company=company)
    return render(request, 'company_detail.html', {'company': company, 'contacts': contacts})


@login_required
def add_company(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            company = form.save(commit=False)
            company.owner = request.user
            company.save()
            return redirect('/companies/')
    else:
        form = CompanyForm()
    return render(request, 'company_form.html', {'form': form})



def edit_company(request, pk):
    company = get_object_or_404(Company, pk=pk)
    
    if request.method == "POST":
        form = CompanyForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            return redirect('company_detail', pk=company.pk)
    else:
        form = CompanyForm(instance=company)
    
    return render(request, 'edit_company.html', {'form': form, 'company': company})


@login_required
def contact_list(request):
    contacts = Contact.objects.all().order_by('id')
    paginator = Paginator(contacts, 10)  # Show 10 companies per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'contacts_list.html', {'page_obj': page_obj})

@login_required
def add_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        form.fields['company'].queryset = Company.objects.all()
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user
            contact.save()
            return redirect('contact_list')
    else:
        form = ContactForm()
    return render(request, 'contact_form.html', {'form': form})


@login_required
def report_list(request):
    reports = Report.objects.all().order_by('id')
    paginator = Paginator(reports, 10)  # Show 10 companies per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'report_list.html', {'page_obj': page_obj})


@login_required
def add_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.owner = request.user
            report.save()
            return redirect('/reports/')
    else:
        form = ReportForm()
    return render(request, 'report_form.html', {'form': form})


# REST API ViewSets
class CompanyViewSet(viewsets.ModelViewSet):
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Company.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ContactViewSet(viewsets.ModelViewSet):
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticated]
    #queryset = Contact.objects.all()

    
    def get_queryset(self):
        return Contact.objects.filter(user=self.request.user)


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReportViewSet(viewsets.ModelViewSet):
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Report.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)




@login_required

def dashboard(request):
    company_count = Company.objects.count()
    contact_count = Contact.objects.count()
    report_count = Report.objects.count()

    context = {
        'company_count': company_count,
        'contact_count': contact_count,
        'report_count': report_count,
    }
    return render(request, 'dashboard.html', context)