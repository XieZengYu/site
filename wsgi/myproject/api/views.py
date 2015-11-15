from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse

import requests
from pyquery import PyQuery


class Login(View):
    """
    登陆用户, 返回 cookie 作为 token,
    之后的操作都需要此 token 作为参数,
    用 token 这个词比较像是真正的 api.
    post 数据为 ::
        {
            'username': username,
            'password': password
        }

    成功登陆返回 token
    失败返回空字符串
    错误返回错误信息
    """

    def post(self, req):
        username = req.POST.get('username')
        password = req.POST.get('password')
        token = ''

        if username and password:
            try:
                session = requests.Session()

                # 登陆 lib.gdei.edu.cn
                session.post(
                    'http://lib.gdei.edu.cn/chklogin.jsp',
                    data={
                        'accno': username,
                        'password': password
                    }
                )

                # 不管成功与否, 请求认证
                # 登陆后点 我的借阅信息 可以发现这个 url
                ret = session.get('http://lib.gdei.edu.cn/opac.jsp')
                if ret.ok:
                    q = PyQuery(ret.text)
                    auth_url = q('iframe[name="ssopac"]').attr('src')
                    session.get(auth_url)
                    token = session.cookies.get('sulcmiswebpac')
            except Exception as e:
                return JsonResponse({'error': str(e)})

        return JsonResponse({'token': token})
