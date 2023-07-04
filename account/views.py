from django.shortcuts import render, redirect
from account.forms import SignupForm
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.urls import reverse
# MQTT 통신
import paho.mqtt.client as mqtt
import core.settings as settings

host_id = settings.MQTT_BROKER_URL
port = 1883
_topic = "refri/"
# MQTT 연결
client = mqtt.Client()

# MQTT --------------
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    if rc == 0:
        print("MQTT 연결 성공, [[refri/login/#]] . . ")
    else: print("연결 실패 : ", rc)

def on_message(client, userdata, msg):
    pass
        
client.on_connect = on_connect
client.on_message = on_message

try:
    client.connect(host_id, port)
    client.loop_start()
except Exception as err:
    print(f"ERR ! /{err}/")
# --------------------
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
            print("다시 회원가입해주세요")
            print(form.errors)
    else: SignupForm()
    context = {'form': form}
    return render(request, 'account/signup.html', context)

# 로그인 account:login
class CustomLoginView(LoginView):
    def get_success_url(self):
        return ''  # 로그인 성공 시 리다이렉트할 URL
        # if 'next' in self.request.GET:
        #     return self.request.GET['next']
        # else:
        #     return reverse('frige:frige_list')  # 로그인 성공 시 리다이렉트할 URL
        
    # 로그인 성공 후 호출됨
    def form_valid(self, form):
        username = self.request.POST['username']
        topic = _topic + "login"
            
        # User 닉네임 Android 에 전달
        client.publish(topic, username)
        print("Topic : {}, User : {}".format(topic, username))
        return super().form_valid(form)

login_view = CustomLoginView.as_view(template_name='account/login.html')

# 로그아웃
def logout_view(request):
    topic = _topic + "logout"
    msg = "success"
    
    # User 닉네임 Android 에 전달
    client.publish(topic, msg)
    print("Topic : {}, {}".format(topic, msg))
    
    logout(request)
    return redirect('account:login')