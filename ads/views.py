from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404 
from django.http import HttpResponseForbidden
from django.contrib import messages
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

@login_required
def ad_update_view(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    if ad.user != request.user:
        return HttpResponseForbidden("Вы не можете редактировать это объявление.")
    if request.method == 'POST':
        form = AdForm(request.POST, request.FILES or None, instance=ad)
        if form.is_valid():
            form.save()
            return redirect('ads:ad_list')
    else:
        form = AdForm(instance=ad)

        context = {
        'form': form,
        'page_title': f'Редактировать: {ad.title}',
        'ad': ad,
        }
    return render(request, 'ads/ad_form.html', context)

@login_required
def ad_delete_view(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    if ad.user != request.user:
        return HttpResponseForbidden("Вы не можете удалить это объявление.")
    
    if request.method == 'POST':
        ad_title = ad.title
        ad.delete()
        messages.success(request, f'Объявление "{ad_title}" успешно удалено.')
        return redirect('ads:ad_list')
    context = {
        'ad': ad,
        'page_title': f'Удалить: {ad.title}'
    }
    return render(request, 'ads/ad_confirm_delete.html', context)