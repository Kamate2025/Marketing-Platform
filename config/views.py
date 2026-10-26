from django.http import JsonResponse
from django.shortcuts import render


def home_view(request):
    return render(request, 'home.html', {
        'page_title': 'Kamate Marketing Studio',
        'meta_description': 'AI-powered marketing workflow for planning, creating, and publishing social content across channels.',
    })


def health_view(request):
    return JsonResponse({'status': 'ok', 'service': 'kamate-marketing-studio'})
