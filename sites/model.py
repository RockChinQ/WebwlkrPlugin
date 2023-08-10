import re
import requests
import random
from bs4 import BeautifulSoup


__site_adapters__ = []
"""网站适配器列表
[
    {
        "regexp": [
            "网址正则表达式0",
            "网址正则表达式1",
        ],
        "cls": <SiteAdapterBase>
    }
]
"""

def site(regexp: list[str]):
    """网站适配器装饰器
    """
    def wrapper(cls):
        __site_adapters__.append({
            "regexp": regexp,
            "cls": cls
        })
        return cls
    return wrapper


user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Version/14.1.2 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Version/14.1 Safari/537.36',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0'
]


class SiteAdapterBase:
    """网站内容适配器的基类"""

    @classmethod
    def feed(cls, url: str) -> bool:
        """判断是否适配此网址"""
        return True

    @classmethod
    def get_html(cls, url: str, timeout: int=10) -> (int, str):
        """获取网页的HTML内容
        
        反反爬策略应该在此应用
        """
        r = requests.get(
            url,
            timeout=timeout,
            headers={
                'User-Agent': random.choice(user_agents)
            }
        )
        
        return r.status_code, r.text
    
    @classmethod
    def get_meta(cls, raw_html: str) -> str:
        """获取网页的meta标签内容"""
        
        soup = BeautifulSoup(raw_html, 'html.parser')
        
        # keywords
        keywords = soup.find('meta', attrs={'name': 'keywords'})
        
        # og:title
        og_title = soup.find('meta', attrs={'property': 'og:title'})
        
        # og:description
        og_description = soup.find('meta', attrs={'property': 'og:description'})
        
        # og:type
        og_type = soup.find('meta', attrs={'property': 'og:type'})
        
        # og:site_name
        og_site_name = soup.find('meta', attrs={'property': 'og:site_name'})
        
        # og:url
        og_url = soup.find('meta', attrs={'property': 'og:url'})
        
        ret = {
            "keywords": keywords['content'] if keywords else '',
            "og_title": og_title['content'] if og_title else '',
            "og_description": og_description['content'] if og_description else '',
            "og_type": og_type['content'] if og_type else '',
            "og_site_name": og_site_name['content'] if og_site_name else '',
            "og_url": og_url['content'] if og_url else '',
        }
        
        return ret

    @classmethod
    def extra_plain(cls, raw_html: str) -> str:
        """提取网页的纯文本内容"""
        soup = BeautifulSoup(raw_html, 'html.parser')
        raw = soup.get_text()

        # 删除所有空行或只有空格的行
        raw = re.sub(r'\n\s*\n', '\n', raw)

        return raw
    
    @classmethod
    def extra_title_element(cls, raw_html: str) -> str:
        """提取网页的标题元素的纯文字"""
        soup = BeautifulSoup(raw_html, 'html.parser')
        raw = soup.title.string

        return raw

    @classmethod
    def regexp_brief(cls, raw_html: str, key: str, regexp: str, briefs: list[str]) -> list[str]:
        """从网页内容中提取信息，加入到briefs列表中"""

        # 多行匹配
        r = re.compile(regexp, re.DOTALL)

        value = r.search(raw_html)

        # value = re.search(regexp, raw_html)
        if value:
            briefs.append(key+": "+value.group(1).strip())
        return briefs

    @classmethod
    def regexp_delete(cls, raw_text: str, regexp: str) -> str:
        return re.sub(regexp, '', raw_text)

    @classmethod
    def make_ret(
        cls,
        status_code: int=200,
        keywords: str='',
        og_title: str='',
        og_description: str='',
        og_type: str='',
        og_site_name: str='',
        author: str='',
        content: str='',
        **kwargs
    ):
        """生成返回的字典"""
        return {
            "status_code": status_code,
            "keywords": keywords,
            "og_title": og_title,
            "og_description": og_description,
            "og_type": og_type,
            "og_site_name": og_site_name,
            "author": author,
            "content": content,
            **kwargs
        }

    @classmethod
    def process(cls, url: str, brief_len: int, **kwargs) -> dict:
        """处理网页内容"""
        status_code, raw_html = cls.get_html(url)
        if status_code != 200:
            return {
                "status_code": status_code,
                "message": "error status code: "+str(status_code)
            }

        plain = cls.extra_plain(raw_html)

        if len(plain) >= brief_len:
            plain = plain[:brief_len]
            
        metas = cls.get_meta(raw_html)

        return cls.make_ret(
            status_code=status_code,
            content=plain,
            **metas,
        )