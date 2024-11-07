"""
Either parse C code or rst. Easier to do latter

https://dzone.com/articles/a-brief-tutorial-on-parsing-restructuredtext-rest
https://github.com/eliben/code-for-blog/blob/master/2017/parsing-rst/rst-link-check.py

The root cause of the problem is indeed the fact that registering new roles/directives affects docutils 
globally. I don't think this can be easily solved.

https://github.com/sphinx-doc/sphinx/issues/2799

Updated - Now Sphinx installs them on running application.

https://github.com/sphinx-doc/sphinx/commit/84baf05c4f9c3ff3f17779fe522cec7aa444b2f8
https://docutils.readthedocs.io/en/sphinx-docs/howto/rst-directives.html#register-the-directive
http://docutils.sourceforge.net/docs/ref/rst/directives.html#custom-interpreted-text-roles
https://docutils.readthedocs.io/en/sphinx-docs/howto/rst-roles.html

https://github.com/sphinx-doc/sphinx/issues/2922#issuecomment-243377010
Unfortunately, Sphinx is a monolithic application. So there is no way to use only parsers.
"""

import glob, os, codecs

import docutils.frontend
import docutils.nodes
import docutils.parsers.rst
import docutils.utils
import docutils.core

import tempfile

from mappyfile.tokens import COMPOSITE_NAMES, ATTRIBUTE_NAMES, SINGLETON_COMPOSITE_NAMES
import logging
import re
import pprint

from docutils.parsers.rst import directives, roles, nodes, Directive

# from sphinx.directives.other import VersionChange

# tmpdir = tempfile.mkdtemp()
# from sphinx.application import Sphinx
# app = Sphinx(srcdir=tmpdir, confdir=None, outdir=tmpdir, doctreedir=tmpdir, buildername='dummy', status=None)

roles.register_local_role("ref", roles.GenericRole("ref", nodes.reference))
"""

from sphinx.application import Sphinx

class VersionChangeMock(VersionChange):

    def run(self):
        self.state.document.settings.env = app.env
        return super(VersionChangeMock, self).run()

directives.register_directive("deprecated", VersionChangeMock)
"""

# http://www.mapserver.org/mapfile/expressions.html
spatial_functions = [
    "area",
    "fromtext",
    "buffer",
    "difference",
    "eq",
    "intersects",
    "disjoint",
    "touches",
    "overlaps",
    "crosses",
    "within",
    "contains",
    "dwithin",
    "beyond",
]

string_functions = [
    "tostring",
    "commify",
    "upper",
    "lower",
    "initcap",
    "firstcap",
    "length",
]

arithmetic_functions = ["round"]

# http://www.mapserver.org/mapfile/geomtransform.html
geotransform_functions = ["simplify", "buffer", "generalize", "simplifypt", "smoothsia"]

# following are on TODO list in issues.rst
missing_list = set(
    [
        "compfilter",
        "scaletoken",
        "relativeto",
        "triangle",
        "graticule",
        "bindvals",
        "minlength",
        "rangeitem",  # all PHP MapScript only
        "include",
        "base",
        "default_base",
        "qstring",  # all in validation block
        "ows_enable_request",
        "ows_onlineresource",
        "ows_srs",  # should these be included as tokens at all?
        "javascript",
    ]
)
missing_deprecated = set(
    [
        "annotation",
        "labelmaxscale",
        "labelminscale",
        "overlaybackgroundcolor",
        "overlaycolor",
        "overlaymaxsize",
        "overlayminsize",
        "overlayoutlinecolor",
        "overlaysize",
        "overlaysymbol",
        "symbolscale",
        "transparency",
    ]
)


def get_keyword(text):
    """
    Accept a string such as BACKGROUNDCOLOR [r] [g] [b]
    and return backgroundcolor
    """
    first_word = text.split(" ")[0]

    if len(first_word) > 1 and first_word.isupper():
        kwd = str(first_word.lower())
    else:
        kwd = None

    return kwd


def get_values(text):
    """
    Accept a string such as BACKGROUNDCOLOR [r] [g] [b]
    and return ['r', 'g', 'b']
    """

    res = re.findall(r"\[(.*?)\]", text)
    values = []

    for r in res:
        if "|" in r:
            params = r.split("|")
            for p in params:
                values.append(p)
        else:
            values.append(r)

    values = [str(v.lower()) for v in values]

    return values


def process_doc(text):
    """
    The :ref: role is supported by Sphinx but not by plain docutils
    """
    # remove :ref: directives
    document = docutils.core.publish_doctree(
        text
    )  # http://epydoc.sourceforge.net/docutils/private/docutils.nodes.document-class.html
    visitor = RefVisitor(document)
    document.walk(visitor)

    return visitor.kwd, visitor.values


def clean_term(text):
    """
    Processing options

    E.g. PROCESSING "ITEMS=attribute_x,attribute_y,attribute_z"

    CLUSTER_GET_ALL_SHAPES=ON
    CLUSTER_KEEP_LOCATIONS=ON
    CLUSTER_USE_MAP_UNITS=ON
    ITEMS
    """

    key, values = process_doc(text)
    return key, values


class RefVisitor(docutils.nodes.GenericNodeVisitor):
    """
    <paragraph><reference>TEMPLATE <template></reference> [filename]</paragraph>
    """

    def visit_title_reference(self, node):
        pass

    # def visit_reference(self, node):
    #    """
    #    Some keywords are also links (in a :ref:)
    #    """
    #    print type(node.parent)

    #    text = node.astext() # e.g. TEMPLATE <template>
    #    logging.debug(text)
    #    text = text.split(" ")[0].lower()
    #    self.kwd = text

    def visit_paragraph(self, node):
        # print(type(node)) # http://epydoc.sourceforge.net/docutils/private/docutils.nodes.paragraph-class.html
        idx = node.first_child_matching_class(
            nodes.Text
        )  # get the root text for the paragraph
        text = node[idx].astext()
        self.kwd = get_keyword(text)
        self.values = get_values(text)

    def default_visit(self, node):
        pass


class TermVisitor(docutils.nodes.GenericNodeVisitor):
    def visit_term(self, node):
        key, values = clean_term(node.astext())
        if key:
            self.kwds_dict[key] = values
            # print(key, values)

    def visit_paragraph(self, node):
        pn = type(node.parent)
        if pn is docutils.nodes.definition:
            # only check paragraphs that have their parent as a definition
            text = node.astext()
            key, values = clean_term(text)
            if key:
                if key in self.kwds_dict:
                    logging.warning(
                        "The key '%s' is already in the keywords dictionary! Ignoring '%s'",
                        key,
                        text,
                    )
                else:
                    self.kwds_dict[key] = values

    def default_visit(self, node):
        # Pass all other nodes through.
        pass


def read_doc(fn, kwds):
    with codecs.open(fn, encoding="utf-8") as fileobj:
        txt = fileobj.read()

    txt = unicode(txt)

    # Parse the file into a document with the rst parser.
    default_settings = docutils.frontend.OptionParser(
        components=(docutils.parsers.rst.Parser,)
    ).get_default_values()

    default_settings.report_level = "quiet"  # level 4
    document = docutils.utils.new_document(fileobj.name, default_settings)

    parser = docutils.parsers.rst.Parser()
    parser.parse(txt, document)

    # Visit the parsed document with our link-checking visitor.
    visitor = TermVisitor(document)
    visitor.kwds_dict = kwds
    document.walk(visitor)


def read_all_docs(fld):
    rst_files = glob.glob(fld + "/*.txt")

    mapfile_dict = {}
    dict_items = []

    ignore_list = [
        "expressions",
        "geomtransform",
        "encoding",
        "fontset",
        "include",
        "index",
        "template",
        "union",
        "xml_mapfile",
        "xmp_metadata",
    ]

    # fontset is a MAP parameter

    for fn in rst_files:  # [:1]:
        class_name = os.path.splitext(os.path.basename(fn))[0].lower()

        if class_name not in ignore_list:  # and class_name in ["layer"]:
            print("--------%s----------" % class_name)

            kwds = {}
            # add a key for each MapServer class
            # and then set its value to a list of associated keywords
            mapfile_dict[class_name] = kwds

            read_doc(fn, kwds)

    # pprint.pprint(mapfile_dict)

    composite_names = mapfile_dict.keys()
    keywords = []
    parameters = []

    for k, v in mapfile_dict.items():
        for kwd, params in v.items():
            keywords.append(kwd)
            for p in params:
                parameters.append(p)

    mappyfile_keywords = COMPOSITE_NAMES.union(ATTRIBUTE_NAMES).union(
        SINGLETON_COMPOSITE_NAMES
    )
    docs_keywords = composite_names + keywords + parameters

    for p in sorted(set(parameters)):
        print(p)

    functions = set(
        spatial_functions
        + string_functions
        + arithmetic_functions
        + geotransform_functions
    )

    print("Missing from mappyfile:")
    mappyfile_composites = set(COMPOSITE_NAMES.union(SINGLETON_COMPOSITE_NAMES))
    print(sorted(list(set(docs_keywords) - mappyfile_composites - functions)))

    print("Missing from docs:")
    missing = sorted(
        list(
            set(mappyfile_keywords)
            - set(docs_keywords)
            - functions
            - missing_list
            - missing_deprecated
        )
    )
    print(missing)

    # add COLORRANGE to STYLE


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    fld = r"D:\GitHub\docs\en\mapfile"
    read_all_docs(fld)
    print("Done!")
