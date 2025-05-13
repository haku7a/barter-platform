from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404 
from django.http import HttpResponseForbidden
from django.contrib import messages
from .models import Ad
from .forms import AdForm, ExchangeProposalForm
from django.core.paginator import Paginator
from django.db.models import Q

def ad_list_view(request):
    ads_list = Ad.objects.all().order_by('-created_at')
    query = request.GET.get('q')
    category_filter = request.GET.get('category')
    condition_filter = request.GET.get('condition')
    if query:
        ads_list = ads_list.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

    if category_filter:
        ads_list = ads_list.filter(category__icontains=category_filter)

    if condition_filter:
        ads_list = ads_list.filter(condition__icontains=condition_filter)

    paginator = Paginator(ads_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    query_params = request.GET.copy()
    if 'page' in query_params:
        del query_params['page']
    current_query_params_encoded = query_params.urlencode()

    context = {
        'page_obj': page_obj,
        'current_query_params': current_query_params_encoded
    }
    return render(request, 'ads/ad_list.html', context)

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

@login_required
def exchange_proposal_create_view(request, ad_receiver_pk):
    ad_receiver = get_object_or_404(Ad, pk=ad_receiver_pk)
    if ad_receiver.user == request.user:
        messages.error(request, "Вы не можете сделать предложение обмена для своего собственного объявления.")
        return redirect('ads:ad_list')
    user_ads_count = Ad.objects.filter(user=request.user).count()
    if user_ads_count == 0:
        messages.warning(request, "У вас нет объявлений, которые можно предложить для обмена. Сначала создайте объявление.")
        return redirect('ads:ad_create')
    if request.method == 'POST':
        form = ExchangeProposalForm(request.POST, user=request.user)
        if form.is_valid():
            proposal = form.save(commit=False)
            proposal.ad_receiver = ad_receiver
            proposal.save()
            messages.success(request, f"Ваше предложение для объявления '{ad_receiver.title}' успешно отправлено!")
            return redirect('ads:ad_list') 
        else:
            form = ExchangeProposalForm(user=request.user)

        context = {
        'form': form,
        'ad_receiver': ad_receiver,
        }
        return render(request, 'ads/exchange_proposal_form.html', context)
