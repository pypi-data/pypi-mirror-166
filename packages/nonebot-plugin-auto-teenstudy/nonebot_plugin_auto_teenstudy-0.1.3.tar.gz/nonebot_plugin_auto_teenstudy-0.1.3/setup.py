# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_auto_teenstudy',
 'nonebot_plugin_auto_teenstudy.resource.crawl']

package_data = \
{'': ['*'],
 'nonebot_plugin_auto_teenstudy': ['data/*',
                                   'resource/*',
                                   'resource/dxx_bg/*',
                                   'resource/endpic/*',
                                   'resource/font/*',
                                   'resource/images/*',
                                   'resource/own_bg_hb/*']}

install_requires = \
['Pillow',
 'anti_useragent>=1.0.7,<1.1.0',
 'beautifulsoup4>=4.10.0,<4.11.0',
 'httpx>=0.20.0,<0.21.0',
 'nonebot-adapter-onebot>=2.0.0b1,<3.0.0',
 'nonebot2>=2.0.0b2']

setup_kwargs = {
    'name': 'nonebot-plugin-auto-teenstudy',
    'version': '0.1.3',
    'description': '基于nonebot异步框架的青年大学自动提交插件',
    'long_description': '<div align="center">\n    <img src="https://s4.ax1x.com/2022/03/05/bw2k9A.png" alt="bw2k9A.png" border="0"/>\n    <h1>nonebot_plugin_auto_teenstudy</h1>\n    <b>基于nonebot2的青年大学习自动提交插件，用于自动完成大学习，在后台留下记录，返回完成截图</b>\n    <br/>\n    <a href="https://github.com/ZM25XC/nonebot_plugin_auto_teenstudy/issues"><img alt="GitHub issues" src="https://img.shields.io/github/issues/ZM25XC/nonebot_plugin_auto_teenstudy?style=flat-square"></a>\n    <a href="https://github.com/ZM25XC/nonebot_plugin_auto_teenstudy/network"><img alt="GitHub forks" src="https://img.shields.io/github/forks/ZM25XC/nonebot_plugin_auto_teenstudy?style=flat-square"></a>\n    <a href="https://github.com/ZM25XC/nonebot_plugin_auto_teenstudy/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/ZM25XC/nonebot_plugin_auto_teenstudy?style=flat-square"></a>\n    <a href="https://github.com/ZM25XC/nonebot_plugin_auto_teenstudy/blob/main/LICENSE"><img alt="GitHub license" src="https://img.shields.io/github/license/ZM25XC/nonebot_plugin_auto_teenstudy?style=flat-square"></a>\n</div>\n\n\n## 各地区使用方式（已经支持地区）\n\n- [江西地区](./nonebot_plugin_auto_teenstudy/resource/江西地区.md)\n- [湖北地区](./nonebot_plugin_auto_teenstudy/resource/湖北地区.md)\n- [浙江地区](./nonebot_plugin_auto_teenstudy/resource/浙江地区.md)\n- [安徽地区](./nonebot_plugin_auto_teenstudy/resource/安徽地区.md)\n- [山东地区](./nonebot_plugin_auto_teenstudy/resource/山东地区.md)\n- [四川地区](./nonebot_plugin_auto_teenstudy/resource/四川地区.md)\n\n\n**其他地区努力适配中**\n\n## 参考\n\n- [江西共青团自动提交](https://github.com/XYZliang/JiangxiYouthStudyMaker)\n\n- [青春湖北自动提交](https://github.com/Samueli924/TeenStudy)\n\n- [28位openid随机生成和抓包](https://hellomango.gitee.io/mangoblog/2021/09/26/other/%E9%9D%92%E5%B9%B4%E5%A4%A7%E5%AD%A6%E4%B9%A0%E6%8A%93%E5%8C%85/)\n- [定时推送大学习答案，完成截图](https://github.com/ayanamiblhx/nonebot_plugin_youthstudy)\n##  安装及更新\n\n1. 使用`git clone https://github.com/ZM25XC/nonebot_plugin_auto_teenstudy.git`指令克隆本仓库或下载压缩包文件\n2. 使用`pip install nonebot-plugin-auto-teenstudy`来进行安装,使用`pip install nonebot-plugin-auto-teenstudy -U`进行更新\n\n## 导入插件\n**使用第一种安装方式**\n\n- 将`nonebot_plugin_auto_teenstudy`放在nb的`plugins`目录下，运行nb机器人即可\n\n**使用第二种安装方式**\n- 在`bot.py`中添加`nonebot.load_plugin("nonebot_plugin_auto_teenstudy")`或在`pyproject.toml`里的`[tool.nonebot]`中添加`plugins = ["nonebot_plugin_auto_teenstudy"]`\n\n\n## 机器人配置\n\n- 在nonebot的.env配置文件中设置好超管账号\n\n  ```py\n  SUPERUSERS=[""]\n  ```\n\n## 功能列表\n|      指令       |           指令格式            |                        说明                        |\n|:-------------:|:-------------------------:|:------------------------------------------------:|\n|     添加大学习     |    添加大学习#地区#json格式用户信息    |           各地区的json格式用户信息不同，详细查看各地区使用方式           |\n|     我的大学习     |           我的大学习           |                      查询个人信息                      |\n|     提交大学习     |           提交大学习           |                    提交最新一期大学习                     |\n|      大学习      |         大学习、青年大学习         |                  获取最新一期青年大学习答案                   |\n|     完成截图      |    完成截图、大学习截图、大学习完成截图     |              获取最新一期青年大学习完成截图（带状态栏）               |\n|      查组织      |  查组织#地区#学校#学院名称+团委#团支部名称  |              江西、浙江地区可使用，用于查询团支部nid               |\n|    个人信息截图     |       个人信息截图、青春湖北截图       |                 湖北地区使用，获取个人信息截图                  |\n|  开启（关闭）大学习推送  |        开启（关闭）大学习推送        |                 开启（关闭）大学习检查更新推送                  |\n| 开启（关闭）自动提交大学习 |       开启（关闭）自动提交大学习       |                 开启（关闭）自动提交大学习 功能                 |\n|     更改信息      |       更改信息 通知方式 群聊        |          可更改项目：openid、token 、通知方式、通知群聊           |\n|     大学习帮助     |   大学习帮助、大学习功能、dxx_help    |                     查看插件详细功能                     |\n| 开启（关闭）大学习图片回复 |       开启（关闭）大学习图片回复       |               插件主人指令、插件回复方式，默认图片回复               |\n|    设置大学习配置    | 设置大学习配置#QQ号#地区#json格式用户信息 |          插件主人指令，添加用户，json格式用户信息同添加大学习指令          |\n|     删除大学习     |         删除大学习#QQ号         |                  插件主人指令，删除个人信息                   |\n|   查看大学习用户列表   |         查看大学习用户列表         |                 插件主人指令，查看插件用户列表                  |\n|    查看大学习用户    |        查看大学习用户#QQ号        |                 插件主人指令，查看用户详细信息                  |\n|     完成大学习     |         完成大学习#QQ号         |               插件主人（团支书）指令，提交用户大学习                |\n| 全局开启（关闭）大学习推送 |       全局开启（关闭）大学习推送       |              插件主人指令，用于开启（关闭）大学习更新推送              |\n|  添加（删除）推送好友   |      添加（删除）推送好友#QQ号       |            插件主人指令，将用户加入（移除）大学习更新推送列表             |\n|  添加（删除）推送群聊   |       添加（删除）推送群聊#群号       |            插件主人指令，将群聊加入（移除）大学习更新推送列表             |\n| 查询推送群聊（好友）列表  |       查询推送群聊（好友）列表        |             插件主人指令，查看大学习更新推送群聊（好友）列表             |\n|     更新大学习     |           更新大学习           |            插件主人指令，用于手动更新青年大学习答案和完成截图             |\n|     推送大学习     |           推送大学习           |                插件主人指令，用于手动启动更新推送                 |\n|     一键提交      |        一键提交、全员大学习         | 插件主人（团支书）指令，一键提交所有（团支部）成员大学习，暂未解决ip池问题（维护中，暂不开放） |\n|     一键提醒      |           一键提醒            |      插件主人（团支书）指令，提醒未完成大学习成员完成大学习（维护中，暂不开放）       |\n|     一键查询      |           一键查询            |         插件主人（团支书）指令，查询大学习完成情况（维护中，暂不开放）          |\n\n## 说明\n- 一键提交、一键提醒和一键查询功能维护更新。\n- 一键提醒和一键查询目前只能查询插件内的提交情况，无法查询公众号提交情况（目前已知福建、上海和安徽地区有接口可查询，正在考虑添加此功能），所以意义不大，暂时不开放。\n- ip池目前没有啥办法解决，大多地区提交大学习时验证SSL,需要https代理，目前免费的https代理少，不稳定。\n- 时间精力有限，目前只维护湖北和江西两个地区，其他地区出问题请提交Issues,我找个时间修，需要增加地区可以提交Pull requests\n- 觉得项目不错，不妨点个stars.\n## To Do\n- [ ] 开发公众号统一推送\n- [ ] 增加ip池，防止多次用同一ip导致封ip\n- [ ] 增加更多地区支持\n- [ ] 优化 Bot\n- [ ] ~~逐步升级成群管插件~~\n\n## 更新日志\n\n### 2022/09/04\n- 更改添加用户方式（使用json格式添加）\n- 统一用户信息存储格式\n- 添加自动提交大学习功能（默认检测到大学习更新后，10~30分钟以后执行自动提交功能）\n- 增加安徽地区\n- 增加山东地区\n- 增加四川地区\n- 重新添加浙江地区\n- 完成截图状态栏时间延后5~10分钟\n- 支持用户修改部分信息（通知方式、通知群号、团支书QQ等）\n### 2022/06/16\n\n- 因浙江地区一个openid只能提交一个人的大学习，故移除对浙江地区支持。\n- 将不支持使用机器人替多人完成大学习的地区的提交文件上传到另一[仓库](https://github.com/ZM25XC/commit_dxx)，单人使用可前往另一个[仓库](https://github.com/ZM25XC/commit_dxx)进行使用\n- 添加自动检查青年大学习更新并推送功能\n- 添加获取最新一期青年大学习答案和完成截图功能，完成截图功能有手机状态栏，状态栏时间会变。\n- 湖北地区增加获取个人信息截图功能。\n- 增加图片回复功能。\n### 2022/06/05\n\n- 增加浙江地区\n- 将爬取[江西](./nonebot_plugin_auto_teenstudy/resource/crawl/crawjx.py)和[浙江](./nonebot_plugin_auto_teenstudy/resource/crawl/crawlzj.py)地区高校团支部数据（抓取nid）文件上传\n### 2022/06/04\n\n- 将代码上传至pypi，可使用`pip install nonebot-plugin-auto-teenstudy`指令安装本插件\n- 增加已支持地区使用提示\n- 上传基础代码\n- 支持江西和湖北地区自动完成大学习（可在后台留记录）返回完成截图',
    'author': 'ZM25XC',
    'author_email': '2393899036@qq.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ZM25XC/nonebot_plugin_auto_teenstudy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
