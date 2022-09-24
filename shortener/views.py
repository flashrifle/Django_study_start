from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from shortener.models import Users
from django.views.decorators.csrf import csrf_exempt

def index(request):
    user = Users.objects.filter(username="admin").first()
    email = user.email if user else "Anonymus User!"
    print(email)
    print(request.user.is_authenticated) # 로그인이 되었는가
    if request.user.is_authenticated is False:
        email = "Anonymus User!" # 로그인이 안됐다면 출력됨
    print(email)
    return render(request, "base.html", {"welcome_msg": f"hello {email}"})

@csrf_exempt
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