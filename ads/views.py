from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect 
from .models import Ad
from .forms import AdForm

def ad_list_view(request):
    ads = Ad.objects.all().order_by('-created_at')
    return render(request, 'ads/ad_list.html', {'ads': ads}) 

@login_required
def ad_create_view(request):
    if request.method == 'POST':
        form = AdForm(request.POST, request.FILES or None)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.user = request.user
            ad.save()
            return redirect('ads:ad_list')
    else:
        form = AdForm()
    return render(request, 'ads/ad_form.html', {'form': form})