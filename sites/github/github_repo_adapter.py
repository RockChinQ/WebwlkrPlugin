from ..model import site, SiteAdapterBase

from bs4 import BeautifulSoup

import re

# 匹配大于两层的路径
@site([
    r'https?://github\.com/([a-zA-Z0-9_-]+)/([a-zA-Z0-9_-]+)',
    r'https?://www\.github\.com/([a-zA-Z0-9_-]+)/([a-zA-Z0-9_-]+)',
])
class GithubRepoSiteAdapter(SiteAdapterBase):

    @classmethod
    def feed(cls, url: str) -> bool:
        """判断是否适配此网址"""
        return True

    @classmethod
    def process(cls, url: str, brief_len: int, **kwargs) -> dict:
        """处理网页内容"""
        status_code, raw_html = cls.get_html(url)
        if status_code != 200:
            return cls.make_ret(
                status_code=status_code,
                message="error"
            )
            
        metas = cls.get_meta(raw_html)

        soup = BeautifulSoup(raw_html, 'html.parser')

        raw = soup.get_text()

        # strip每一行
        raw = '\n'.join([line.strip() for line in raw.split('\n')])

        # 删除所有空行或只有空格的行
        raw = re.sub(r'\n\s*\n', '\n', raw)

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