import html5lib

def article(pathname):
    return _article(html5lib.parse(open(pathname)))
def _article(node):
    if 0 == len(node.childNodes):
        return None
    for n in node.childNodes:
        if "article" == n.name:
            return n
    for n in node.childNodes:
        out = _article(n)
        if out is not None:
            return out

def article_title(article):
    for n in article.childNodes:
        if "h1" == n.name:
            return _article_title(n)
        elif "hgroup" == n.name or "heading" == n.name:
            return article_title(n)
    return None
def _article_title(node):
    title = []
    for n in node.childNodes:
        if n.name is None:
            title.append(n.value)
        else:
            title.extend(_article_title(n))
    return "".join(title)
