"""
Spoon feeds HTML5 into Atom.
"""

from spoon import atom, html5
from xml.etree import ElementTree
import os

class Spoon(object):
    """
    Spoon feeds HTML5 into Atom.
    """

    def __init__(self,
        document_root=None,
        server_name=None,
        title=None,
        author=None,
        url=None
    ):
        """
        Setup to manage a static site and Atom feed.  Sensible defaults will
        be found as necessary.
        """

        # Find sensible defaults for omitted arguments.
        if document_root is None:
            self.document_root = os.getcwd()
        else:
            self.document_root = document_root
        if server_name is None:
            import socket
            self.server_name = socket.getfqdn()
        else:
            self.server_name = server_name
        if title is None:
            title = self.server_name
        if author is None:
            import pwd
            self.author = pwd.getpwuid(os.getuid())[0]
        else:
            self.author = author
        if url is None:
            url = "http://{0}/{1}".format(self.server_name, "index.xml")

        try:
            os.mkdir(self.document_root)
        except OSError:
            pass

        self.atom = atom.Atom(
            pathname=os.path.join(self.document_root, "index.xml"),
            title=title,
            alternate="http://{0}/".format(self.server_name),
            id=url,
            author=self.author
        )

    def pathname2url(self, pathname):
        """
        Get the web-accessible portion of pathname based on the document_root.
        """
        return os.path.relpath(pathname, self.document_root)

    def publish(self, pathname):
        """
        Publish the HTML5 document at pathname in the Atom feed.
        """

        article = html5.article(pathname)
        title = html5.article_title(article)
        url = "http://{0}/{1}".format(self.server_name,
            self.pathname2url(pathname))

        self.atom.entry(
            title=title,
            alternate=url,
            id=url,
            author=self.author,
            content=article.toxml()
        )

        # TODO Manage links on index.html and archives.html.

    def republish(self, pathname):
        """
        Republish the HTML5 document at pathname in the same <entry> in the
        Atom feed.
        """
        pass # TODO
