Comments
========

mappyfile can remove or keep Mapfile comments. This page discusses how comments are retained when using mappyfile.
mappyfile supports both single-line comments starting with a ``#`` and also C-style multi-line comments.

In a Mapfile comments can appear anywhere. That means that in the context of a classic parser (such as lark), 
a ``COMMENT?`` would have to be added between practically every token. This can be done automatically
but it will slow down some parsers (like Earley), or possibly complicate others (like LALR), and 
create a parse-tree that is much harder to process. This means it's much easier to get rid of them at the lexer.

However mappyfile takes a creative approach that makes comments accessible within the tree as a "comment" attribute.

The next sections descibe how comments are stored in the mappyfile Python dictionary structure, and output using
the pretty-printer. See `test_comments.py <https://github.com/geographika/mappyfile/blob/master/tests/test_comments.py>`_
for some sample tests.

Attribute Comments
++++++++++++++++++

Comments will be associated with attribute keys, and stored in a new "__comments__" property
at its parent level. For example a layer with two properties and two comments such as 
below:

.. code-block:: mapfile

    LAYER
        NAME 'Test' # Name comment
        TYPE POLYGON # Type comment
    END

will be transformed into the following structure, where the attribute names are used as key in 
the "__comments__" property:

.. code-block:: json

    {
        "name": "Test", 
        "__type__": "layer", 
        "__comments__": {
            "type": "Type comment", 
            "name": "Name comment"
        }, 
        "type": "polygon"
    }

The location of the comment will decide which attribute it is associated with. A comment will 
always be associated with its preceding attribute. New lines will be ignored, so the Mapfile
below will produce the same output as above:

.. code-block:: mapfile

    LAYER
        NAME 'Test' 
        
        # Name comment on a new line
        TYPE POLYGON 
        
        # Type comment
    END

If a comment falls within the middle of an attribute value, it will be removed (even though this seems to be valid within a Mapfile):

.. code-block:: mapfile

        COLOR  255 #comment will be removed
        0 0

Composite Level Comments
++++++++++++++++++++++++

Any comments directly before or after a composite typename will be associated with
the composite type. 

.. code-block:: mapfile

    # Layer comment
    LAYER
        NAME 'Test'
    END

.. code-block:: json

    {
        "name": "Test", 
        "__type__": "layer", 
        "__comments__": {
            "__type__": "Layer comment"
        }
    }

Multiple Comments
+++++++++++++++++

In both the above cases multiple comments can be stored in a list. This 
will be the same for multiple attribute comments. 

.. code-block:: mapfile

    # Layer comment 1
    # Layer comment 2
    LAYER
        NAME 'Test'
    END

.. code-block:: json

    {
        "name": "Test", 
        "__type__": "layer", 
        "__comments__": {
            "__type__": [
                "Layer comment 1", 
                "Layer comment 2"
            ]
        }
    }

Pretty Printing
---------------

How to format lists of comments?

.. code-block:: mapfile

    NAME "Test" # comment 1 comment 2

Associate with an object - put at top of definition?

.. code-block:: mapfile

    # Map comment 1
    # Map comment 2
    MAP

    END

    # Layer comment
    LAYER

    END