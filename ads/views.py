from django.shortcuts import render

def ads_view(request):
    return render(request, 'ads/index.html')
