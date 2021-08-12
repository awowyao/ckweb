from django.shortcuts import render
# Create your views here.

from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.http import JsonResponse
from rest_framework.views import APIView
from django.shortcuts import render,HttpResponse
import os
import json
from api.models import *
import datetime
import random
ip_list = []



import hashlib
def Md5(str):
  md5 = hashlib.md5()  # 创建md5对象
  # 此处必须声明encode
  # 若写法为hl.update(str)  报错为： Unicode-objects must be encoded before hashing
  md5.update(str.encode(encoding='utf-8'))
  # 把输入的旧密码装换为md5格式
  result = md5.hexdigest()
  # 返回加密结果
  return result

def result_json(code, msg, data):
  # 创建一个空字典
  result = {"code": code, "msg": msg, "data": data}
  return result




@csrf_exempt
def register(request):
    # print(Userinfo.objects.filter(userName='test2').first().userName)
    # return HttpResponseForbidden()
    # 判断是否为post请求
    if request.method == "POST":
       # 获取请求头数据，请求以json的格式传输
       registerinformation = request.body
       # 将请求头数据转化为json格式
       registerinformationData = json.loads(registerinformation)
       # 获取用户名
       userName = registerinformationData.get('userName')
       # 从数据库中查找是否存在该用户名
       userNameDB = Userinfo.objects.filter(userName=userName)
       # 判断用户名是否存在，若存在，则提示已有该用户，若不存在，则进行密码加密后存储到数据库中

       if userNameDB:
           return HttpResponse(json.dumps(result_json('312', '该用户名已经存在', '')),
                               content_type="application/json,charset=utf-8")
       else:
           # 获取用户密码

           userPwd = registerinformationData.get('userPwd')
           user_img = registerinformationData.get('userimg')
           print(userName, userPwd)
           # 密码加密操作md5，md5加密功能具体看md5加密代码
           userPwdMd5 = Md5(str(userPwd))
           # 将加密后的密码赋值给请求头中的密码参数
           registerinformationData["userPwd"] = userPwdMd5
           # 将json格式数据，类型为dict 存储到数据库中，表明为Userinfo，将注册请求存储到数据库中
           user_img = Userinfo(
               userName=userName,
               userImg= user_img,
               userPwd=userPwdMd5
           )
           user_img.save()

       # Userinfo.objects.create(**registerinformationData)
       return HttpResponse(json.dumps(result_json('201', '注册成功，请登录', '')),
                           content_type="application/json,charset=utf-8")
    else:
       return HttpResponse(json.dumps(result_json('501', '不是post请求', '')),
                           content_type="application/json,charset=utf-8")



'''
    用户验证，当用户首次登录时随机生成一个token
'''
# CBV 视图模式

class AuthView(APIView):
    '''
        在配置了全局认证的情况下，可以使用authentication_classes = [] 表示该视图不进行认证
    '''
    authentication_classes = []
    def post(self, request):
        ret = {'code': 201, 'msg': None}
        # user = request.POST.get('username')
        print(request.body)
        try:

            data = json.loads(request.body)
            # print(data)
            user = data['userName']
            pwd = Md5(str(data['userPwd']))
            print(user, pwd)
            obj = Userinfo.objects.filter(userName=user, userPwd=pwd).first()
            if not obj:
                # raise exceptions.AuthenticationFailed('403-请登录')
                return HttpResponseForbidden(json.dumps({'code': 403 ,'msg': '密码错误'}))

            # 为用户创建token
            zm_list = ['a','b','c','d','e','f','g','h','i','j','k','l','n','m','o','p','q','r','s','t','1','2','3']
            mi = random.sample(zm_list, 5)
            token = Md5(user + ''.join(mi))
            # 存在就更新，不存在就创建
            now_time = datetime.datetime.now()
            UserToken.objects.update_or_create(user=obj, defaults={'token': token, 'time': now_time})
            ret['token'] = token
            ret['userImg'] = obj.userImg if obj.userImg else 'NULL'

        except Exception as e:
            ret['code'] = 401
            ret['msg'] = '传参出错'
            return HttpResponse(json.dumps(ret), status=401)

        return JsonResponse(ret)






# from zhylbwg.util.authenticationSelf import AuthenticationSelf

ORDER_DICT = {
    1:{
        'name':'apple',
        'price':15
    },
    2:{
        'name':'dog',
        'price':100
    }
}

from api.authenticationSelf.AuthenticationSelf import AuthenticationSelf
class OrderView(APIView):
    '''订单相关业务'''
    authentication_classes = [AuthenticationSelf,]    #添加局部认证

    def get(self,request, *args, **kwargs):
        ret = {'code':1000,'msg':None,'data':None}
        try:
            ret['data'] = ORDER_DICT
        except Exception as e:
            pass
        return JsonResponse(ret)


def user_Img(request):
    user_img = usersImg(
        userImg=request.FILES.get('file'),
    )
    user_img.save()

    url = {'url' : 'http://47.106.159.32/'+str(user_img.userImg)}
    return HttpResponse(json.dumps(url))




def Imgnotice(request):
    data = json.loads(request.body)
    IMG = str(data['imgDataList'])
    title = str(data['title'])
    topUrlimg = str(data['topUrlimg'])
    content = str(data['content'])
    Imgnotice = Img_notice(
        topUrlimg=topUrlimg,
        Img=IMG,
        title=title,
        content=content,)
    Imgnotice.save()
    return HttpResponse(status=200)

# 查询全部
class all_data(APIView):
    def get(self,request, *args, **kwargs):
        size = request.GET.get('size')
        page = request.GET.get('page')
        data = Img_notice.objects.all()
        data_nub = len(data)
        cartoon = Paginator(data, int(size))
        data = cartoon.page(int(page))

        d_list = []
        for i in data:
            d_list.append({
                    'time': str(i.time.strftime('%Y-%m-%d %H:%M:%S')),
                    'title': i.title,
                    'id': i.id,
                    'topUrlimg': i.topUrlimg,
                  })

        dic = {'total_count': data_nub , 'dataList': d_list}
        return HttpResponse(json.dumps(dic))

# 查询全部
def notall_data(request):
    size = request.GET.get('size')
    page = request.GET.get('page')
    data = Img_notice.objects.all()
    data_nub = len(data)
    cartoon = Paginator(data, int(size))
    data = cartoon.page(int(page))

    d_list = []
    for i in data:
        d_list.append({
            'time': str(i.time.strftime('%Y-%m-%d %H:%M:%S')),
            'title': i.title,
            'id': i.id,
            'topUrlimg': i.topUrlimg,
        })

    dic = {'total_count': data_nub, 'dataList': d_list}
    return HttpResponse(json.dumps(dic))



# 根据id查询
def check_data(request):
    id = request.GET.get('id')
    if request.method == 'DELETE':
        id_data = json.loads(request.body)
        id = str(id_data['id'])
        data = Img_notice.objects.get(id=id)

        # os.remove('./static/user/1.jpg')
        try:
            for i in eval(data.Img):
                i = i.split('/')[-1]
                usersImg.objects.get(userImg='static/user/{}'.format(i)).delete()
                os.remove('./static/user/{}'.format(i))
        except:
            pass

        data.delete()
        return HttpResponse(status=200)

    elif request.method == 'GET':
        data = Img_notice.objects.get(id=id)
        dic = {
                    'topUrlimg': data.topUrlimg,
                    'time': str(data.time.strftime('%Y-%m-%d %H:%M:%S')),
                    'content': data.content,
                    'imgDataList': eval(data.Img),
                    'title': data.title

        }
        return HttpResponse(json.dumps(dic))
    elif request.method == 'PUT':
        id_data = json.loads(request.body)
        id = str(id_data['id'])
        IMG = str(id_data['imgDataList'])
        title = str(id_data['title'])
        topUrlimg = str(id_data['topUrlimg'])
        content = str(id_data['content'])

        data = Img_notice.objects.get(id=id)
        data.title = title
        data.Img = IMG
        data.topUrlimg = topUrlimg
        data.content = content
        data.save()
        return HttpResponse(status=200)


    else:
        return HttpResponse(status=401)


# 新增视频
def UPvideoNotice(request):

    data = json.loads(request.body)
    IMG = str(data['imgDataList'])

    title = str(data['title'])
    topUrlimg = str(data['topUrlimg'])
    content = str(data['content'])

    Imgnotice = video_notice(
        topUrlimg=topUrlimg,
        video=IMG,
        title=title,
        content=content
    )

    Imgnotice.save()
    return HttpResponse(status=200)



# 分页视频
class video_all_data(APIView):
    def get(self, request, *args, **kwargs):
        size = request.GET.get('size')
        page = request.GET.get('page')
        data = video_notice.objects.all()
        data_nub = len(data)
        cartoon = Paginator(data, int(size))
        data = cartoon.page(int(page))

        d_list = []
        for i in data:
            d_list.append({
                'time': str(i.time.strftime('%Y-%m-%d %H:%M:%S')),
                'title': i.title,
                'id': i.id,
                'topUrlimg': i.topUrlimg,
            })

        dic = {'total_count': data_nub, 'dataList': d_list}
        return HttpResponse(json.dumps(dic))


# 不校验分页视频
def notvideo_all_data(request):
    size = request.GET.get('size')
    page = request.GET.get('page')
    data = video_notice.objects.all()
    data_nub = len(data)
    cartoon = Paginator(data, int(size))
    data = cartoon.page(int(page))

    d_list = []
    for i in data:
        d_list.append({
                'time': str(i.time.strftime('%Y-%m-%d %H:%M:%S')),
                'title': i.title,
                'id': i.id,
                'topUrlimg': i.topUrlimg,
              })

    dic = {'total_count': data_nub , 'dataList': d_list}
    return HttpResponse(json.dumps(dic))

# 根据ip查询视频和删除
def video_check_data(request):
    id = request.GET.get('id')
    if request.method == 'DELETE':
        id_data = json.loads(request.body)
        id = str(id_data['id'])
        data = video_notice.objects.get(id=id)
        data.delete()
        return HttpResponse(status=200)
    elif request.method == 'GET':
        data = video_notice.objects.get(id=id)
        dic = {
                    'topUrlimg': data.topUrlimg,
                    'time': str(data.time.strftime('%Y-%m-%d %H:%M:%S')),
                    'content': data.content,
                    'imgDataList': eval(data.video),
                    'title': data.title

        }
        return HttpResponse(json.dumps(dic))

    elif request.method == 'PUT':
        id_data = json.loads(request.body)
        id = str(id_data['id'])
        IMG = str(id_data['imgDataList'])
        title = str(id_data['title'])
        topUrlimg = str(id_data['topUrlimg'])
        content = str(id_data['content'])

        data = video_notice.objects.get(id=id)
        data.title = title
        data.video = IMG
        data.topUrlimg = topUrlimg
        data.content = content
        data.save()
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=401)




class Home_img(APIView):
    def get(self, request, *args, **kwargs):
        with open('./home_img.txt', 'r') as f:
            data = f.read().split('$%')
            dic = {
                'title': data[0],
                'url': data[1],
            }
            f.close()
        return HttpResponse(json.dumps(dic))

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        title = str(data['title'])
        url = str(data['url'])
        with open('./home_img.txt', 'w') as f:
            f.write(str(title) + '$%' + str(url))
            f.close()
        dic = {
            'title': title,
            'url': url,
        }
        return HttpResponse(json.dumps(dic))


def notHome_img(request):

    if request.method == 'GET':
        with open('./home_img.txt', 'r') as f:
            data = f.read().split('$%')
            dic = {
                'title': data[0],
                'url': data[1],
            }
            f.close()
        return HttpResponse(json.dumps(dic))




class Introduction_img(APIView):
    def get(self,request, *argsm, **kwargs):
        with open('./Introduction.txt', 'r') as f:
            data = f.read().split('$%')
            dic = {
                'title': data[0],
                'url': data[1],
            }
            f.close()
        return HttpResponse(json.dumps(dic))
    def post(self,request, *argsm, **kwargs):
        data = json.loads(request.body)
        title = str(data['title'])
        url = str(data['url'])
        with open('./Introduction.txt', 'w') as f:
            f.write(str(title) + '$%' + str(url))
            f.close()
        dic = {
            'title': title,
            'url': url,
        }
        return HttpResponse(json.dumps(dic))



def notIntroduction_img(request):

    if request.method == 'GET':
        with open('./Introduction.txt', 'r') as f:
            data = f.read().split('$%')
            dic = {
                'title': data[0],
                'url': data[1],
            }
            f.close()
        return HttpResponse(json.dumps(dic))


# 访问量
def userValue(request):
    now_time = datetime.datetime.now()
    end_time = datetime.datetime(2021, 8, 9, 0, 0)
    # print((now_time-end_time).days)
    dic = {"dataList": []}
    for i in range(((now_time - end_time).days), -1, -1):

        day = now_time.date() - datetime.timedelta(days=i)
        visit = user_visit.objects.filter(time__year=int(day.year), time__month=int(day.month), time__day=int(day.day))
        visit_nub = len(visit)
        dic['dataList'].append({"date": day, 'value': visit_nub})

    return JsonResponse(dic)














import re
import os
from wsgiref.util import FileWrapper
from django.http import StreamingHttpResponse
import mimetypes
def file_iterator(file_name, chunk_size=8192, offset=0, length=None):
    with open(file_name, "rb") as f:
        f.seek(offset, os.SEEK_SET)
        remaining = length
        while True:
            bytes_length = chunk_size if remaining is None else min(remaining, chunk_size)
            data = f.read(bytes_length)
            if not data:
                break
            if remaining:
                remaining -= len(data)
            yield data


def stream_video(request):
    """将视频文件以流媒体的方式响应"""
    range_header = request.META.get('HTTP_RANGE', '').strip()
    range_re = re.compile(r'bytes\s*=\s*(\d+)\s*-\s*(\d*)', re.I)
    range_match = range_re.match(range_header)
    path = 'E:\\陈\\[桜都字幕组]2021年02月合集\\CHS\\1.mp4'
    size = os.path.getsize(path)
    content_type, encoding = mimetypes.guess_type(path)
    content_type = content_type or 'application/octet-stream'
    if range_match:
        first_byte, last_byte = range_match.groups()
        first_byte = int(first_byte) if first_byte else 0
        last_byte = first_byte + 1024 * 1024 * 1       # 8M 每片,响应体最大体积
        if last_byte >= size:
            last_byte = size - 1
        length = last_byte - first_byte + 1
        resp = StreamingHttpResponse(file_iterator(path, offset=first_byte, length=length), status=206, content_type=content_type)
        resp['Content-Length'] = str(length)
        resp['Content-Range'] = 'bytes %s-%s/%s' % (first_byte, last_byte, size)
    else:
        # 不是以视频流方式的获取时，以生成器方式返回整个文件，节省内存
        resp = StreamingHttpResponse(FileWrapper(open(path, 'rb')), content_type=content_type)
        resp['Content-Length'] = str(size)
    resp['Accept-Ranges'] = 'bytes'
    return resp
