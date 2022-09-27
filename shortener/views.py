from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from shortener.forms import RegisterForm
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
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        msg = "가입되어 있지 않거나 로그인이 필요합니다."
        if form.is_valid():
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                msg = "로그인 성공"
                login(request, user)
        return render(request, "login.html", {"form":form, "msg":msg})
    else:
        form = AuthenticationForm()
        return render(request, "login.html", {form:form})

def logout_view(request):
    logout(request)
    return redirect("index")

@login_required #로그아웃 상태일시 로그인 페이지로 이동하게 해주는 기능
def list_view(request):
    page = int(request.GET.get("p",1))
    users = Users.objects.all().order_by("-id") # 오름차순 정렬
    paginator = Paginator(users, 10)
    users = paginator.get_page(page)

    return render(request, "boards.html", {"users":users})