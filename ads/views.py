from django.shortcuts import render
from .models import Ad

def ad_list_view(request):
    ads = Ad.objects.all().order_by('-created_at')
    return render(request, 'ads/index.html', {'ads': ads}) 