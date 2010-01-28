"""
An Atom feed.
"""

from xml.etree import ElementTree
from datetime import datetime

# A puppy dies every time Fredrik Lundh serializes XML.
NS = "http://www.w3.org/2005/Atom"
ElementTree._namespace_map[NS] = "atom"

def qname(name):
    """
    Return a node name qualified with the Atom namespace.
    """
    return unicode(ElementTree.QName(NS, name))

class Atom(object):
    """
    An Atom feed.
    """

    # The maximum number of <entry> nodes.
    ENTRIES = 15

    def __init__(self, pathname, title, alternate, id, author):
        """
        Setup to manage an Atom feed.
        """
        self.pathname = pathname
        self.title = title
        self.alternate = alternate
        self.author = author
        try:
            self.etree = ElementTree.parse(self.pathname)
        except IOError:
            feed = ElementTree.Element(qname("feed"))
            ElementTree.SubElement(feed, qname("title"), {
                "type": "html"
            }).text = self.title
            ElementTree.SubElement(feed, qname("link"), {
                "href": id,
                "rel": "self"
            })
            ElementTree.SubElement(feed, qname("link"), {
                "href": alternate,
                "rel": "alternate"
            })
            ElementTree.SubElement(feed, "id").text = id
            ElementTree.SubElement(feed, qname("updated"))
            ElementTree.SubElement(ElementTree.SubElement(feed,
                qname("author")), qname("name")).text = self.author
            self.etree = ElementTree.ElementTree(feed)
            self.etree.write(self.pathname)
            self.etree = ElementTree.parse(self.pathname)

    def __del__(self):
        """
        Write the Atom feed back to disk with an updated timestamp.
        """
        self.etree.find(qname("updated")).text
            = datetime.today().strftime("%Y-%m-%dT%H:%M:%SZ")
        self.etree.write(self.pathname)

    def entry(self,
        title=None,
        alternate=None,
        id=None,
        author=None,
        content=""
    ):
        """
        Create a new <entry>, bumping an old one out of the Atom feed if
        necessary.  Fill the new <entry> with the parameters or sensible
        defaults.
        """

        # Find sensible defaults for omitted arguments.
        if title is None:
            title = self.title
        if alternate is None:
            alternate = self.alternate
        if author is None:
            author = self.author

        # Setup the new <entry>.
        entry = self.etree.find(qname("entry"))
        if entry is None:
            entry = ElementTree.SubElement(self.etree.getroot(),
                qname("entry"))
        else:
            i = 0
            for e in self.etree.getroot().getchildren():
                if qname("entry") == e.tag:
                    break
                i += 1
            self.etree.getroot()[i+1:i+self.ENTRIES] \
                = self.etree.getroot()[i:i+self.ENTRIES-1]
            entry = self.etree.getroot()[i] = ElementTree.Element(
                qname("entry"))

        # Place the new article in the <entry>.
        ElementTree.SubElement(entry, qname("title"), {
            "type": "html"
        }).text = title
        ElementTree.SubElement(entry, qname("link"), {
            "href": alternate,
            "rel": "alternate"
        })
        ElementTree.SubElement(entry, qname("id")).text = id
        ElementTree.SubElement(entry, qname("published")).text \
            = datetime.today().strftime("%Y-%m-%dT%H:%M:%SZ")
        ElementTree.SubElement(entry, qname("updated")).text \
            = datetime.today().strftime("%Y-%m-%dT%H:%M:%SZ")
        ElementTree.SubElement(ElementTree.SubElement(entry,
            qname("author")), qname("name")).text = author
        ElementTree.SubElement(entry, qname("content"), {
            "type": "html"
        }).text = content
