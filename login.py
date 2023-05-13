import hashlib
import json
import re
import requests
from bs4 import BeautifulSoup


def para_checker(_no, _para_list):
    r"""子站检查

    """

    def wrapper(func):
        def decorate(*args, **kw):
            if len(args) == 1:
                raise ValueError("未设置欲登录子站参数!")
            if args[_no] not in _para_list:
                raise ValueError("尚未实现 " + args[_no] + " 的登录, 请检查!")
            else:
                return func(*args, **kw)

        return decorate

    return wrapper


class SZLCSC:
    def __init__(self, phone, password) -> None:
        r"""通过手机号和密码登录立创任意CAS子站.
        :param phone: 登录手机号.
        :param password: 登录密码.
        """
        self.phone = phone
        self.password = password
        self.session = requests.session()
        self.oshw_login_status = False
        self.oshw_signin_status = False
        self.seven_day = 0  # 0-天数不足;1-可领取;2-已领取
        self.month_day = 0
        self.seven_day_uuid = ""
        self.seven_day_couponuuid = ""
        self.month_day_data_uuid = ""
        self.my_integral = 0
        self.weekly_days = 0
        self.monthly_days = 0

    @para_checker(1, ['oshwhub', 'szlcsc'])
    def login(self, login_site) -> requests.Session:
        r"""通过手机号和密码登录立创任意CAS子站.
        :param login_site: 欲登录目标子站, oshwhub, szlcsc...
        :rtype: 返回登录会话
        """
        passport2oshwhub = 'https://passport.szlcsc.com/login?service=https%3A%2F%2Foshwhub.com%2Flogin%3Ff%3Doshwhub'
        passport2szlcsc = 'https://www.szlcsc.com/member/login.html'

        self.session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ('
                                                   'KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
                                     # 'X-forwarded-for': '114.114.114.114'
                                     })
        passport_url = 'https://passport.szlcsc.com/login'

        # 刷新页面获取一次性LT和execution
        r = self.session.get(passport_url)

        login_payload = {
            'lt': re.findall(r'<input type="hidden" name="lt" value="(.*?)" />', r.text)[0],
            'execution': re.findall(r'<input type="hidden" name="execution" value="(.*?)" />', r.text)[0],
            '_eventId': 'submit',
            'loginUrl': 'https%3A%2F%2Fpassport.szlcsc.com%2Flogin',
            'scene': 'login',
            'loginFromType': 'shop',
            'showCheckCodeVal': 'false',
            'username': self.phone,
            'password': hashlib.md5(self.password.encode('utf-8')).hexdigest(),
            'rememberPwd': 'yes'}
        self.session.headers.update({'referer': 'https://passport.szlcsc.com/login'})
        r = self.session.post(passport_url, data=login_payload)
        # print(r.status_code)

        if r.status_code == 200 and login_site == 'szlcsc':
            print('passport登录成功')
            self.session.headers.update({'referer': 'https://passport.szlcsc.com/login', 'Host': 'www.szlcsc.com'})
            r = self.session.get(passport2szlcsc, allow_redirects=False)

            self.session.headers.update({'referer': 'https://passport.szlcsc.com/login', 'Host': 'www.szlcsc.com'})
            r = self.session.get(r.headers['Location'], allow_redirects=False)

            self.session.headers.update({'referer': 'https://passport.szlcsc.com/login', 'Host': 'member.szlcsc.com'})
            r = self.session.get(r.headers['Location'], allow_redirects=False)

            self.session.headers.update({'referer': 'https://passport.szlcsc.com/login', 'Host': 'passport.szlcsc.com'})
            r = self.session.get(r.headers['Location'], allow_redirects=False)

            self.session.headers.update({'referer': 'https://passport.szlcsc.com/login', 'Host': 'member.szlcsc.com'})
            r = self.session.get(r.headers['Location'], allow_redirects=False)

            self.session.headers.update({'referer': 'https://passport.szlcsc.com/login', 'Host': 'member.szlcsc.com'})
            r = self.session.get(r.headers['Location'], allow_redirects=False)

            self.session.headers.update({'referer': 'https://passport.szlcsc.com/login', 'Host': 'passport.szlcsc.com'})
            self.session.get(r.headers['Location'], allow_redirects=False)

            # 跳转szlcsc.com
            self.session.headers.update({'referer': 'https://passport.szlcsc.com/login', 'Host': 'www.szlcsc.com'})
            self.session.get('https://www.szlcsc.com/member/login.html', allow_redirects=False)

            self.session.headers.update({'referer': 'https://www.szlcsc.com/index.html', 'Host': 'member.szlcsc.com'})
            r = self.session.get('https://member.szlcsc.com/member/hiddenAutoLogin.html', allow_redirects=False)
            # print(r.content)
            return self.session

        if r.status_code == 200 and login_site == 'oshwhub':
            try:

                # self.session.headers.update({'referer': 'passport.szlcsc.com', 'Host': 'passport.szlcsc.com'})
                r = self.session.get(passport2oshwhub, allow_redirects=False)

                # self.session.headers.update({'referer': 'passport.szlcsc.com', 'Host': 'oshwhub.com'})
                r = self.session.get(r.headers['Location'], allow_redirects=False)

                # self.session.headers.update({'Host': 'oshwhub.com'})
                r = self.session.get(r.headers['Location'], allow_redirects=False)

                r = self.session.get(r.headers['Location'], allow_redirects=False)
                self.oshw_login_status = True

                self.get_status()
                return self.session
            except KeyError:
                self.oshw_login_status = False
                # print("oshwhub登录失败, 可能用户名密码错误或需要验证, 请自行网页端登录检查")

    def perform_oshwhub_signin(self) -> str:
        r"""执行oshw签到
                """
        if not self.oshw_login_status:
            # print("请先登录")
            return "未登录"
        r = self.session.post("https://oshwhub.com/api/user/sign_in")
        self.get_status()
        return json.loads(r.text)['message']

    def get_status(self) -> None:
        r"""获取账户状态
                        """
        if not self.oshw_login_status:
            print("请先登录")
            return

        # 奖励可领取状态
        soup = BeautifulSoup(self.session.get("https://oshwhub.com/sign_in").text, "html.parser")
        for div in soup.find_all("div", attrs={'class': "reward-way"}):
            self.seven_day = int(div.contents[1].attrs["data-status"])
            self.month_day = int(div.contents[3].attrs["data-status"])
            # print(div.contents[1].attrs["data-status"])
            # print(div.contents[3].attrs["data-status"])

        # 当前积分, 本周已签, 本月已签
        for span in soup.find_all("span", attrs={'class': "specific-integral"}):
            self.my_integral = int(span.get_text())
        for span in soup.find_all("span", attrs={'class': "sign-in-days sign-week"}):
            self.weekly_days = int(span.get_text())
        for span in soup.find_all("span", attrs={'class': "sign-in-days sign-month"}):
            self.monthly_days = int(span.get_text())
        seven_r = self.session.get("https://oshwhub.com/api/user/sign_in/getUnbrokenGiftInfo")
        self.seven_day_uuid = json.loads(seven_r.text)["result"]["sevenDay"]["uuid"]
        self.seven_day_couponuuid = json.loads(seven_r.text)["result"]["sevenDay"]["coupon_uuid"]
        month_r = self.session.get("https://oshwhub.com/api/user/sign_in/getMonthGiftInfo")
        self.month_day_data_uuid = json.loads(month_r.text)["result"]["uuid"]
        # print(self.seven_day_uuid, self.seven_day_couponuuid, self.month_day_data_uuid)

        # 本日已签
        for tag in soup.find_all("button", attrs={'class': "btn btn-secondary"}):
            if "签到" not in tag.get_text():
                continue
            if tag.get_text() == "已签到":
                self.oshw_signin_status = True
            else:
                self.oshw_signin_status = False

    def get_seven_day_coupon(self) -> str:
        r"""执行七天奖励领取
                        """
        if not self.oshw_login_status:
            print("请先登录")
            return "未登录"
        payload = {
            "gift_uuid": self.seven_day_uuid,
            "coupon_uuid": self.seven_day_couponuuid
        }
        r = self.session.post("https://oshwhub.com/api/user/sign_in/getSevenDayGift", data=payload)
        return json.loads(r.text)["message"]

    def get_month_day_coupon(self) -> str:
        r"""执行月度奖励领取
                        """
        if not self.oshw_login_status:
            print("请先登录")
            return "未登录"
        payload = {
            "gift_uuid": self.month_day_data_uuid,
        }
        r = self.session.post("https://oshwhub.com/api/user/sign_in/getMonthGift", data=payload)
        return json.loads(r.text)["message"]
