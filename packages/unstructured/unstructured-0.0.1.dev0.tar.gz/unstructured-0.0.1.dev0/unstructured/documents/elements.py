from abc import ABC
from typing import Optional
from uuid import uuid4


class Element(ABC):
    """An element is a section of a page in the document."""

    def __init__(self, element_id: Optional[str] = None):
        element_id = uuid4().hex if not element_id else element_id
        self.id: str = element_id


class Text(Element):
    """Base element for capturing free text from within document."""

    def __init__(self, text: str, element_id: Optional[str] = None):
        self.text: str = text
        super().__init__(element_id=element_id)

    def __str__(self):
        return self.text

    def __eq__(self, other):
        return self.text == other.text


class NarrativeText(Text):
    """NarrativeText is an element consisting of multiple, well-formulated sentences. This
    excludes elements such titles, headers, footers, and captions."""

    pass


class Title(Text):
    """A text element for capturing titles."""

    pass
