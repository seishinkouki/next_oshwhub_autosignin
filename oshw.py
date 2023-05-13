import os
import json
from notify import send

if "OSHW" in os.environ and len(os.environ["OSHW"]) > 1:
    try:
        users = json.loads(os.environ["OSHW"])
        for key in users:
            print(key + ":" + users[key])
    except json.decoder.JSONDecodeError:
        print('用户名密码解析失败, 请检查环境变量中 OSHW 的格式')


send("oshw签到通知", "测试1\r\n测试2\r\n测试3")
