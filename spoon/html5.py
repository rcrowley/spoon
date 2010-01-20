"""
HTML5 parsing.
"""

import html5lib

def article(pathname):
    """
    Find the top-most <article> in the HTML5 document at pathname.
    """
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
    """
    Return the title of the HTML5 <article>.  This is the contents of the
    <h1> and all its children with tags stripped.  If necessary, this will
    traverse <hgroup> and <header> tags.
    """
    for n in article.childNodes:
        if "h1" == n.name:
            return _article_title(n)
        elif "hgroup" == n.name or "header" == n.name:
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
