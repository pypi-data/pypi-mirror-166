import requests
import re


def auth(auth_url, username, password):
    """
    A simple cross-auth for Tsinghua ID.
    @params:
        auth_url: URL which will be redirected to Tsinghua auth page.
        username: the username of Tsinghua ID
        password: the password of Tsinghua ID
    @return:
        a dict of cookies after authentication
    """
    s = requests.Session()
    s.get(auth_url, allow_redirects=True)  # Tsinghua id system
    res = s.post("https://id.tsinghua.edu.cn/do/off/ui/auth/login/check", data={
        "i_user": username,
        "i_pass": password,
        "i_captcha": "",
    })
    redirect_url = re.findall(r'<a href="([\s\S]+?)">直接跳转', res.text)[0]
    s.get(redirect_url, allow_redirects=True)
    return s.cookies.get_dict()
