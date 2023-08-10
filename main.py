from pkg.plugin.models import *
from pkg.plugin.host import EventContext, PluginHost

import logging
import re
import os
import shutil
import yaml

from .sites import mux


from . import webpilot

backend_mapping = {
    "webpilot": webpilot.process,
    "native": mux.process,
}

process: callable = None


# 注册插件
@register(name="Webwlkr", description="基于GPT的函数调用能力，为QChatGPT提供联网功能", version="0.1.1", author="RockChinQ")
class WebwlkrPlugin(Plugin):

    cfg: dict = None

    # 插件加载时触发
    # plugin_host (pkg.plugin.host.PluginHost) 提供了与主程序交互的一些方法，详细请查看其源码
    def __init__(self, plugin_host: PluginHost):
        global process
        # 检查webwlkr.yaml是否存在
        if not os.path.exists("webwlkr.yaml"):
            shutil.copyfile("plugins/WebwlkrPlugin/config-template.yaml", "webwlkr.yaml")
        
        # 读取配置文件
        with open("webwlkr.yaml", "r", encoding="utf-8") as f:
            self.cfg = yaml.load(f, Loader=yaml.FullLoader)

        process = backend_mapping[self.cfg["backend"]]


    @func("access_the_web")
    def _(url: str, brief_len: int=4096):
        """Call this function to search about the question before you answer any questions.
        - Do not search through google.com at any time.
        - If you need to search somthing, visit https://www.sogou.com/web?query=<something>.
        - If user ask you to open a url (start with http:// or https://), visit it directly.
        - Summary the plain content result by yourself, DO NOT directly output anything in the result you got.

        Args:
            url(str): url to visit
            brief_len(int): max length of the plain text content, recommend 1024-4096, prefer 4096
        """
        try:
            return process(url, brief_len)
        except Exception as e:
            logging.error("[Webwlkr] error visit web: {}".format(e))
            return "error visit web:{}".format(e)

    # 插件卸载时触发
    def __del__(self):
        pass
