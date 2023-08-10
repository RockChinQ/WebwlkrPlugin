from ..model import site, SiteAdapterBase

from bs4 import BeautifulSoup

import re


# 处理github.com/xxx这种网址，排除有二级路径的网址

@site([
    "https?://github.com/[^/^?]+$",
    "https?://www.github.com/[^/^?]+$",
])
class GithubUserSiteAdapter(SiteAdapterBase):

    @classmethod
    def feed(cls, url: str) -> bool:
        """判断是否适配此网址"""
        exclude_url = [
            "https://github.com/pulls",
            "https://github.com/issues",
            "https://github.com/codespaces",
            "https://github.com/marketplace",
            "https://github.com/explore",
            "https://github.com/topics"
        ]
        return url not in exclude_url

    @classmethod
    def process(cls, url: str, brief_len: int, **kwargs) -> dict:
        """处理网页内容"""
        status_code, raw_html = cls.get_html(url)
        if status_code != 200:
            return cls.make_ret(
                status_code=status_code,
                content="error: "+str(status_code),
            )
            
        metas = cls.get_meta(raw_html)

        soup = BeautifulSoup(raw_html, 'html.parser')

        raw = soup.get_text()

        delete = """Actions
        Automate any workflow
        Packages
        Host and manage packages
        Security
        Find and fix vulnerabilities
        Codespaces
        Instant dev environments
        Copilot
        Write better code with AI
        Code review
        Manage code changes
        Issues
        Plan and track work
        Discussions
        Collaborate outside of code
        Explore
        All features
        Documentation
        GitHub Skills
        Blog
        Solutions
        For
        Enterprise
        Teams
        Startups
        Education
        By Solution
        CI/CD & Automation"""
        
        del_spt = delete.split('\n')
        
        for i in del_spt:
            raw = re.sub(i, '', raw)

        raw = re.sub(r'Stars', '', raw)

        # strip每一行
        raw = '\n'.join([line.strip() for line in raw.split('\n')])

        # 删除所有空行或只有空格的行
        raw = re.sub(r'\n\s*\n', '\n', raw)
        
        # 删除任何包含`contributions on`的行
        raw = re.sub(r'.*contributions? on.*', '', raw)

        # 删除仅包含月份的行
        month = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'Novermber', 'December', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        for i in month:
            raw = re.sub(r'\n'+i+r'\n', '', raw)
            
        # 删除仅包含星期的行
        week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        for i in week:
            raw = re.sub(r'\n'+i+r'\n', '', raw)

        # strip每一行
        raw = '\n'.join([line.strip() for line in raw.split('\n')])

        # 删除所有空行或只有空格的行
        raw = re.sub(r'\n\s*\n', '\n', raw)
        
        if len(raw) > brief_len:
            raw = raw[:brief_len] + "..."

        return cls.make_ret(
            status_code=status_code,
            content=raw,
            **metas
        )