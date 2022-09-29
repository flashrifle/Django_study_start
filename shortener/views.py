from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from shortener.forms import RegisterForm, LoginForm
from shortener.models import Users
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm
from django.core.paginator import Paginator

def index(request):
    user = Users.objects.filter(id=request.user.id).first()
    email = user.email if user else "Anonymus User!"
    print("Logged in?", request.user.is_authenticated) # 로그인이 되었는가
    if request.user.is_authenticated is False:
        email = "Anonymus User!" # 로그인이 안됐다면 출력됨
    print(email)
    return render(request, "base.html", {"welcome_msg": "hello"})

@csrf_exempt # 사이트 위변조 방지 코드
def get_user(request, user_id):
    print(user_id)
    if request.method == ('GET'):
        abc = request.GET.get("abc")
        xyz = request.GET.get("xyz")
        user = Users.objects.filter(pk=user_id).first()
        return render(request, "base.html", {"user":user, "params":[abc,xyz]})
    elif request.method == "POST":
        username = request.GET.get("username")
        if username:
            user = Users.objects.filter(pk=user_id).update(username=username)
        
        return JsonResponse(status=201, data=dict(msg="Yot Just reached with Post Method"), safe=False)

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        msg = "올바르지 않은 데이터 입니다."
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            msg = "회원가입 완료"
        return render(request, "register.html", {"form":form, "msg":msg})
    else:
        form = RegisterForm()
        return render(request, "register.html", {"form":form})

def login_view(request):
    is_ok = False
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            raw_password = form.cleaned_data.get("password")
            remember_me = form.cleaned_data.get("remember_me")
            msg = "올바른 유저ID와 패스워드를 입력하세요."
            try:
                user = Users.objects.get(email=email)
            except Users.DoesNotExist:
                msg = "올바른 유저ID와 패스워드를 입력하세요."
            else:
                if user.check_password(raw_password):
                    msg = None
                    login(request, user)
                    is_ok = True
                    request.session["remember_me"] = remember_me

                    # if not remember_me:
                    #     request.session.set_expirey(0)
    else:
        msg = None
        form = LoginForm()
    print("REMEMBER_ME: ", request.session.get("remember_me"))
    return render(request, "login.html", {"form": form, "msg": msg, "is_ok": is_ok})

def logout_view(request):
    logout(request)
    return redirect("login")

@login_required #로그아웃 상태일시 로그인 페이지로 이동하게 해주는 기능
def list_view(request):
    page = int(request.GET.get("p",1))
    users = Users.objects.all().order_by("-id") # 오름차순 정렬
    paginator = Paginator(users, 10)
    users = paginator.get_page(page)

    return render(request, "boards.html", {"users":users})