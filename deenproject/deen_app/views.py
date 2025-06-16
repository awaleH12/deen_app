from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django import forms

# Create your views here.

def home(request):
  return render(request, 'deen_app/home/index.html')

def about(request):
  return render(request, 'deen_app/home/about.html')

@login_required
def dashboard(request):
  return render(request, 'deen_app/home/dashboard.html')
