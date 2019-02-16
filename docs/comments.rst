Comments Design Notes
=====================

Parsing
-------

There are currently 2 comment tokens in the grammar:

.. code-block:: bat

    COMMENT: /\#[^\n]*/
    CCOMMENT.3: /\/[*].*?[*]\//s

Questions
+++++++++

+ Would the comment tokens have to be added throughout the grammar? This would result
  in a messy, hard to read grammar. Is there any way to add comment tokens automatically?

From ``erezsh``:

    Regarding comments, you are correct that the problem is that comments can appear anywhere. 
    That means that in the context of a classic parser (such as lark), you will have to add COMMENT? 
    between practically every token. It can be done automatically (in fact Lark implements such operations), 
    but it will slow down some parsers (like earley), or possibly complicate others (like lalr), and even if not, 
    it will create a parse-tree that is obviously much harder to process. So, you can see that it's much easier 
    to get rid of them at the lexer.
    Having said that, with some creativity it should be possible to make comments accessible within the tree, 
    for example as a "comment" attribute.

+ Is it therefore possible to have this as an option that can be enabled (with comments removed by default)?

Transformer
-----------

See ``tests/test_comments.py`` for some sample tests. 

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
always be associated with its preceeding attribute. New lines will be ignored, so the Mapfile
below will produce the same output as above:

.. code-block:: mapfile

    LAYER
        NAME 'Test' 
        
        # Name comment on a new line
        TYPE POLYGON 
        
        # Type comment
    END

If a comment falls within the middle of an attribute value, it will also be associated the preceeding
attribute. In the case below the comment will be associated with ``COLOR``. 

.. code-block:: mapfile

        COLOR  255 #comment
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