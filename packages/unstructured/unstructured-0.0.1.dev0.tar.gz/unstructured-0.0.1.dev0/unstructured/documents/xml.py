import os
import tempfile
from typing import Optional, Union

import lxml.etree as etree

from unstructured.logger import get_logger
from unstructured.documents.base import Document

logger = get_logger()

VALID_PARSERS = Union[etree.HTMLParser, etree.XMLParser, None]


class XMLDocument(Document):
    """Class for handling .xml documents. This class uses rules based parsing to identify
    sections of interest within the document."""

    def __init__(
        self,
        filename: str,
        stylesheet: Optional[str] = None,
        parser: VALID_PARSERS = None,
    ):
        """Class for parsing XML documents. XML documents are parsed using lxml.

        Parameters
        ----------
        filename:
            The name of the XML file to read
        stylesheet:
            An XLST stylesheet that can be applied to transform the XML file
        parser:
            The lxml parser to use with the file. The HTML parser is used by default
            because it is more tolerant of special characters and malformed XML. If you
            are using a stylesheet, you likely want the XMLParser.
        """
        if not parser:
            parser = etree.XMLParser() if stylesheet else etree.HTMLParser()

        self.stylesheet = stylesheet
        self.parser = parser
        self.document_tree = None
        super().__init__(filename=filename)

    def read(self):
        raise NotImplementedError

    def _read_xml(self):
        """Reads in an XML file and converts it to an lxml element tree object."""
        if self.document_tree is None:
            with open(self.filename, "r+") as f:
                content = f.read().encode()
            document_tree = etree.fromstring(content, self.parser)

            if self.stylesheet:
                if isinstance(self.parser, etree.HTMLParser):
                    logger.warning(
                        "You are using the HTML parser with an XSLT stylesheet. "
                        "Stylesheets are more commonly parised with the "
                        "XMLParser. If your HTML does not display properly, try "
                        "`import lxml.etree as etree` and setting "
                        "`parser=etree.XMLParser()` instead."
                    )
                xslt = etree.parse(self.stylesheet)
                transform = etree.XSLT(xslt)
                document_tree = transform(document_tree)

            self.document_tree = document_tree

        return self.document_tree

    @classmethod
    def from_string(cls, text: str, parser: VALID_PARSERS = etree.HTMLParser()):
        """Supports reading in an XML file as a raw string rather than as a file."""
        logger.info("Reading document from string ...")
        tmp = tempfile.NamedTemporaryFile(delete=False)
        tmp.write(text.encode())
        tmp.close()
        doc = cls(filename=tmp.name, parser=parser)
        doc._read_xml()
        os.unlink(tmp.name)
        return doc
