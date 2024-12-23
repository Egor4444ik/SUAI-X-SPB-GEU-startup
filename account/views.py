from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm
from django.contrib.auth.decorators import login_required
from .models import ozon
import matplotlib.pyplot as plt

@login_required
def dashboard(request):
    ozon_instance = ozon.objects.get_or_create(user=request.user)[0]
    ozon_instance.update_data()
    print(ozon_instance.data.get('iphone_16', {}))
    return render(request,
                  'account/dashboard.html',
                  {'section': 'dashboard'})

def wildberries_analitic(request):
    return render(request, 'account/wildberries_analitic.html', {'section': 'wildberries_analitic'})

def ozon_analitic(request):
    ozon_instance = ozon.objects.get_or_create(user=request.user)[0]
    goods = ozon_instance.data
    return render(request, 'account/ozon_analitic.html', {'section': 'ozon_analitic', "goods": goods})

def ozonGood(request, name):
    ozon_instance = ozon.objects.get_or_create(user=request.user)[0]
    good = name

    plt.close()
    plt.hist(ozon_instance.data.get(name, {})['buyer_sex'])
    plt.savefig("account/static/img/MaleToFemale.png")

    plt.close()
    data = []
    for i in range(len(ozon_instance.data.get(name, {})['count_from_FBS'])):
        data.append( ozon_instance.data.get(name, {})['count_from_FBS'][i] + ozon_instance.data.get(name, {})['count_from_FBO'][i] + ozon_instance.data.get(name, {})['count_from_other_fullfilment'][i] )
    plt.plot(ozon_instance.data.get(name, {})['date'], data)
    plt.savefig("account/static/img/QuantityToTime.png")

    plt.close()
    plt.plot(ozon_instance.data.get(name, {})['date'], ozon_instance.data.get(name, {})['price'])
    plt.savefig("account/static/img/PriceToTime.png")

    plt.close()
    plt.bar(data, ozon_instance.data.get(name, {})['buyer_age'])
    plt.savefig("account/static/img/PriceToQuantity.png")

    plt.close()
    plt.hist(ozon_instance.data.get(name, {})['buyer_region'])
    plt.savefig("account/static/img/Regions.png")

    plt.close()
    plt.bar(ozon_instance.data.get(name, {})['buyer_region'], ozon_instance.data.get(name, {})['buyer_age'])
    plt.savefig("account/static/img/AgeToRegions.png")

    plt.close()
    plt.plot(ozon_instance.data.get(name, {})['date'], ozon_instance.data.get(name, {})['buyer_age'])
    plt.savefig("account/static/img/AgeToTime.png")

    plt.close()
    plt.bar(ozon_instance.data.get(name, {})['price'], ozon_instance.data.get(name, {})['buyer_age'])
    plt.savefig("account/static/img/AgeToPrice.png")

    return render(request, 'account/good.html', {'section': 'ozon_analitic', "good": good})

def ozon_add_product(request):
    return render(request, 'account/add_product.html', {'section': 'ozon_analitic'})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
        return render(request, 'account/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Создать новый объект пользователя,
            # но пока не сохранять его
            new_user = user_form.save(commit=False)
            # Установить выбранный пароль
            new_user.set_password(
                user_form.cleaned_data['password'])
            # Сохранить объект User
            new_user.save()
            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'account/register.html',
                  {'user_form': user_form})