闹钟已经成了我们生活中必不可少的东西。如果全球每个国家的当地时间明天早上，所有的闹钟突然都不响了，不知道会发生什么样的混乱。

然而我们要讨论另外一种情况，闹钟每天定时响起来，真的是最好的情况吗？你有过醒来以后等闹钟的经历吗？如果你有时候在闹钟响之前就起来了，那么你会不会希望闹钟能知道你已经起来了？如果你提前醒了，那么闹钟就不响，只有你一直睡着的时候，闹钟才会按时响起来。
<!--more-->

这个项目基于 Andorid 上面的自动化 workflow 程序 Automate 和 Python 制作。总代码量非常小。

做这个东西目的，是因为我现在早上有时候会在 7 点起床写东西，然后再去上班。但有时候可能会直接睡到 7 点 45 ，让闹钟把我闹醒。提前起床可能会忘记关闹钟，但是我不希望在我早上写作的时候被闹钟打扰。

如果我早上提前起床使用电脑，那么 Automate 可以得到信息，并关闭闹钟。如果 Automate 发现我 7 点 45 都还没有碰电脑，就会把我闹醒。整个过程，我不需要和闹钟有任何的交互。

这就是AutoAlarmClock这个项目存在的意义。

## 设计思路

AutoAlarmClock分为三个部分，安卓手机上的Automate，VPS上面的Web Server和Mac OS上面的一行命令。

每天早上7点40，手机上的Automate会访问一个URL A：[http://autoemo.kingname.info:745/alarm_clock](http://autoemo.kingname.info:745/alarm_clock)，只要没有得到返回信息“No”，无论是网络问题，还是因为服务器返回的是其他信息，都会设定一个闹钟，在7点45分响起来。只有访问URL以后，服务器返回“No”，那么就不设闹钟。

对于电脑来说，每天早上7点30分，如果电脑是开着的，说明我正在工作。这个时候电脑就会自动访问一个URL B：[http://autoemo.kingname.info:745/set_alarm](http://autoemo.kingname.info:745/set_alarm).只有这个URL被访问过，之前给Automate访问的URL A才会返回“No”。

## 设计实现

### Web Server
Web Server是手机和电脑之间的桥梁。它是使用Python的Flask框架写成的。代码已经放在了Github上：[AutoAlarmClock](https://github.com/kingname/Automatic.git). 包括空行总共只有32行代码。

```python
from flask import Flask
from datetime import date
import os

app = Flask(__name__)

@app.route('/')
def index():
    return 'please visit my blog at http://kingname.info'

@app.route("/alarm_clock")
def alarm_clock():
    if os.path.exists('alarmclock.txt'):
        with open('alarmclock.txt') as f:
            date_in_txt = f.read()
            today = str(date.today())
            if date_in_txt == today:
                return 'No'
    return 'Yes'

@app.route('/set_alarm')
def set_alarm():
    with open('alarmclock.txt', 'w') as f:
        f.write(str(date.today()))
    return 'OK'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=745)
```

由于这个Web Server每天只访问两次，所以没有必要使用数据库或者做线程安全的设置。数据只需要使用一个文本文件作为中转即可。一旦[http://autoemo.kingname.info:745/set_alarm](http://autoemo.kingname.info:745/set_alarm)这个链接被访问，就会在当前目录创建一个alarmclock.txt文件，里面存放的是今天的日期。当[http://autoemo.kingname.info:745/alarm_clock](http://autoemo.kingname.info:745/alarm_clock)被访问的时候，它会去检查alarmclock.txt，如果这个文件不存在，或者里面的日期不是今天的日期，那么它就会返回“Yes”。只有当alarmclock.txt存在，并且里面的内容为今天的日期，它才会返回“No”。

### 电脑端
电脑只需要访问[http://autoemo.kingname.info:745/set_alarm](http://autoemo.kingname.info:745/set_alarm).由于Mac Book Pro只休眠，不关机，无法使用开机启动的方法来触发这个URL的访问。所以我使用了Crontab这个定时任务。因为在电脑休眠的时候，Crontab的定时任务是不会执行的，只有我在电脑上工作的时候，电脑开着才会访问这个URL，并让它生成记录今天日期的文本文件。

通过下面的命令设定Crontab定时任务，编辑器我选择的是VIM：

```
env EDITOR=vim crontab -e
```

定时任务设定为：
```
30 07 * * * curl -G http://autoemo.kingname.info:745/set_alarm
```

表示每天的7点30分使用curl访问后面的链接。

Crontab在Linux下面也可以正常使用。

如果你的电脑为Windows，因为Windows电脑一般在晚上睡觉时会关机，所以访问URL的工作可以设定开机启动来完成。

首先创建一个EnableAlarmClock.py文件：
```
import requests

requests.get('http://autoemo.kingname.info:745/set_alarm')
```
这个文件用到了Python的requests库，如果你没有的话，请使用pip安装。

再创建一个EnableAlarmClock.bat文件，文件内容如下：
```
python EnableAlarmClock.py
```
打开Windows的 **任务计划** ，触发器选择“当前用户登录时”，操作选择“启动程序”，并填写EnableAlarmClock.bat的路径，如下图所示：

![](http://7sbpmp.com1.z0.glb.clouddn.com/task.png)

这样，每次开机登录桌面的时候，程序自动就会访问设定闹钟的页面了。

### 手机端

Automate是安卓上面的一个强大的自动化工具，类似于IFTTT和iOS上面的Workflow。

在Automate中创建一个Flow，如下图所示：
![](http://7sbpmp.com1.z0.glb.clouddn.com/Screenshot_20161108-074321.png)
其中涉及到了"Time await", "HTTP request", "Expression true?", "Alarm add"这几个组件。

* "Time await"的设置如下图所示：
![](http://7sbpmp.com1.z0.glb.clouddn.com/Screenshot_20161107-224111.png)

* "HTTP request"的设置为下面两张图：
![](http://7sbpmp.com1.z0.glb.clouddn.com/Screenshot_20161107-224136.png)
![](http://7sbpmp.com1.z0.glb.clouddn.com/Screenshot_20161107-224142.png)

* "Alarm add"的设置为下图：
![](http://7sbpmp.com1.z0.glb.clouddn.com/Screenshot_20161107-224155.png)
这里由于没有设置“REPEAT WEEKDAYS”这一项，所以闹钟都是一次性的，关了以后，第二天需要再根据实际情况来让Automate来决定是否需要创建。

设置并启动这个Flow以后，每天早上的闹钟就可以根据你是否在电脑前面工作而决定要不要闹响了。