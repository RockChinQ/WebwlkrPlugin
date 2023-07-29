from pkg.plugin.models import *
from pkg.plugin.host import EventContext, PluginHost

import re

# 注册插件
@register(name="Webwlkr", description="基于GPT的函数调用能力，为QChatGPT提供联网功能", version="0.1", author="RockChinQ")
class WebwlkrPlugin(Plugin):

    # 插件加载时触发
    # plugin_host (pkg.plugin.host.PluginHost) 提供了与主程序交互的一些方法，详细请查看其源码
    def __init__(self, plugin_host: PluginHost):
        pass

    @func("access_the_web")
    def _(url: str, brief_len: int):
        """Call this function to search about the question before you answer any questions.
        - Do not search through baidu.com at any time.
        - If you need to search somthing, visit https://www.google.com/search?q=xxx.
        - If user ask you to open a url (start with http:// or https://), visit it directly.
        - Summary the plain content result by yourself, DO NOT directly output anything in the result you got.

        Args:
            url(str): url to visit
            brief_len(int): max length of the plain text content, recommend 1024-4096, prefer 4096

        Returns:
            str: plain text content of the web page or error message(starts with 'error:')
        """
        try:
            import requests
            from bs4 import BeautifulSoup

            r = requests.get(
                url,
                timeout=10,
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.183"
                }
            )
            soup = BeautifulSoup(r.text, 'html.parser')

            s = soup.get_text()

            # 删除多余的空行或仅有\t和空格的行
            s = re.sub(r'\n\s*\n', '\n', s)

            if len(s) >= brief_len:
                return s[:brief_len]

            return s
        except Exception as e:
            return "error visit web:{}".format(e)

    # 插件卸载时触发
    def __del__(self):
        pass
