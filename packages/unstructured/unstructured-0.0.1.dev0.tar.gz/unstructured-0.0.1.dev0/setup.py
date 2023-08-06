from setuptools import setup, find_packages

from unstructured.__version__ import __version__

setup(
    name="unstructured",
    description="A library that prepares raw documents for downstream ML tasks.",
    author="Unstructured Technologies",
    author_email="devops@unstructuredai.io",
    packages=find_packages(),
    version=__version__,
    entry_points={},
    install_requires=[
        "lxml",
        "nltk",
    ],
    extras_require={"pdf": ["layoutparser[layoutmodels,tesseract]"]},
)
