{1}

# A Simple Document

This document highlights some markdown features.

## Blocks

### Paragraphs

Paragraphs are contiguous collections of lines, and newlines are
ignored for the purposes of formatting unless the newline is preceeded
by two or more spaces (e.g. the line ends in two or more spaces),
which s an explicit request  
for a line break.

There is special syntax to create markup within a paragraph, discussed
below in the 'Inline' section.

### HTML

An HTML block starts with an html tag in the first column, and ends with
the next HTML endtag in the first column. For example:

<table border="1">
  <tr><td>Apple</td><td>1</td></tr>
</table>

### Blockquote

You can create a blockquote by starting a line with '> '

> This text will be wrapped in a blockquote.
> When converted to HTML. When rendered in ascii it
> will keep the same structure.

### Code

You can insert code from an artibrary programming language
using two different syntaxes:

~~~python
class Person(Object):
  def __init__(self, name):
    self._name = name
~~~

or:

    class Person(Object):
      def __init__(self, name):
        self._name = name

with the former being more useful because it allows one to specify which
language the code is implemented in.  In HTML, the code is syntax
highlighted using [highlight.js](https://highlightjs.org/).

{2}

### Tables

One can specify a table with the following syntax:

Table: Fruit

| Fruit     | Count |
| :----     | ----: |
| Apple     |     3 |
| Banana    |     1 |
| Cantelope |     2 |



### Panels

One can specify a panel with the following syntax:

Panel: Example Panel

    The panel text must be indented at least four spaces so that
    it looks like a code block or blocks.

    For example, this paragraph is part of the panel too.


### Lists

One can specify unordered lists with hyphens:

- this is a first point
- here is a second point across multiple lines
  to show how it is handled
- a third line in which the continuation lines are not
indented, but is still handled properly. This only
works until the first empty line, which signals the
end of the list (like what happens with
the paragraph below this). If you want multiple
blocks in a list, indent them.

One can specify ordered lists with numbers:

 1. apple

    - Nested lists are easy to write

 2. banana

    - Nested lists can have nested paragraphs

      > and blockquotes

      ~~~bash
      and code blocks
      ~~~

      and any other kind of block (table, etc.)

 3. cantelope

This verifies that unindented paragraphs terminate the list, and the following
shows that list items do not need empty lines before them.

 * Apple
 * Banana
 * Cantelope

## A Second Level-2 Section

To test parsing of upper sections.





### A subsubsection

Another section.

## Titled Blocks

It is sometimes useful to parse a section by title blocks,
as in this example.

**Light Green**: This is an initial titled paragraph

With a second untitled paragraph afterward.

**Red**. And this is another titled paragraph.

With a second paragraph and third list.

* **Light**: simple para.

* **Dark**: another simple

  With second para

* **Medium**: third.

* list item with no title.

## Final thoughts

How is this?

#### A level 4 within a level 2

Is this handled properly?

# And another top-level section

Does this get parsed too?
DO NOT ADD MORE SECTIONS BELOW THIS (test code relies on this being the last section)
