在对安卓手机设计自动化测试用例的时候，判断一个测试场景是否可以自动化的依据在于其是否需要人的参与。对于wifi能否自动打开关闭，短信能否自动收发这样的场景，不需要人参与就可以通过程序来判断，因此对Wifi与短信这样的测试，可以通过程序来实现自动化测试。但是另外还有一些测试场景，需要人的眼睛来看，这种场景要实现自动化就比较困难。

## 需求分析
使用安卓的浏览器访问一个网站，如何判断网站已经加载成功？目标网站确实已经收到了请求，也返回了HTML数据，手机也收到了网站返回的数据，但是不知道什么原因，在某些时候，浏览器上面却什么都显示，而浏览器输出的Log却完全看不出异样。对于这样的场景，为了减少人力开销，如何让测试程序自动发现网页没有加载成功，并通知开发者？

这个需求可以使用计算机图像识别来实现自动化。

## 设计思路
由于这个需求只需要判断网页是否加载成功，因此并不需要非常高深的图像识别的理论。对一个网页来说，所谓的加载成功就是指它里面的内容能够正常地在浏览器中显示出来。因此，可以设计一个特别的网页，网页要足够简单，但是又要足够特别，从而方便图像识别。

这篇文章将会使用一个纯绿色的网页来进行测试。网页加载完成以后，手机屏幕上绝大多数的区域是绿色的。这个时候，截取屏幕，并使用程序来识别这张截图。如果发现截图中有大面积的绿色区域，那就证明网页已经加载完成了。

## Demo实现
### 纯绿色的网页

创建一个“greenpage.html”，它的代码如下：
```
<html>
<head>
    <title>Green Page</title>
</head>
<body bgcolor="green">

</body>
</html>
```

网站加载成功以后，页面是全绿色的，如下图所示。
![](http://7sbpmp.com1.z0.glb.clouddn.com/2016-12-04-18-49-20.png)

在局域网中搭建一个Web Server，并让局域网的设备可以链接。打开终端，进入到这个html文件所在的文件夹，并通过Python 3在局域网中搭建一个简单地WebServer：
```shell
cd ~/Project/IdentifyWebpage
python -m http.server
```
使用手机访问“电脑IP:8000/greenpage.html”，效果如下图所示。
![](http://7sbpmp.com1.z0.glb.clouddn.com/2016-12-04-19-01-42.png)

### 识别绿色截图
这个Demo使用Pillow图像处理库来做图像颜色的识别，通过pip安装Pillow：
```
pip install pillow
```
安装完成以后，在Python程序中使用：
```
from PIL import Image
```
导入它图像模块。

程序使用Image模块载入截图，并从截图中读取某一点颜色RGB值：
```
img = Image.open('snapshot.png')
color = img.getpixel((700, 800))
print(color)
```
代码中的（700, 800）是截图中的某一点的座标。第一个参数为横座标，第二个参数为纵座标。截图左上角为(0, 0)，越往下，纵座标越大；越往右，横座标越大。

为了谨慎起见，在截图中取9个点，分别获取他们的RGB值：
```
points = [(200, 300), (455, 678), (333, 1200),
          (300, 500), (888, 678), (900, 800),
          (400, 600), (245, 365), (799, 777)]
img = Image.open('snapshot.png')
for point in self.points:
    color = img.getpixel(point)
    print(color)
```
运行以后的结果如下图所示：
![](http://7sbpmp.com1.z0.glb.clouddn.com/2016-12-04-19-44-55.png)
从图中可以看到，9个点的RGB值全部是(0, 128, 0)，这个值正是绿色的RGB值。到这里，可以认为这个图片大部分的地方确实是绿色的。如果你觉得9个点还是不够全面，那你可以使用代码生成几百个点来计算。

### 获取屏幕截图
adb（Android Debug Bridge）是安卓的调试工具，可以通过adb的命令来控制手机。要对手机截图，只需要使用下面两条命令：
```
adb shell /system/bin/screencap -p /sdcard/screenshot.png
adb pull /sdcard/screenshot.png ~/Project/IndenfyWebpage/screenshot.png
```
第一条命令生成截图，并将截图保存到手机内置存储中。虽然这里写的是“sdcard”，但是对于现在没有SD卡的手机，这条命令依然可以使用。

第二条命令将手机内置存储中的截图文件取出来，并保存到电脑中。如果你的电脑为Windows系统，可以将第二条命令修改为：
```
adb pull /sdcard/screenshot.png D:/Project/IndenfyWebpage/screenshot.png
```
保存到D盘下面。注意这里使用的是从右上到左下的斜杠（/）。

完整的程序请访问-> [https://github.com/kingname/Automatic](https://github.com/kingname/Automatic)

## 更多应用
虽然这个Demo只是针对网页来进行测试。但是这个方法除了网页还可以验证很多其他的测试场景。例如验证视频能否正常播放，做一个特殊的视频，视频中是几个不同的纯色画面不停的切换。每一个画面停留一定的时间，程序定时获取截图并分析此时是否为纯色画面，且纯色画面是否在更换。

理论上讲，任何需要在屏幕上显示信息的测试案例，都可以使用这个方法来实现自动化。

