from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from App.models import AXFUser

REQUIRE_LOGIN = [
    '/axf/addtocart/',
]


class LoginMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # print(request.path)
        if request.path in REQUIRE_LOGIN:

            user_id = request.session.get('user_id')
            if user_id:
                try:
                    user = AXFUser.objects.get(pk=user_id)
                    request.user = user
                except:
                    # return redirect(reverse('axf:login'))
                    data = {
                        'status': 301,
                        'msg': 'user not avaliable'
                    }
                    return JsonResponse(data=data)
            else:
                data = {
                    'status': 301,
                    'msg': 'user not login'
                }
                # return redirect(reverse('axf:login'))
                return JsonResponse(data=data)
