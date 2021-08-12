from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import api.routing
# 第一种设置的方法
from channels.security.websocket import AllowedHostsOriginValidator
application = ProtocolTypeRouter({
    # 普通的HTTP协议在这里不需要写，框架会自己指明
    'websocket': AllowedHostsOriginValidator(
	AuthMiddlewareStack(
    	URLRouter(
        	# 指定去对应应用的routing中去找路由
        	api.routing.websocket_urlpatterns
    		)
		),
	)
})
