import os
import json
from notify import send
from login import SZLCSC

notifications = "-----------------------\r\n"
if "OSHW" in os.environ and len(os.environ["OSHW"]) > 1:
    try:
        users = json.loads(os.environ["OSHW"])
        for key in users:
            notifications += "用户" + key[:3] + "******" + key[9:] + "统计情况" + "\r\n"
            my_user = SZLCSC(key, users[key])
            my_user.login("oshwhub")
            if my_user.oshw_login_status:
                notifications += "oshwhub登录成功\r\n"
                if my_user.oshw_signin_status is False:
                    notifications += my_user.perform_oshwhub_signin() + "\r\n"
                else:
                    notifications += "本日已签到\r\n"
                notifications += "当前积分:" + str(my_user.my_integral) + "\r\n"
                notifications += "本周已签天数:" + str(my_user.weekly_days) + "\r\n"
                notifications += "本月已签天数:" + str(my_user.monthly_days) + "\r\n"
                if my_user.seven_day == 1:
                    notifications += "七天奖励:" + my_user.get_seven_day_coupon() + "\r\n"
                else:
                    notifications += "七天奖励: 天数不够\r\n" if my_user.seven_day == 0 else "七天奖励: 已领取\r\n"
                if my_user.month_day == 1:
                    notifications += "月度奖励:" + my_user.get_month_day_coupon() + "\r\n"
                else:
                    notifications += "月度奖励: 天数不够\r\n" if my_user.month_day == 0 else "月度奖励: 已领取\r\n"
            else:
                notifications += "登录失败, 可能用户名密码错误或需要验证, 请自行网页端登录检查\r\n"
            notifications += "-----------------------\r\n"
    except json.decoder.JSONDecodeError:
        notifications += "用户名密码解析失败, 请检查环境变量中 OSHW 的格式\r\n"
# print(notifications)
send("立创签到统计", notifications)
