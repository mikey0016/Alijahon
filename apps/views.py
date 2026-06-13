from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, CreateView, FormView, DeleteView
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator

from apps.forms import RegistrationForm, LoginForm, StreamForm, PayForm, ProfileForm
from apps.models import User, Product, Category, Stream, Transaction, Order, WishList, District


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
            self.request.session['referrer_id'] = referal_id

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


class StatistikaTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'statistika.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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
        data['referral_count'] = self.request.user.referrals.count()
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
        user = form.save(commit=False)

        new_password = self.request.POST.get('new_password')
        confirm_password = self.request.POST.get('confirm_password')

        if new_password:
            if new_password != confirm_password:
                messages.error(self.request, "Yangi parollar bir-biriga mos kelmadi!")
                return self.form_invalid(form)

            if len(new_password) < 6:
                messages.error(self.request, "Yangi parol kamida 6 belgidan iborat bo'lishi kerak!")
                return self.form_invalid(form)

            user.password = make_password(new_password)
            messages.success(self.request, "Parol muvaffaqiyatli o'zgartirildi!")
            messages.warning(self.request, "Iltimos, qayta kiring!")

        user.save()
        messages.success(self.request, "Profil muvaffaqiyatli yangilandi!")
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
            referrer = User.objects.get(id=referrer_id)
            user.referred_by = referrer
        user.save()
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
        # Wishlistda bor yoki yo'qligini tekshirish
        if self.request.user.is_authenticated:
            data['in_wishlist'] = WishList.objects.filter(
                user=self.request.user,
                product=self.object
            ).exists()
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


class HavolaDeleteView(DeleteView):
    queryset = Stream.objects.all()
    template_name = 'havolalar.html'
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('havolalar')


class WishListView(LoginRequiredMixin, ListView):
    model = WishList
    template_name = 'wishlist.html'
    context_object_name = 'wishlist_items'

    def get_queryset(self):
        return WishList.objects.filter(user=self.request.user).select_related('product')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['cate'] = Category.objects.all()
        return data


class WishListToggleView(View):
    def post(self, request):
        import json
        try:
            data = json.loads(request.body)
            product_id = data.get('pk')

            if not product_id:
                return JsonResponse({'error': 'Product ID required'}, status=400)

            product = get_object_or_404(Product, id=product_id)
            wishlist_item = WishList.objects.filter(user=request.user, product=product)

            if wishlist_item.exists():
                wishlist_item.delete()
                return JsonResponse({
                    'active': False,
                    'message': 'Mahsulot wishlistdan o\'chirildi',
                    'count': WishList.objects.filter(user=request.user).count()
                })
            else:
                WishList.objects.create(user=request.user, product=product)
                return JsonResponse({
                    'active': True,
                    'message': 'Mahsulot wishlistga qo\'shildi',
                    'count': WishList.objects.filter(user=request.user).count()
                })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)



def check_wishlist_status(request):
    product_id = request.GET.get('pk')
    if not product_id:
        return JsonResponse({'error': 'Product ID required'}, status=400)

    exists = WishList.objects.filter(
        user=request.user,
        product_id=product_id
    ).exists()

    return JsonResponse({'active': exists})


def district_view(request):
    region_id = request.GET.get('region_id')
    district_list = list(District.objects.filter(region_id=region_id).values("id", "title"))
    return JsonResponse(data=district_list, safe=False)


def success_accept(request):
    if request.method == 'POST':
        product_id = request.POST['product_id']
        product = Product.objects.get(id=product_id)

        quantity = int(request.POST['quantity'])
        total_price = product.price * quantity

        order = Order.objects.create(
            product=product,
            full_name=request.POST['full_name'],
            phone_number=request.POST['phone_number'],
            quantity=quantity,
            total_price=total_price,
            status='pending'
        )
        return render(request, 'success_accept.html', {'order': order})
    else:
        return redirect('home')