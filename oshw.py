import os
import json

if "OSHW" in os.environ and len(os.environ["OSHW"]) > 1:
    try:
        users = json.loads(os.environ["OSHW"])
        for key in users:
            print(key + ":" + users[key])
    except json.decoder.JSONDecodeError:
        print('用户名密码解析失败, 请检查环境变量中 OSHW 的格式')
