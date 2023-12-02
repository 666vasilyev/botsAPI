import re


def link_format(link: str) -> str:
    match = re.search(r"https://t.me/(.*)", link)
    if match:
        return match.group(1)
    else:
        return link
