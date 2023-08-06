from typing import Dict, List

from unstructured.documents.elements import Text


def convert_to_isd(elements: List[Text]) -> List[Dict[str, str]]:
    """Represents the document elements as an Initial Structured Document (ISD)."""
    isd: List[Dict[str, str]] = list()
    for element in elements:
        section = element.__dict__
        section["type"] = type(element).__name__
        isd.append(section)
    return isd
