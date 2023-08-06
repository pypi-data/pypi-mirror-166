# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ayugespidertools', 'ayugespidertools.common']

package_data = \
{'': ['*'], 'ayugespidertools': ['VIT/*', 'doc/*']}

install_requires = \
['DBUtils>=3.0.2,<4.0.0',
 'Pillow>=9.2.0,<10.0.0',
 'PyExecJS>=1.5.1,<2.0.0',
 'PyMySQL>=1.0.2,<2.0.0',
 'SQLAlchemy>=1.4.39,<2.0.0',
 'Scrapy>=2.6.2,<3.0.0',
 'WorkWeixinRobot>=1.0.1,<2.0.0',
 'aiohttp>=3.8.1,<4.0.0',
 'crawlab-sdk>=0.6.0,<0.7.0',
 'environs>=9.5.0,<10.0.0',
 'html2text>=2020.1.16,<2021.0.0',
 'itemadapter>=0.7.0,<0.8.0',
 'loguru>=0.6.0,<0.7.0',
 'numpy>=1.23.1,<2.0.0',
 'opencv-python>=4.6.0,<5.0.0',
 'pandas>=1.4.3,<2.0.0',
 'pymongo==3.11.0',
 'requests>=2.28.1,<3.0.0',
 'retrying>=1.3.3,<2.0.0']

setup_kwargs = {
    'name': 'ayugespidertools',
    'version': '1.0.0',
    'description': '一些爬虫开发中简单的工具集',
    'long_description': '# AyugeSpiderTools 工具说明\n\n> 本文章用于说明在爬虫开发中遇到的各种通用方法，将其打包成 `Pypi` 包以方便安装和使用，此工具会长久维护。\n\n## 前言\n在 `Python` 开发时会遇到一些经常使用的模块，为了更方便地使用这些模块，我们需要将其打包并发布到 `Pypi` 上。\n\n## 项目状态\n\n> 目前项目正处于**积极开发和维护**中\n\n项目创建初期，且包含各阶段时期的代码，会出现代码风格不统一，代码杂乱，文档滞后和测试文件不全的问题，近期会优化此情况。\n\n项目目前暂定主要包含两大部分：\n\n- 开发场景中的工具库\n  - 比如 `MongoDB`，`Mysql sql` 语句的生成，图像处理，数据处理相关 ... ...\n- `Scrapy` 扩展功能\n  - 使爬虫开发无须在意数据库和数据表结构，不用去管常规 `item, pipelines` 和 `middlewares` 的文件的编写\n\n注：具体内容请查看本文中的 [TodoList](# TodoList) 内容\n\n## 1. 前提条件\n\n> `python 3.8+` 可以直接输入以下命令：\n\n```shell\npip install ayugespidertools -i https://pypi.org/simple\n```\n\n> `python 3.8` 以下的版本，请自行安装以下依赖：\n\n```ini\nopencv-python = "^4.6.0"\nnumpy = "^1.23.1"\nPyExecJS = "^1.5.1"\nenvirons = "^9.5.0"\nrequests = "^2.28.1"\nloguru = "^0.6.0"\nPillow = "^9.2.0"\nPyMySQL = "^1.0.2"\nScrapy = "^2.6.2"\npandas = "^1.4.3"\nWorkWeixinRobot = "^1.0.1"\npytest = "^6.2.5"\ncrawlab-sdk\nretrying = "^1.3.3"\n# 这个 pymongo 库必须为 3.11.0 及以下，会有兼容问题，以后优化\npymongo = "3.11.0"\nSQLAlchemy = "^1.4.39"\nDBUtils = "^3.0.2"\nitemadapter = "^0.7.0"\n```\n\n注：`pymongo` 版本要在 `3.11.0` 及以下的要求是因为我的 `MongoDB` 的版本为 `3.4`；若依赖库中的库有版本冲突，请去除版本限制即可。\n\n## 2. 功能介绍\n\n### 2.1. 数据格式化\n\n> 目前此场景下的功能较少，后面会慢慢丰富其功能\n\n#### 2.1.1. get_full_url\n\n根据域名 `domain_name` 拼接 `deal_url` 来获得完整链接，示例如下：\n\n```python\nfull_url = FormatData.get_full_url(domain_name="https://static.geetest.com", deal_url="/captcha_v3/batch/v3/2021-04-27T15/word/4406ba6e71cd478aa31e0dca37601cd4.jpg")\n```\n\n输出为：\n\n```\nhttps://static.geetest.com/captcha_v3/batch/v3/2021-04-27T15/word/4406ba6e71cd478aa31e0dca37601cd4.jpg\n```\n\n#### 2.1.2. click_point_deal\n\n将小数 `decimal` 保留小数点后 `decimal_places` 位，结果四舍五入，示例如下：\n\n```\nres = FormatData.click_point_deal(13.32596516, 3)\n```\n\n输出为：\n\n```\n13.326\n```\n\n#### 2.1.3. normal_to_stamp\n\n将网页中显示的正常时间转为时间戳\n\n```python\nnormal_stamp = FormatData.normal_to_stamp("Fri, 22 Jul 2022 01:43:06 +0800")\nprint("normal_stamp1:", normal_stamp)\n\nnormal_stamp = FormatData.normal_to_stamp("Thu Jul 22 17:59:44 2022")\nprint("normal_stamp2:", normal_stamp)\n\nnormal_stamp = FormatData.normal_to_stamp("2022-06-21 16:40:00")\n\nnormal_stamp = FormatData.normal_to_stamp("2022/06/21 16:40:00")\nprint("normal_stamp4:", normal_stamp)\n\nnormal_stamp = FormatData.normal_to_stamp("2022/06/21", date_is_full=False)\nprint("normal_stamp4_2:", normal_stamp)\n\n# 当是英文的其他格式，或者混合格式时，需要自己自定时间格式化符\nnormal_stamp = FormatData.normal_to_stamp(normal_time="2022/Dec/21 16:40:00", _format_t="%Y/%b/%d %H:%M:%S")\nprint("normal_stamp5:", normal_stamp)\n```\n\n输出为：\n\n```\nnormal_stamp1: 1658425386\nnormal_stamp2: 1658483984\nnormal_stamp3: 1655800800\nnormal_stamp4: 1655800800\nnormal_stamp4_2: 1655740800\nnormal_stamp5: 1671612000\n```\n\n### 2.2. 图片相关操作\n\n#### 2.2.1. 滑块验证码缺口距离识别\n\n通过背景图片和缺口图片识别出滑块距离，示例如下：\n\n```python\n# 参数为图片全路径的情况\ngap_distance = Picture.identify_gap("doc/image/2.jpg", "doc/image/1.png")\nprint("滑块验证码的缺口距离1为：", gap_distance)\nassert gap_distance in list(range(205, 218))\n\n# 参数为图片 bytes 的情况\nwith open("doc/image/1.png", "rb") as f:\ntarget_bytes = f.read()\nwith open("doc/image/2.jpg", "rb") as f:\ntemplate_bytes = f.read()\ngap_distance = Picture.identify_gap(template_bytes, target_bytes, "doc/image/33.png")\nprint("滑块验证码的缺口距离2为：", gap_distance)\n```\n\n结果为：\n\n<img src="http://175.178.210.193:9000/drawingbed/image/image-20220802110652131.png" alt="image-20220802110652131" style="zoom: 25%;" />\n\n<img src="http://175.178.210.193:9000/drawingbed/image/image-20220802110842737.png" alt="image-20220802110842737" style="zoom:33%;" />\n\n#### 2.2.2. 滑块验证轨迹生成\n\n根据滑块缺口的距离生成轨迹数组，目前也不是通用版。\n\n```python\ntracks = VerificationCode.get_normal_track(space=120)\n```\n\n结果为：\n\n```\n生成的轨迹为： [[2, 2, 401], [4, 4, 501], [8, 6, 603], [13, 7, 701], [19, 7, 801], [25, 7, 901], [32, 10, 1001], [40, 12, 1101], [48, 14, 1201], [56, 15, 1301], [65, 18, 1401], [74, 19, 1501], [82, 21, 1601], [90, 21, 1701], [98, 22, 1801], [105, 23, 1901], [111, 25, 2001], [117, 26, 2101], [122, 28, 2201], [126, 30, 2301], [128, 27, 2401], [130, 27, 2502], [131, 30, 2601], [131, 28, 2701], [120, 30, 2802]]\n```\n\n### 2.3. Mysql 相关\n\n`sql` 语句简单场景生成，目前是残废版，只适用于简单场景。\n\n更多复杂的场景请查看 [directsql](https://pypi.org/project/directsql/#history), [python-sql](https://pypi.org/project/python-sql/#history),  [pypika](https://pypi.org/project/PyPika/#description) 或 [pymilk](https://pypi.org/project/pymilk/) 的第三方库实现，以后会升级本库的方法。\n\n```python\n# mysql 连接\nmysql_client = MysqlClient.MysqlOrm(NormalConfig.PYMYSQL_CONFIG)\n\n# test_select_data\nsql_pre, sql_after = SqlFormat.select_generate(db_table="newporj", key=["id", "title"], rule={"id|<=": 5}, order_by="id")\nstatus, res = mysql_client.search_data(sql_pre, sql_after, type="one")\n\n# test_insert_data\ninsert_sql, insert_value = SqlFormat.insert_generate(db_table="user", data={"name": "zhangsan", "age": 18})\nmysql_client.insert_data(insert_sql, insert_value)\n\n# test_update_data\nupdate_sql, update_value = SqlFormat.update_generate(db_table="user", data={"score": 4}, rule={"name": "zhangsan"})\nmysql_client.update_data(update_sql, update_value)\n```\n\n### 2.4. 自动化相关\n\n目前是残废阶段，以后放上一些自动化相关操作\n\n### 2.5. 执行 js 相关\n\n鸡肋封装，以后会优化和添加多个常用功能\n\n```python\n# 测试运行 js 文件中的方法\njs_res = RunJs.exec_js("doc/js/add.js", "add", 1, 2)\nprint("test_exec_js:", js_res)\nassert js_res\n\n# 测试运行 ctx 句柄中的方法\nwith open(\'doc/js/add.js\', \'r\', encoding=\'utf-8\') as f:\n    js_content = f.read()\nctx = execjs.compile(js_content)\n\njs_res = RunJs.exec_js(ctx, "add", 1, 2)\nprint("test_exec_js_by_file:", js_res)\nassert js_res\n```\n\n## 3. Scrapy 扩展功能\n\n> 此功能单开一个章节，此扩展使爬虫开发不用考虑 `Scrapy` 的 `item` 文件，内置通用的 `middlewares` 中间件方法（随机请求头，动态/独享代理等），和常用的`pipelines` 方法（`Mysql`，`MongoDB` 存储，`Kafka`，`RabbitMQ` 推送队列等）。开发人员只需配置并激活相关配置即可，可以专注于爬虫 `spider` 的开发。\n\n这里的内容也比较多，请移步到 `Github` 上的 [DemoSpdier](https://github.com/shengchenyang/DemoSpider) 项目中查看。\n\n## 4. 总结\n\n项目目前是疯狂开发阶段，会慢慢丰富 `python` 开发中的遇到的通用方法。\n\n## TodoList\n\n- [x] 添加常用的图片验证码中的图片处理方法\n  - [x] 滑块缺口距离的识别方法\n  - [x] 根据滑块距离生成轨迹数组的方法\n  - [x] 识别点选验证码位置及点击顺序，识别结果不太好，待优化\n  - [ ] ... ...\n- [x] `scrapy` 的扩展功能开发（会优先更新此功能）\n  - [ ] `scrapy` 结合 `crawlab` 的日志统计功能\n  - [x] `scrapy` 脚本运行信息统计和项目依赖表采集量统计，可用于日志记录和预警\n  - [ ] 自定义模板，在 `scrapy startproject` 和 `scrapy genspider` 时生成适合本库的模板文件\n  - [x] ~~增加根据 `nacos` 来获取配置的功能~~ -> 改为增加根据 `consul` 来获取配置的功能\n  - [x] 代理中间件（独享代理、动态隧道代理）\n  - [x] 随机请求头 `UA` 中间件，根据 `fake_useragent` 中的权重来随机\n  - [x] 使用以下工具来替换 `scrapy` 的发送请求\n    - [ ] `selenum`: 性能没有 pyppeteer 强\n    - [x] `pyppeteer`: Gerapy-pyppeteer 库已经实现此功能\n    - [x] `requests`: 这个不推荐使用，requests 同步库会降低 scrapy 运行效率\n    - [ ] `splash`\n    - [x] `aiohttp`: 集成将 `scrapy Request` 替换为 `aiohttp` 的协程方式\n  - [x] `Mysql` 存储的场景下适配\n    - [x] 自动创建 `Mysql` 用户场景下需要的数据库和数据表及字段格式，还有字段注释\n  - [x] `MongoDB` 存储的场景下适配\n  - [ ] 集成 `Kafka`，`RabbitMQ` 等数据推送功能\n  - [ ] ... ...\n- [x] 常用的数据处理相关\n  - [x] `sql` 语句拼接，只是简单场景，后续优化。已给出优化方向，参考库等信息。\n  - [x] `mongoDB` 语句拼接\n  - [ ] 数据格式化处理，比如：去除网页标签，去除无效空格等\n  - [ ] ... ...\n\n',
    'author': 'ayuge',
    'author_email': 'ayuge.s@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://175.178.210.193:8090/mkdocs-material/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
