# 电影信息采集分析系统的设计与实现
- [背景](#背景)
- [配置](#配置)
- [安装](#安装)
- [运行](#运行)
- [证书](#证书)

## 背景
&ensp; &ensp; 随着经济全球化进程的不断推进以及电影技术革新、拍摄技术迭代，国内外电影的种类和数量持续增长。虽然这些海量的电影资源为用户提供了丰富的体验，但与此同时由于电影的相关数据种类繁多数据量大，对于用户来说想要寻找感兴趣的电影并对其深入了解需要花费更多的时间，基于此设计了一个电影信息采集分析系统。

&ensp; &ensp; 本系统首先应用爬虫技术采集电影网站的相关数据，在对这些数据进行一系列处理后存入数据库中，从而为后续的分析提供数据支撑。其次对影评数据进行关键词提取，以提取结果为基础通过余弦相似度来计算与之相似的电影从而帮助用户推荐电影。本系统的主要功能包括电影数据采集、影评关键词提取、电影推荐以及数据可视化。通过电影搜索、电影分类、电影榜单、地区偏好来查看电影及其影评用户分析和影评分析，从而帮助用户更加深入地了解电影。

&ensp; &ensp; 根据本系统的分析结果，用户不但能够在较短时间内了解一部电影，而且还能更快地挑选出感兴趣的电影，具有一定的工程实用价值。
## 配置
- [Python](https://www.python.org/) 版本:3.10.4 (tags/v3.10.4:9d38120, Mar 23 2022, 23:13:41) [MSC v.1929 64 bit (AMD64)] on win32
    - 所用的库: json、math、hashlib、datetime、queue、collections、time、random、threading、[jwt](https://jwt.io/)==2.3.0、black==22.3.0、flask==2.1.1、jieba==0.42.1、lxml==4.8.0、pymysql==1.0.2、requests==2.27.1、selenium==4.1.3
- JavaScript
    - 所用的库:[ECharts](https://echarts.apache.org/zh/index.html) 5.2.1、[jQuery](https://jquery.com/) 3.5.1、[wordcloud2.js](https://github.com/timdream/wordcloud2.js) 1.2.2
- HTML
- CSS
    - 所用的库: [animate.css](https://animate.style/)
- 前端开发框架:[Bootstrap 4.6](https://v4.bootcss.com/)
- WEB应用框架:[Flask](https://flask.net.cn/) 2.1.1
- 数据库:[MySQL](https://www.mysql.com/) 8.0.28
- 浏览器:[谷歌浏览器](https://www.google.cn/intl/zh-CN/chrome/) 101.0.4951.64 (正式版本) (64位)
- 谷歌浏览器驱动:[chromedriver](http://chromedriver.storage.googleapis.com/index.html) 100.0.4896.60

[film_system.sql](https://github.com/Eterniter/film_system-me/blob/main/film_system.sql)至少保存了[豆瓣电影 Top 250](https://movie.douban.com/top250)的电影信息、对应电影100条影评数据以及对应影评用户信息。可以在后台管理中根据豆瓣URL添加电影。

## 安装

1. 安装[配置](#配置)。
2. 运行[film_system.sql](https://github.com/Eterniter/film_system-me/blob/main/film_system.sql)创建数据库。
3. 在[mysql_query.py](https://github.com/Eterniter/film_system-me/blob/main/mysql_query.py)文件中配置好连接数据库的信息。
4. 运行[app.py](https://github.com/Eterniter/film_system-me/blob/main/app.py)文件
5. 如果开启了爬虫，第一次运行需要微信扫码登录获取[Cookie](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Cookies)，务必确保谷歌浏览器版本与[chromedriver](http://chromedriver.storage.googleapis.com/index.html)版本适配。
## 运行
[演示视频](https://www.bilibili.com/video/BV1Hg411R76w?spm_id_from=333.999.0.0)
## 证书
[MIT](LICENSE)
