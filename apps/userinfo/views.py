from django.shortcuts import render,HttpResponse,redirect,reverse
from django.views.decorators.http import require_POST,require_GET
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from utils.captcha import ImgCaptcha,PhoneCaptcha
from utils import restful
from utils import yunpian
from django.contrib import auth
from io import BytesIO
from django.http import JsonResponse
from .models import *
from .forms import RegForm
from django.contrib.auth import get_user_model

User=get_user_model()

def index(request):
    return HttpResponse("hello")


def login(request):

    # if request.method=="POST":
    #     username=request.POST.get("username")
    #     password=request.POST.get("password")
    #     valid_code=request.POST.get("valid_code")
    #     if valid_code and valid_code.upper()==request.session
    # code=img_captcha(request)
    # print(code)
    return render(request,"login.html")



def get_phonecaptcha(request):
    ret = {"status": 0, "msg": ""}
    phone=request.POST.get("phone")
    code=PhoneCaptcha().get_code()
    print("code:",code)
    cache.set("phone",code,5*60)
    ret["msg"]=code
    return JsonResponse(ret)

def get_img_captcha(request):
    text, image = ImgCaptcha.gene_code()
    cache.set("code",text,5*60)
    # BytesIO：相当于一个管道，用来存储图片的流数据
    out = BytesIO()
    # 调用image的save方法，将这个image对象保存到BytesIO中
    image.save(out, 'png')
    # 将BytesIO的文件指针移动到最开始的位置
    out.seek(0)

    response = HttpResponse(content_type='image/png')
    # 从BytesIO的管道中，读取出图片数据，保存到response对象上
    response.write(out.read())
    response['Content-length'] = out.tell()

    # 12Df：12Df.lower()
    cache.set(text.lower(), text.lower(), 5 * 60)

    return response


def check_phone_exist(request):
    ret = {"status": 0, "msg": ""}
    phone = request.POST.get("phone")
    print(phone)
    is_exist =UserInfo.objects.filter(phone=phone).first()
    print("is_exist:",is_exist)
    if is_exist:
        ret["status"] = 1
        ret["msg"] = "手机号码已被注册！"
    # return JsonResponse(ret)
    return HttpResponse("hello")
def register(request):
    '''用户注册223'''
    ret = {"status": 0, "msg": ""}
    if request.method=="POST":
        print("用户注册")
        # print(request.data)
        form_obj=RegForm(request.POST)
        if form_obj.is_valid():
            username=request.POST.get("username")

            passwd=request.POST.get("password")
            print("passwd:",passwd)
            form_obj.cleaned_data.pop("re_password")
            avatar_img=request.FILES.get("avatar")

            print("avatar:",avatar_img)
            code=request.POST.get("valid_code")
            print("获取的验证码：",code)
            if code==cache.get("phone"):
                UserInfo.objects.create_user(**form_obj.cleaned_data,avatar=avatar_img)
                user=auth.authenticate(password=passwd,username=username)
                if user:

                    ret["msg"] = "/userinfo/index/"
                    auth.login(request,user)
                    return JsonResponse(ret)

        else:
            print(form_obj.errors)
            ret["status"] = 1
            ret["msg"] = form_obj.errors
            print(ret)
            print("=" * 120)
            return JsonResponse(ret)

    form_obj=RegForm(request.POST)
    return render(request,"register.html",{"form_obj":form_obj})


def logout(request):
    auth.logout(request)
    return redirect(reverse('userinfo:index'))