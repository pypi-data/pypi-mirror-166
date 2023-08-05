__version__ = '0.1.0'

import argparse
from pathlib import Path
from typing import Dict, Callable, Optional, Iterator, TextIO

import bs4
from bs4 import BeautifulSoup


# lib

class Handlers:
    """
    Stores the handlers for each HTML tag.

    A handler is thereby a function that takes a BeautifulSoup Tag object and yields LaTeX code.
    You may yield two strings, the first one being the LaTeX code *before* processing the children,
    and the second one being the code *after* processing the children. You are allowed to omit the second yield,
    if you don't need it.
    """

    def __init__(self):
        self.handlers: Dict[str, Callable] = {}
        """A dictionary mapping tag names to functions that handle them."""

    def register(self):
        """This decorator registers its decorated function as a handler for HTML tags named exactly like the
        function."""

        def decorator(func: Callable):
            handler_for_tag = func.__name__
            self.handlers[handler_for_tag] = func
            return func

        return decorator


class NodeHandler:
    """
    Handles a specific node in the HTML tree.
    Based on the handler function, it writes the corresponding LaTeX code before entering and after leaving the
    node.
    """

    def __init__(self, *, node: bs4.element.Tag, depth: int, output_file: TextIO, handlers: Handlers):
        self.node = node
        self.depth = depth
        self.output_file = output_file
        self.handler = self._get_handler(handlers)

    def _get_handler(self, handlers: Handlers) -> Optional[Iterator[str]]:
        # Get the handler for the current node
        try:
            generator_function = handlers.handlers[self.node.name]
        except KeyError as err:
            # No handler for this tag, so simply ignore it
            # Probably some of its children has a handler
            return None

        # Calling a generator function returns a generator object.
        # This, in turn, can be called with next() to get values.
        generator = generator_function(self.node)
        return generator

    def _exec_handler(self):
        """
        Executes the handler by driving the generator one step forward.
        Indents the yielded text by the current depth and prints it to stdout.
        """

        if self.handler is None:
            return

        try:
            text = next(self.handler)
        except KeyError as err:
            raise ValueError(f"Handler for {self.node.name} needs argument {err}")
        except StopIteration:
            # The handler only yields once,
            # so it does not produce anything after handling all children.
            # This is totally fine. Not every handler needs to do something afterwards
            return

        if isinstance(text, list):
            text = "\n".join(text)

        # Indent *all* lines produced by the handler by the current depth
        indent = '\t' * self.depth
        # Indent the first line
        text = indent + text
        # Indent all following lines
        text = text.replace('\n', '\n' + indent)
        self.output_file.write(text + '\n\n')

    def __enter__(self):
        # Preamble
        self._exec_handler()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # "Postamble"
        self._exec_handler()


class TreeWalker:
    """Walks the tree of HTML nodes and calls the handlers for each node."""

    def __init__(self, *, output: TextIO, handlers: Handlers):
        """
        :param output: The file to which the output is written
        :param handlers: The handlers for the HTML tags.
        """

        self.output_file = output
        self.handlers = handlers

    def _node_handler(self, node: bs4.element.Tag, depth: int = -1) -> NodeHandler:
        """Helper function helping by creating NodeHandlers. Automatically fills in the output_file and handlers."""

        return NodeHandler(node=node, depth=depth, output_file=self.output_file, handlers=self.handlers)

    def walk(self, node: bs4.element.Tag, depth: int = -1):
        """Walks the tree of HTML nodes and calls the handlers for each node."""

        # The NodeHandler is a context manager which calls the first part of the handler (preamble) when starting
        # entering the context and the second part (postamble) when exiting the context.
        # For example, a NodeHandler prints \section{...} when entering the context and \end{section} when exiting.
        with self._node_handler(node, depth) as node_handler:
            # Recursively traverse the children of this node
            for child in node.contents:
                if not isinstance(child, bs4.element.Tag):
                    # Normal text is not a tag, so we don't walk it
                    continue
                self.walk(child, depth + 1)


# bin

handlers = Handlers()


@handlers.register()
def head(node: bs4.element.Tag):
    yield "%%%%%% HEAD START %%%%%%"
    yield "%%%%%% HEAD END %%%%%%"


@handlers.register()
def body(node: bs4.element.Tag):
    yield [
        "%%%%%% MAIN DOCUMENT START %%%%%%",
        r"\begin{document}",
        r"\maketitle",
    ]
    yield [
        r"\end{document}",
        "%%%%%% MAIN DOCUMENT END %%%%%%"
    ]


@handlers.register()
def title(node: bs4.element.Tag):
    yield f"\\title{{{node.text}}}"


@handlers.register()
def meta(node: bs4.element.Tag):
    name = node.attrs['name'] if 'name' in node.attrs else None
    if name == 'author':
        yield r"\author{%s}" % node.attrs['content']
    elif name == 'date':
        yield r"\date{%s}" % node.attrs['content']
    elif name == "link":
        if node.attrs['rel'] == 'icon':
            yield r"\logo{\includegraphics{%s}}" % node.attrs['href']


@handlers.register()
def h1(node: bs4.element.Tag):
    section_name = node.string
    section_id = node.attrs['id']
    yield [
        r"\section{%s}" % section_name,
        r"\label{%s}" % section_id,
    ]


@handlers.register()
def p(node: bs4.element.Tag):
    yield f"{node.string}"


@handlers.register()
def img(node: bs4.element.Tag):
    yield f"\\includegraphics{{{node.attrs['src']}}}"
