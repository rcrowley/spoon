from spoon import atom, html5
from xml.etree import ElementTree
import os

class Spoon(object):
    """
    Spoon feeds HTML5.
    """

    def __init__(self, document_root):
        self.document_root = document_root
        try:
            os.mkdir(self.document_root)
        except OSError:
            pass
        self.atom = atom.Atom(os.path.join(
            self.document_root,
            atom.Atom.FILENAME
        ))

    def pathname2url(self, pathname):
        return os.path.relpath(pathname, self.document_root)

    def publish(self, pathname):

        article = html5.article(pathname)
        title = html5.article_title(article)
        url = "http://rcrowley.org/{0}".format(self.pathname2url(pathname))

        self.atom.entry(
            title=title,
            alternate=url,
            id=url,
            author="Richard Crowley",
            content=article.toxml()
        )

        # TODO Manage links on index.html and archives.html.

    def republish(self, pathname):
        pass
