import json
import fitz  # PyMuPDF
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from .forms import CustomerForm, DocumentUploadForm
from .models import Customer, CustomerDocument

def home(request):
    return render(request, "home.html")

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('create_customer')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')

def create_customer(request):
    if request.method == 'POST':
        customer_form = CustomerForm(request.POST)
        document_form = DocumentUploadForm(request.POST, request.FILES)
        if customer_form.is_valid() and document_form.is_valid():
            customer = customer_form.save(commit=False)
            customer.created_by = request.user
            customer.save()

            document = document_form.save(commit=False)
            document.customer = customer
            document.save()
            extracted_text = extract_text_from_document(document.attached_file.path)
            document.extracted_json = json.dumps(extracted_text)
            document.save()

            return redirect('customer_list')
    else:
        customer_form = CustomerForm()
        document_form = DocumentUploadForm()
    return render(request, 'create_customer.html', {
        'customer_form': customer_form,
        'document_form': document_form
    })

def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'customer_list.html', {'customers': customers})

def extract_text_from_document(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return {"extracted_text": text}

def process_document_upload(request):
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.save()
            extracted_text = extract_text_from_document(document.attached_file.path)
            document.extracted_json = json.dumps(extracted_text)
            document.save()

            return redirect('customer_list')
    else:
        form = DocumentUploadForm()
    return render(request, 'upload_document.html', {'form': form})

def customer_list_extracted(request):
    customers = Customer.objects.all()
    customer_documents = CustomerDocument.objects.filter(customer__in=customers)
    customer_data = []

    for customer in customers:
        documents = customer_documents.filter(customer=customer)
        document_data = []
        for document in documents:
            if document.extracted_json:
                extracted_data = json.loads(document.extracted_json)
            else:
                extracted_data = {}
            document_data.append({
                'file': document.attached_file,
                'extracted_data': extracted_data
            })
        customer_data.append({
            'customer': customer,
            'documents': document_data
        })

    return render(request, 'customer_list_data.html', {'customer_data': customer_data})


