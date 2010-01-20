from xml.etree import ElementTree
from datetime import datetime

# A puppy dies every time Fredrik Lundh serializes XML.
NS = "http://www.w3.org/2005/Atom"
ElementTree._namespace_map[NS] = "atom"

def qname(name):
    return unicode(ElementTree.QName(NS, name))

class Atom(object):

    # The filename of the spoon-fed feed.
    FILENAME = "index.xml"

    # The maximum number of <entry> nodes.
    ENTRIES = 15

    def __init__(self, pathname):
        self.pathname = pathname
        try:
            self.etree = ElementTree.parse(self.pathname)
        except IOError:
            feed = ElementTree.Element("feed")
            feed.set("xmlns", NS)
            ElementTree.SubElement(feed, "title").text = "Crowley Code!"
            ElementTree.SubElement(feed, "link",
                href="http://rcrowley.org/feed", rel="self")
            ElementTree.SubElement(feed, "link",
                href="http://rcrowley.org/", rel="alternate")
            ElementTree.SubElement(feed,
                "id").text = "http://rcrowley.org/feed"
            ElementTree.SubElement(feed, "updated")
            ElementTree.SubElement(ElementTree.SubElement(feed,
                "author"), "name").text = "Richard Crowley"
            self.etree = ElementTree.ElementTree(feed)
            self.etree.write(self.pathname)
            self.etree = ElementTree.parse(self.pathname)

    def __del__(self):
        self.etree.find(qname("updated")).text = datetime.now().isoformat()
        self.etree.write(self.pathname)

    def entry(self,
        title=None,
        alternate=None,
        id=None,
        author=None,
        content=None
    ):

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
        #   FIXME This will repeat the headline.
        ElementTree.SubElement(entry, qname("title")).text = title
        ElementTree.SubElement(entry, qname("link"),
            href=alternate, rel="alternate")
        ElementTree.SubElement(entry, qname("id")).text = id
        ElementTree.SubElement(entry, qname("published")).text \
            = datetime.now().isoformat()
        ElementTree.SubElement(entry, qname("updated")).text \
            = datetime.now().isoformat()
        ElementTree.SubElement(ElementTree.SubElement(entry,
            qname("author")), qname("name")).text = author
        ElementTree.SubElement(entry, qname("content"),
            type="html").text = content
