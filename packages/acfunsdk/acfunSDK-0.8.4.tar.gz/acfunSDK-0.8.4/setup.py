# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['acfun',
 'acfun.libs',
 'acfun.libs.blackboxprotobuf',
 'acfun.libs.blackboxprotobuf.libs',
 'acfun.libs.blackboxprotobuf.libs.types',
 'acfun.libs.you_get',
 'acfun.libs.you_get.cli_wrapper',
 'acfun.libs.you_get.cli_wrapper.downloader',
 'acfun.libs.you_get.cli_wrapper.openssl',
 'acfun.libs.you_get.cli_wrapper.player',
 'acfun.libs.you_get.cli_wrapper.transcoder',
 'acfun.libs.you_get.extractors',
 'acfun.libs.you_get.processor',
 'acfun.libs.you_get.util',
 'acfun.page',
 'acfun.protos',
 'acfun.protos.Im',
 'acfun.protos.Live']

package_data = \
{'': ['*'],
 'acfun': ['src/README.md',
           'src/README.md',
           'src/generate.bat',
           'src/generate.bat',
           'templates/*',
           'templates/parts/*']}

install_requires = \
['alive-progress>=2.4,<3.0',
 'beautifulsoup4>=4.11,<5.0',
 'cssutils>=2.6,<3.0',
 'filetype>=1.1,<2.0',
 'httpx>=0.23,<0.24',
 'jinja2>=3.1,<4.0',
 'lxml>=4.9,<5.0',
 'proto-plus==1.22.1',
 'protobuf==3.20.1',
 'psutil>=5.9,<6.0',
 'pycryptodome>=3.15,<4.0',
 'rich>=12.5,<13.0',
 'websocket-client>=1.4,<2.0']

setup_kwargs = {
    'name': 'acfunsdk',
    'version': '0.8.4',
    'description': 'acfunSDK - UNOFFICEICAL',
    'long_description': '# acfunSDK - **UNOFFICEICAL**\n\n<br />\n\n<p align="center">\n<a href="https://github.com/dolaCmeo/acfunSDK">\n<img height="100" src="https://s3.dualstack.us-east-2.amazonaws.com/pythondotorg-assets/media/files/python-logo-only.svg" alt="">\n<img height="100" src="https://ali-imgs.acfun.cn/kos/nlav10360/static/common/widget/header/img/acfunlogo.11a9841251f31e1a3316.svg" alt="">\n</a>\n</p>\n\n<br />\n\nacfunSDK是 **非官方的 [AcFun弹幕视频网][acfun.cn]** Python库。\n\n几乎搜集了所有与 [AcFun弹幕视频网][acfun.cn] 相关的接口与数据。\n\nps: _如发现未知接口，或现有功能失效，请随时提交 [Issue]_\n\n- - -\n\n**Python** : 开发环境为 `Python 3.8.10` & `Python 3.9.6`\n\n`Python`本体请自行[下载安装][python]。\n\n## [从PyPI安装](https://pypi.org/project/acfunsdk/)\n\n```shell\npython -m pip install acfunsdk\n```\n\n**需要`ffmpeg`**  主要用于下载视频。\n> 建议去官网下载 https://ffmpeg.org/download.html\n>\n> 可执行文件 `ffmpeg` 需要加入到环境变量，或复制到运行根目录。\n\n- - -\n\n## 使用方法\n\n\n### 实例化获取对象\n```python\nfrom acfun import Acer\n# 实例化一个Acer\nacer = Acer(debug=True)\n# 登录用户(成功登录后会自动保存 \'<用户名>.cookies\')\n# 请注意保存，防止被盗\nacer.login(username=\'you@email.com\', password=\'balalabalala\')\n# 读取用户(读取成功登录后保存的 \'<用户名>.cookies\')\nacer.loading(username=\'13800138000\')\n# 每日签到，领香蕉🍌\nacer.signin()\n# 通过链接直接获取内容对象\n# 目前支持 9种类型：\n# 视  频: https://www.acfun.cn/v/ac4741185\ndemo_video = acer.get("https://www.acfun.cn/v/ac4741185")\nprint(demo_video)\n# 文  章: https://www.acfun.cn/a/ac16695813\ndemo_article = acer.get("https://www.acfun.cn/a/ac16695813")\nprint(demo_article)\n# 合  集: https://www.acfun.cn/a/aa6001205\ndemo_album = acer.get("https://www.acfun.cn/a/aa6001205")\nprint(demo_album)\n# 番  剧: https://www.acfun.cn/bangumi/aa5023295\ndemo_bangumi = acer.get("https://www.acfun.cn/bangumi/aa5023295")\nprint(demo_bangumi)\n# 个人页: https://www.acfun.cn/u/39088\ndemo_up = acer.get("https://www.acfun.cn/u/39088")\nprint(demo_up)\n# 动  态: https://www.acfun.cn/moment/am2797962\ndemo_moment = acer.get("https://www.acfun.cn/moment/am2797962")\nprint(demo_moment)\n# 直  播: https://live.acfun.cn/live/378269\ndemo_live = acer.get("https://live.acfun.cn/live/378269")\nprint(demo_live)\n# 分  享: https://m.acfun.cn/v/?ac=37086357\ndemo_share = acer.get("https://m.acfun.cn/v/?ac=37086357")\nprint(demo_share)\n```\n\n- - -\n\n<details>\n<summary>DEMOs</summary>\n\n**以下DEMO列举了主要的使用方法，具体请自行研究。**\n\n## 👤 主要对象\n\n+ 主对象acer示例 [acer_demo.py][acer] \n\n## 📖 综合页面对象\n\n+ 首页对象示例 [index_reader.py][index] \n+ 频道对象示例 [channel_reader.py][channel] \n+ 搜索对象示例 [search_reader.py][search] \n\n## 🔗 内容页面对象\n\n+ 番剧对象 [bangumi_demo.py][bangumi]\n+ 视频对象 [video_demo.py][video]\n+ 文章对象 [article_demo.py][article]\n+ 合集对象 [album_demo.py][album]\n+ UP主对象 [member_demo.py][member]\n+ 动态对象 [moment_demo.py][moment]\n+ 直播对象 [live_demo.py][live]\n\n## 🎁 附赠: AcSaver\n\n+ 离线保存 [AcSaver_demo.py][saver] \n\n</details>\n\n<details>\n<summary>AcSaver</summary>\n\n> 这是一个依赖acfunSDK的小工具，也算是DEMO。\n> \n> 主要用于离线收藏保存A站的各种资源。\n> 保存后，可使用浏览器打开对应页面。\n\n\n初始化本地路径\n```python\nsaver_path = r"D:\\AcSaver"\n\n# 实例化AcSaver父类\nacsaver = acer.AcSaver(saver_path)\n# 实例化后 会在路径下生成 index.html\n\n# github下载静态文件\n# https://github.com/dolaCmeo/acfunSDK/tree/assets\nacsaver.download_assets_from_github()\n\n# 下载所有Ac表情资源\nacsaver.save_emot()\n```\n\n保存文章\n```python\ndemo_article = acer.get("https://www.acfun.cn/a/ac32633020")\ndemo_article.saver(saver_path).save_all()\n```\n\n保存视频\n```python\ndemo_video = acer.get("https://www.acfun.cn/v/ac4741185")\ndemo_video.saver(saver_path).save_all()\n```\n\n~~保存番剧(暂未支持)~~\n```python\n\n```\n\n~~录制直播(暂未支持)~~\n```python\n\n```\n\n</details>\n\n<details>\n<summary>依赖库</summary>\n\n>内置+修改: 位于 `libs` 文件夹内\n>\n>+ [`you-get`](https://github.com/soimort/you-get)\n>+ [`ffmpeg_progress_yield`](https://github.com/slhck/ffmpeg-progress-yield)\n>+ [`blackboxprotobuf`](https://pypi.org/project/blackboxprotobuf/)\n\n**依赖: 包含在 `requirements.txt` 中**\n\n基础网络请求及页面解析:\n+ [`httpx`](https://pypi.org/project/httpx/)\n+ [`lxml`](https://pypi.org/project/lxml/)\n+ [`beautifulsoup4`](https://pypi.org/project/beautifulsoup4/)\n+ [`cssutils`](https://pypi.org/project/cssutils/)\n\n下载及html页面渲染:\n+ [`alive-progress`](https://pypi.org/project/alive-progress/)\n+ [`filetype`](https://pypi.org/project/filetype/)\n+ [`jinja2`](https://pypi.org/project/jinja2/)\n\nWebSocket通信及数据处理:\n+ [`websocket-client`](https://pypi.org/project/websocket-client/)\n+ [`pycryptodome`](https://pypi.org/project/pycryptodome/)\n+ [`protobuf`](https://pypi.org/project/protobuf/)\n+ [`proto-plus`](https://pypi.org/project/proto-plus/)\n+ [`rich`](https://pypi.org/project/rich/)\n+ [`psutil`](https://pypi.org/project/psutil/)\n\n</details>\n\n- - - \n## 参考 & 鸣谢\n\n+ [AcFun 助手](https://github.com/niuchaobo/acfun-helper) 是一个适用于 AcFun（ acfun.cn ） 的浏览器插件。\n+ [AcFunDanmaku](https://github.com/wpscott/AcFunDanmaku) 是用C# 和 .Net 6编写的AcFun直播弹幕工具。\n+ [实现自己的AcFun直播弹幕姬](https://www.acfun.cn/a/ac16695813) [@財布士醬](https://www.acfun.cn/u/311509)\n+ QQ频道“AcFun开源⑨课”\n+ 使用 [Poetry](https://python-poetry.org/) 构建\n\n- - - \n\n## About Me\n\n[![ac彩娘-阿部高和](https://tx-free-imgs2.acfun.cn/kimg/bs2/zt-image-host/ChQwODliOGVhYzRjMTBmOGM0ZWY1ZRCIzNcv.gif)][dolacfun]\n♂ 整点大香蕉🍌\n<img alt="AcFunCard" align="right" src="https://discovery.sunness.dev/39088">\n\n- - - \n\n[dolacfun]: https://www.acfun.cn/u/39088\n\n[acfun.cn]: https://www.acfun.cn/\n[Issue]: https://github.com/dolaCmeo/acfunSDK/issues\n[python]: https://www.python.org/downloads/\n[venv]: https://docs.python.org/zh-cn/3.8/library/venv.html\n\n[acer]: https://github.com/dolaCmeo/acfunSDK/blob/main/examples/acer_demo.py\n[index]: https://github.com/dolaCmeo/acfunSDK/blob/main/examples/index_reader.py\n[channel]: https://github.com/dolaCmeo/acfunSDK/blob/main/examples/channel_reader.py\n[search]: https://github.com/dolaCmeo/acfunSDK/blob/main/examples/seach_reader.py\n\n[bangumi]: https://github.com/dolaCmeo/acfunSDK/blob/main/examples/bangumi_demo.py\n[video]: https://github.com/dolaCmeo/acfunSDK/blob/main/examples/video_demo.py\n[article]: https://github.com/dolaCmeo/acfunSDK/blob/main/examples/article_demo.py\n[album]: https://github.com/dolaCmeo/acfunSDK/blob/main/examples/album_demo.py\n[member]: https://github.com/dolaCmeo/acfunSDK/blob/main/examples/member_demo.py\n[moment]: https://github.com/dolaCmeo/acfunSDK/blob/main/examples/moment_demo.py\n[live]: https://github.com/dolaCmeo/acfunSDK/blob/main/examples/live_demo.py\n\n[saver]: https://github.com/dolaCmeo/acfunSDK/blob/main/examples/AcSaver_demo.py\n',
    'author': 'dolacmeo',
    'author_email': 'dolacmeo@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://pypi.org/project/acfunsdk/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
