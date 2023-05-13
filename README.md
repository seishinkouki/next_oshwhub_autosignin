# next_oshwhub_autosignin

实现对立创开源社区的每日签到获取积分, 并自动领取奖励, 支持多账号

# 食用方法
## 青龙面板:
1. 拉库命令:
```ql repo https://github.com/seishinkouki/next_oshwhub_autosignin.git "oshw|login" "" ""```
2. 增加名为```OSHW```的环境变量, 值为```{"手机号1": "密码1",""手机号2": "密码2", "手机号n": "密码n"}```
3. 自行添加定时任务

## 软路由/服务器/电脑 上单独运行

### 本repo需python3.x 环境, 理论上有python环境即可运行, 下载repo, 自行替换```os.environ["OSHW"]```为上面OSHW变量