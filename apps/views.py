from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView, FormView, DeleteView

from apps.forms import RegistrationForm, LoginForm, StreamForm, PayForm, ProfileForm
from apps.models import User, Product, Category, Stream, Transaction


class AlijahonHomeView(ListView):
    template_name = 'home.html'
    model = Category
    context_object_name = 'cate'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['pro_data'] = Product.objects.all()
        data['cate_data'] = Category.objects.all()

        referal_id = self.request.GET.get('referal')
        if referal_id:
            self.request.session['user_id'] = referal_id

        return data

class ShopView(TemplateView):
    template_name = 'shop.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['cate'] = Category.objects.all()
        return data


class AccountView(TemplateView):
    template_name = 'acc.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['user'] = self.request.user
        return data


class AdminMarketView(ListView):
    template_name = 'market.html'
    context_object_name = 'products'

    def get_queryset(self):
        category_id = self.kwargs.get('pk')
        if category_id:
            return Product.objects.filter(category_id=category_id)
        return Product.objects.all()

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['cate'] = Category.objects.all()
        return data


class SorovTemplateView(TemplateView):
    template_name = 'sorov.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['cate'] = Category.objects.all()
        return data


class HavolaTemplateView(TemplateView):
    template_name = 'havolalar.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['streams'] = Stream.objects.all()
        return data

class StatistikaTemplateView(LoginRequiredMixin ,TemplateView):
    template_name = 'statistika.html'

    def get_context_data(self, **kwargs):
        context  = super().get_context_data(**kwargs)
        streams = Stream.objects.filter(user=self.request.user)
        context['streams'] = streams
        return context


class KonkursTemplateView(TemplateView):
    template_name = 'konkurs.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['cate'] = Category.objects.all()
        return data


class PayTemplateView(LoginRequiredMixin, FormView):
    template_name = 'pay.html'
    form_class = PayForm
    success_url = '/pay/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['transactions'] = Transaction.objects.filter(user=self.request.user)
        return context

    def form_valid(self, form):
        user = self.request.user
        transaction = form.save(commit=False)

        amount = transaction.amount
        typee = transaction.type

        # проверка баланса
        if typee == 'money' and user.balance < amount:
            messages.error(self.request, "Balansingiz yetarli emas!")
            return self.form_invalid(form)

        if typee == 'coin' and user.coins < amount:
            messages.error(self.request, "Tangangiz yetarli emas!")
            return self.form_invalid(form)

        transaction.user = user
        transaction.save()

        if typee == 'money':
            user.balance -= amount
        else:
            user.coins -= amount

        user.save()

        messages.success(self.request, "So'rovingiz qabul qilindi!")
        return super().form_valid(form)


class ReferalTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'referal.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['cate'] = Category.objects.all()
        data['referrals'] = self.request.user.referrals.all().order_by('-date_joined')
        return data


class SettingsTemplateView(LoginRequiredMixin, FormView):
    template_name = 'sozlamalar.html'
    form_class = ProfileForm
    success_url = reverse_lazy('settings')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Profil saqlandi!')
        return super().form_valid(form)




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
        data['cate'] = Category.objects.all()
        return data


class LoginFormView(FormView):
    form_class = LoginForm
    success_url = reverse_lazy('home')
    template_name = 'home.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['cate'] = Category.objects.all()
        return data

    def form_invalid(self, form):
        for error_message in form.errors.values():
            messages.error(self.request, error_message)
        return super().form_invalid(form)


# class RegisterView(CreateView):
#     queryset = User.objects.all()
#     form_class = RegistrationForm
#     template_name = 'home.html'
#     success_url = reverse_lazy('home')
#
#     def get_context_data(self, **kwargs):
#         data = super().get_context_data(**kwargs)
#         data['cate'] = Category.objects.all()
#         return data
#
#     def form_invalid(self, form):
#         for error_message in form.errors.values():
#             messages.error(self.request, error_message)
#         return super().form_invalid(form)

class RegisterView(CreateView):
    queryset = User.objects.all()
    form_class = RegistrationForm
    template_name = 'home.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['cate'] = Category.objects.all()
        return data

    def form_valid(self, form):
        user = form.save(commit=False)

        referrer_id = self.request.session.get('referrer_id')
        if referrer_id:
            try:
                referrer = User.objects.get(id=referrer_id)
                user.referred_by = referrer
            except User.DoesNotExist:
                pass

        user.save()
        if 'referrer_id' in self.request.session:
            del self.request.session['referrer_id']
        login(self.request, user)
        messages.success(self.request, "Muvaffaqiyatli ro'yxatdan o'tdingiz!")
        return redirect(self.success_url)

    def form_invalid(self, form):
        for error_message in form.errors.values():
            messages.error(self.request, error_message)
        return super().form_invalid(form)

class LogOut(View):
    def get(self, request):
        logout(request)
        return redirect('home')


class ProductDetailView(DetailView):
    queryset = Product.objects.all()
    template_name = 'detail.html'
    context_object_name = 'data'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['cate'] = Category.objects.all()
        return data


class StreamCreateView(CreateView):
    form_class = StreamForm
    success_url = reverse_lazy('havolalar')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.view_count = 0
        return super().form_valid(form)

    def form_invalid(self, form):
        for error_message in form.errors.values():
            messages.error(self.request, error_message)
        return redirect('market')

    #     def get_context_data(self, **kwargs):
    #         data = super().get_context_data(**kwargs)
    #     data['cate'] = Category.objects.all()
    #     return data
    #
    # def form_invalid(self, form):
    #     for error_message in form.errors.values():
    #         messages.error(self.request, error_message)
    #     return super().form_invalid(form)

class HavolaDeleteView(DeleteView):
    queryset = Stream.objects.all()
    template_name = 'havolalar.html'
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('havolalar')

def DistrictListView(request):
    region_id = request.GET.get('region_id')
    district_list = list(District.objects.filter(region_id=region_id).values("id","title"))

    return JsonResponse(data=district_list, safe=False)