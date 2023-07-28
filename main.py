from pkg.plugin.models import *
from pkg.plugin.host import EventContext, PluginHost

# 注册插件
@register(name="Webwlkr", description="基于GPT的函数调用能力，为QChatGPT提供联网功能", version="0.1", author="RockChinQ")
class WebwlkrPlugin(Plugin):

    # 插件加载时触发
    # plugin_host (pkg.plugin.host.PluginHost) 提供了与主程序交互的一些方法，详细请查看其源码
    def __init__(self, plugin_host: PluginHost):
        pass

    @on(ContentFunction)
    def visit_page(lnk: str):
        """Visit the provided link and return the plain text content.
        
        Args:
            lnk(str): The link to visit.

        Returns:
            str: The plain text content of the page.
        """
        import requests
        from bs4 import BeautifulSoup

        r = requests.get(lnk)
        soup = BeautifulSoup(r.text, 'html.parser')

        s = soup.get_text()

        if len(s) >= 256:
            return s[:256]

        return s

    # 插件卸载时触发
    def __del__(self):
        pass
