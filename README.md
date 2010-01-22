spoon(7) -- Spoon feeds HTML5 into Atom
=======================================

## SYNPOSIS

	import spoon
	s = spoon.Spoon(document_root, server_name, title, author)
	s.publish(pathname)

## DESCRIPTION

Spoon is a Python library for managing an Atom feed on a static Web site.  The feed is maintained at `{document_root}/index.xml`.  When publishing, the Atom feed adds a new `<entry>` node at the beginning and removes the last one if necessary to keep the total at 15.  The HTML5 document at `pathname` is parsed to find the outermost `<article>` node.  The title of that `<article>` element, as found by traversing `<header>`, `<hgroup>`, and `<h1>` nodes, is used as the `<title>` node in the Atom feed.  By default, the author of the entire feed will be listed as the author of each article; this may be overridden using the `author` keyword argument to `Spoon.publish`.  The content of the `<article>` will become the `<content>` node in the Atom feed.

## OPTIONS

Options to `Spoon`'s constructor:

* `document_root`:
  This should agree with your Web server's document root as it is used to construct URLs from absolute paths.
* `server_name`:
  By default, `socket.getfqdn` will be used to determine the server's name but this is frequently wrong in shared environments and is always wrong if you publish and then push to production.
* `title`:
  The site's title as the Atom feed should report it.
* `author`:
  The site's author as the Atom feed should report it.  This will be used by default for all published articles.
* `url`:
  URL the Atom feed should use for itself.  This will not change the path where the Atom feed is stored.  This is mostly for mod_rewrite users.

Options to `Spoon.publish`:

* `pathname`:
  Absolute path to the article to be published.  It must be within `document_root`.

## DEPENDENCIES

* Python 2.6 <http://python.org/>

## AUTHOR

Richard Crowley <r@rcrowley.org>

## SEE ALSO

* <http://github.com/rcrowley/spoon>
* <http://github.com/rcrowley/rcrowley/blob/master/bin/publish>
* <http://github.com/mojombo/jekyll>

## LICENSE

<http://www.freebsd.org/copyright/freebsd-license.html>
