from typing import Final, List, Optional, Tuple

from lxml import etree

from unstructured.logger import get_logger
from unstructured.documents.base import Page
from unstructured.documents.elements import NarrativeText, Title
from unstructured.documents.xml import XMLDocument, VALID_PARSERS
from unstructured.nlp.partition import is_possible_narrative_text, is_possible_title

logger = get_logger()

TEXT_TAGS: Final[List[str]] = ["p", "a", "td", "span", "font"]
HEADING_TAGS: Final[List[str]] = ["h1", "h2", "h3", "h4", "h5", "h6"]
TABLE_TAGS: Final[List[str]] = ["table", "tbody", "td", "tr"]
PAGEBREAK_TAGS: Final[List[str]] = ["hr"]
HEADER_OR_FOOTER_TAGS: Final[List[str]] = ["header", "footer"]


class HTMLDocument(XMLDocument):
    """Class for handling HTML documents. Uses rules based parsing to identify sections
    of interest within the document."""

    def __init__(
        self,
        filename: str,
        stylesheet: Optional[str] = None,
        parser: VALID_PARSERS = None,
    ):

        super().__init__(filename=filename, stylesheet=stylesheet, parser=parser)

    def read(
        self,
        inplace: bool = True,
        skip_table_text: bool = True,
        skip_headers_and_footers: bool = True,
    ) -> Optional[List[Page]]:
        """Reads and structures and HTML document. If present, looks for article tags.
        if there are multiple article sections present, a page break is inserted between them.

        Parameters
        ----------
        inplace:
            If True, sets self.pages. Otherwise returns the list of pages.
        skip_table_text:
            If True, skips text that is contained within a table element
        skip_headers_and_footers:
            If True, ignores any contain that is within <header> or <footer> tags
        """
        logger.info(f"Reading document for file: {self.filename} ...")
        pages: List[Page] = list()
        root = _find_main(self._read_xml())

        articles = _find_articles(root)
        page_number = 0
        page = Page(number=page_number)
        for article in articles:
            descendanttags: Tuple[etree._Element, ...] = tuple()
            for tag in article.iter():
                if skip_headers_and_footers:
                    if _in_header_or_footer(tag):
                        continue
                    if tag.tag == "footer":
                        break

                if _is_text_tag(tag, skip_table_text=skip_table_text):
                    text = _construct_text(tag)
                    if (tag in descendanttags) or (len(text) < 2):
                        # Prevent repeating something that's been flagged as text as we chase it
                        # down a chain
                        continue
                    descendanttags = tuple(tag.iterdescendants())
                    if is_possible_narrative_text(text):
                        page.elements.append(NarrativeText(text=text))
                    elif is_possible_title(text):
                        page.elements.append(Title(text=text))

                elif tag.tag in HEADING_TAGS:
                    text = _construct_text(tag)
                    if is_possible_title(text):
                        page.elements.append(Title(text=text))

                elif tag.tag in PAGEBREAK_TAGS and len(page.elements) > 0:
                    pages.append(page)
                    page_number += 1
                    page = Page(number=page_number)

            if len(page.elements) > 0:
                pages.append(page)
                page_number += 1
                page = Page(number=page_number)

        if inplace:
            self.pages = pages
            return None
        return pages


def _construct_text(tag: etree._Element) -> str:
    """Extracts text from a text tag element."""
    text = ""
    for item in tag.itertext():
        _text = item.strip()
        if _text:
            text += " " + _text

    if tag.tail:
        text = text.strip() + " " + tag.tail.strip()
    return text.strip()


def _is_text_tag(tag: etree.Element, skip_table_text: bool = True) -> bool:
    """Deteremines if a tag potentially contains narrative text."""
    if _has_table_ancestor(tag) and skip_table_text:
        return False

    if tag.tag in TEXT_TAGS:
        return True

    # NOTE(robinson) - This indicates that a div tag has no children. If that's the
    # case and the tag has text, its potential a text tag
    if tag.tag == "div" and len(tag.getchildren()) == 0:
        return True

    return False


def _has_table_ancestor(tag: etree._Element) -> bool:
    """Checks to see a tag has ancestors that are table elements. If so, we consider it to be
    a table element rather than a section of narrative text."""
    for ancestor in tag.iterancestors():
        if ancestor.tag in TABLE_TAGS:
            return True
    return False


def _in_header_or_footer(tag: etree._Element) -> bool:
    """Checks to see if a tag is contained within a header or a footer tag."""
    for ancestor in tag.iterancestors():
        if ancestor.tag in HEADER_OR_FOOTER_TAGS:
            return True
    return False


def _find_main(root: etree._Element) -> etree._Element:
    """Finds the main tag of the HTML document if it exists. Otherwise, returns the
    whole document."""
    main_tag = root.find(".//main")
    return main_tag if main_tag is not None else root


def _find_articles(root: etree._Element) -> List[etree._Element]:
    """Tries to break the HTML document into distinct articles. If there are no article
    tags, the entire document is returned as a single item list."""
    articles = root.findall(".//article")
    if len(articles) == 0:
        # NOTE(robinson) - ref: https://schema.org/Article
        articles = root.findall(".//div[@itemprop='articleBody']")
    return [root] if len(articles) == 0 else articles
