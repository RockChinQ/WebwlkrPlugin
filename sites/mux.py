import re
import logging
import json

from . import model


def process(url: str, brief_len: int=4096, **kwargs) -> str:
    """处理网页内容"""

    adapter_cls: model.SiteAdapterBase = model.SiteAdapterBase

    found = False
    for adapter in model.__site_adapters__:
        for regexp in adapter['regexp']:
            if re.match(regexp, url):
                if not adapter['cls'].feed(url):
                    # 匹中了这个适配器，但适配器不接受这个链接
                    # 则直接检查下一个适配器
                    break
                adapter_cls = adapter['cls']
                found = True
                break
        if found:
            break

    logging.debug("site adapter: {}".format(adapter_cls))

    processed: dict = adapter_cls.process(url, brief_len, **kwargs)

    logging.debug("site adapter ret: {}".format(processed))

    # 处理成纯文本

    text = json.dumps(processed, ensure_ascii=False)

    return text