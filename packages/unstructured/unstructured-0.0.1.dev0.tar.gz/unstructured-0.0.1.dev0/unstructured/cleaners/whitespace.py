import re


def clean_extra_spaces(text: str, lowercase: bool = False) -> str:
    """Cleans extra whitespace characters that appear between words.

    Example
    -------
    ITEM 1.     BUSINESS -> ITEM 1. BUSINESS
    """
    text = text.lower() if lowercase else text
    cleaned_text = text.rstrip(".,:;")
    cleaned_text = re.sub(r"[-\xa0\n]", " ", cleaned_text)
    cleaned_text = re.sub(r"([ ]{2,})", " ", cleaned_text).strip()
    return cleaned_text
