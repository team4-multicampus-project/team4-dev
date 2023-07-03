from django.shortcuts import render, redirect, get_object_or_404
from .forms import FrigeForm
from .models import Frige, Drink
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# MQTT 통신
import account.views as account

# MQTT 연결
client = account.client
_topic = "refri/"

# Create your views here.

# 냉장고 등록 및 리스트 frige:frige_list  
# @login_required
def frige_list(request):
    user = request.user
    friges = Frige.objects.filter(user=user)
    form = FrigeForm()
    
    client.publish(f"{_topic}refriname", "")
    print("Topic : {}, Refri : {}".format(f"{_topic}refriname", "main"))

    if request.method == 'POST':
        form = FrigeForm(request.POST)
        if form.is_valid():
            frige = form.save(commit=False)
            frige.user = user
            frige.save()
            return redirect('frige:frige_list')
    #추가
    if request.method == 'GET' and 'delete_frige_id' in request.GET:
        delete_frige_id = request.GET.get('delete_frige_id')
        try:
            frige_to_delete = Frige.objects.get(id=delete_frige_id, user=user)
            frige_to_delete.delete()
            return redirect('frige:frige_list')
        except Frige.DoesNotExist:
            pass
    context = {
        'friges': friges,
        'form': form
    }
    return render(request, 'frige/frige_list.html', context)

# @login_required
# def frige_list(request):
#     user = request.user
#     if user.is_authenticated:  # 인증된 사용자인지 확인
#         friges = Frige.objects.filter(user=user)
#     else:
#         friges = None

#     form = FrigeForm()

#     if request.method == 'POST':
#         form = FrigeForm(request.POST)
#         if form.is_valid():
#             frige = form.save(commit=False)
#             frige.user = user
#             frige.save()
#             return redirect('frige:frige_list')

#     context = {
#         'friges': friges,
#         'form': form
#     }
#     return render(request, 'frige/frige_list.html', context)

# 냉장고 상태 및 주류 품목 조절
# @login_required
def frige_state(request, frige_id):
    frige = get_object_or_404(Frige, id=frige_id, user=request.user)
    drinks = frige.drinks.all()
    current_frige_id = frige.id  # 현재 페이지의 냉장고 ID
    
    client.publish(f"{_topic}refriname", frige.name)
    print("Topic : {}, Refri : {}".format(f"{_topic}refriname", frige.name))

    user = request.user
    friges = Frige.objects.filter(user=user)

    context = {
        'frige': frige,
        'drinks': drinks,
        'friges': friges,
        'current_frige_id': current_frige_id,  # 현재 페이지의 냉장고 ID 변수를 전달
    }
    return render(request, 'frige/frige_state.html', context)

# 수량조절 
@csrf_exempt
def handle_quantity(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode('utf-8'))
            drink_id = data.get('drink_id')
            quantity = data.get('quantity')

            if drink_id is not None and quantity is not None:
                try:
                    drink = Drink.objects.get(id=drink_id)
                    drink.quantity = quantity
                    drink.save()
                    return JsonResponse({'status': 'success', 'result': drink.quantity})
                except Drink.DoesNotExist:
                    return JsonResponse({'status': 'error', 'message': 'Item not found.'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid JSON data.'})

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data.'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})
