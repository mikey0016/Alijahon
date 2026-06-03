from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.hashers import make_password
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView

from apps.models import User, Product, Category


# Create your views here.


class AlijahonHomeView(TemplateView):
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['pro_data'] = Product.objects.all()
        data['cate_data'] = Category.objects.all()
        return data

    template_name = 'home.html'


class ShopView(TemplateView):
    template_name = 'shop.html'


class AccountView(TemplateView):
    template_name = 'acc.html'


class AdminMarketView(TemplateView):
    template_name = 'market.html'


class SorovTemplateView(TemplateView):
    template_name = 'sorov.html'


class HavolaTemplateView(TemplateView):
    template_name = 'havolalar.html'


class StatistikaTemplateView(TemplateView):
    template_name = 'statistika.html'


class KonkursTemplateView(TemplateView):
    template_name = 'konkurs.html'


class PayTemplateView(TemplateView):
    template_name = 'pay.html'


class ReferalTemplateView(TemplateView):
    template_name = 'referal.html'


class SettingsTemplateView(TemplateView):
    template_name = 'sozlamalar.html'


# class RegisterView(View):
#     def get(self, request):
#         return render(request, 'home.html')
#
#     def post(self, request):
#         first_name = request.POST.get('first_name')
#         phone = request.POST.get('phone')
#         password = request.POST.get('password')
#         cnf_password = request.POST.get('cnf_password')
#
#         if password != cnf_password:
#             messages.error(request, 'Password mos kelmadi')
#             return render(request, 'home.html')
#
#         if User.objects.filter(phone=phone).exists():  # phone_number → phone
#             messages.error(request, "Bu telefon raqam allaqachon ro'yxatdan o'tgan")
#             return render(request, 'home.html')
#
#         user = User(first_name=first_name, phone=phone)  # phone_number → phone
#         user.password = make_password(password)
#         user.save()
#         login(request, user)
#         return redirect('home')
#
#
# class LoginView(View):
#     def get(self, request):
#         return render(request, 'home.html')
#
#     def post(self, request):
#         phone_number = request.POST.get('phone')
#         password = request.POST.get('password')
#         queryset = User.objects.filter(phone=phone_number)
#         if queryset.exists():
#             user = queryset.first()
#             if user.check_password(password):
#                 login(request, user)
#                 return redirect('home')
#         messages.error(request, "Telefon yoki parol noto'g'ri")
#         return render(request, 'home.html')


class CategoryProductsView(TemplateView):
    template_name = 'shop.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        cate_it = self.kwargs.get('pk')
        if cate_it:
            data['pro_data'] = Product.objects.filter(category_id=cate_it)
            data['cate_name'] = Category.objects.filter(id=cate_it).first()

        else:
            data['pro_data'] = Product.objects.all()
        data['cate_date'] = Category.objects.all()
        return data


def AllCategory(request):
    cate = Category.objects.all()
    return render(request, 'base/base.html', {'cate': cate})
