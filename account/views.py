from django.shortcuts import render, redirect
from account.forms import SignupForm
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.urls import reverse

# Create your views here.

# 회원가입 account:signup
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            auth_login(request, user)
            messages.success(request, '회원가입이 완료되었습니다. 로그인해주세요.')
            return redirect('account:login')
    else:
        form = SignupForm()
    return render(request, 'account/signup.html', {'form': form})

# 로그인 account:login
class CustomLoginView(LoginView):
    def get_success_url(self):
        # return '/frige/'  # 로그인 성공 시 리다이렉트할 URL
        if 'next' in self.request.GET:
            return self.request.GET['next']
        else:
            return reverse('frige:frige_list')  # 로그인 성공 시 리다이렉트할 URL
        
    # 로그인 성공 후 호출됨
    def form_valid(self, form):
        return super().form_valid(form)

login_view = CustomLoginView.as_view(template_name='account/login.html')

# 로그아웃
def logout_view(request):
    logout(request)
    return redirect('account:login')