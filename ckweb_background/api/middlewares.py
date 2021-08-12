from django.utils.deprecation import MiddlewareMixin
import json
from django.http import JsonResponse
from api.models import user_visit
import datetime


class MD1(MiddlewareMixin):
    def process_request(self, request):  # process_request在视图之前执行
        # 获取ip
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]  # 所以这里是真实的ip
        else:
            ip = request.META.get('REMOTE_ADDR')  # 这里获得代理ip

        if request.path_info == '/api/homeImg' or request.path_info == '/api/front' or request.path_info == '/api/video' or request.path_info == '/api/picture' and ip != '127.0.0.1':
            user = user_visit.objects.filter(ip=ip).last()
            if user:

                time = user.time
                now_time = datetime.datetime.now()
                delta = now_time - time
                if not delta < datetime.timedelta(minutes=12 * 60):
                    visit = user_visit(ip=ip)
                    visit.save()
            else:
                visit = user_visit(ip=ip)
                visit.save()


    # process_response在视图之后
    def process_response(self,request, response): #基于请求响应
        return response