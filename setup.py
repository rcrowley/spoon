import distutils.core

distutils.core.setup(
    name="spoon",
    version="0.1",
    packages=["spoon"],
    requires=["html5lib"],
    author="Richard Crowley",
    author_email="r@rcrowley.org",
    url="http://github.com/rcrowley/spoon",
    license="BSD",
    description="Spoon feeds HTML5 into Atom.",
)
