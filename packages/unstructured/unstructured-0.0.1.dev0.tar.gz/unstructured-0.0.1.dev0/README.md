## `unstructured`

The `unstructured` library provides utilities for extracting data from unstructured documents.
After extracting the data, you can feed it into downstream ML models.

## Installation

You can install the library by cloning the repo and running `make install` from the
root directory. Developers can run `make install-local` to install the dev and test
requirements alongside the base requirements.

For XML and HTML parsing, you'll need `libxml2` and `libxlst` installed. On a Mac, you can do
that with:

```bash
brew install libxml2
brew install libxslt
```

## Examples

### PDF Parsing

Once installed, you can try the following using the
[layoutparser](https://arxiv.org/pdf/2103.15348.pdf). paper as an example. The PDF
of the paper is available in the `example-docs` directory.

```python
from unstructured.documents.pdf import PDFDocument

doc = PDFDocument("example-docs/layout-parser-paper.pdf")
doc.read()
print(doc)
```

At this point, `print(doc)` will print out a string representation of the PDF file. The
first page of output looks like the following:

```

LayoutParser : A Uniﬁed Toolkit for Deep Learning Based Document Image Analysis

Zejiang Shen 1 ( (cid:0) ), Ruochen Zhang 2 , Melissa Dell 3 , Benjamin Charles Germain Lee 4 , Jacob Carlson 3 , and
Weining Li 5

Abstract. Recent advances in document image analysis (DIA) have been primarily driven by the application of neural
networks. Ideally, research outcomes could be easily deployed in production and extended for further investigation.
However, various factors like loosely organized codebases and sophisticated model conﬁgurations complicate the easy
reuse of im- portant innovations by a wide audience. Though there have been on-going eﬀorts to improve reusability and
simplify deep learning (DL) model development in disciplines like natural language processing and computer vision, none
of them are optimized for challenges in the domain of DIA. This represents a major gap in the existing toolkit, as DIA
is central to academic research across a wide range of disciplines in the social sciences and humanities. This paper
introduces LayoutParser , an open-source library for streamlining the usage of DL in DIA research and applica- tions.
The core LayoutParser library comes with a set of simple and intuitive interfaces for applying and customizing DL models
for layout de- tection, character recognition, and many other document processing tasks. To promote extensibility,
LayoutParser also incorporates a community platform for sharing both pre-trained models and full document digiti- zation
pipelines. We demonstrate that LayoutParser is helpful for both lightweight and large-scale digitization pipelines in
real-word use cases. The library is publicly available at https://layout-parser.github.io

Keywords: Document Image Analysis · Deep Learning · Layout Analysis · Character Recognition · Open Source library ·
Toolkit.

Introduction

Deep Learning(DL)-based approaches are the state-of-the-art for a wide range of document image analysis (DIA) tasks
including document image classiﬁcation [11,
```

The `Document` has a `pages` attribute consisting of `Page` object and the `Page` object
has an `element` attribute consisting of `Element` objects. Sub-types of the `Element` class
represent different components of a document, such as `NarrativeText` and `Title`. You can use
these normalized elements to zero in on the components of a document you most care about.

### HTML Parsing

You can parse an HTML document using the following command.

```python
from unstructured.documents.html import HTMLDocument

doc = HTMLDocument("example-docs/example-10k.html")
doc.read()
print(doc.pages[2])
```

The output of this will be the following:

```
SPECIAL NOTE REGARDING FORWARD-LOOKING STATEMENTS

This report contains statements that do not relate to historical or current facts but are “forward-looking” statements. These statements relate to analyses and other information based on forecasts of future results and estimates of amounts not yet determinable. These statements may also relate to future events or trends, our future prospects and proposed new products, services, developments or business strategies, among other things. These statements can generally (although not always) be identified by their use of terms and phrases such as anticipate, appear, believe, could, would, estimate, expect, indicate, intent, may, plan, predict, project, pursue, will continue and other similar terms and phrases, as well as the use of the future tense.

Actual results could differ materially from those expressed or implied in our forward-looking statements. Our future financial condition and results of operations, as well as any forward-looking statements, are subject to change and to inherent known and unknown risks and uncertainties. You should not assume at any point in the future that the forward-looking statements in this report are still valid. We do not intend, and undertake no obligation, to update our forward-looking statements to reflect future events or circumstances.
```

If you then run:

```python
doc.pages[2].elements
```

You'll get the following output, showing that the parser successfully differentiated between
titles and narrative text.

```python
[<unstructured.documents.base.Title at 0x169cbe820>,
 <unstructured.documents.base.NarrativeText at 0x169cbe8e0>,
 <unstructured.documents.base.NarrativeText at 0x169cbe3a0>]
```

### Building the documentation

The documentation for the library is built with `sphinx`. To build the documentation, run
`cd docs && make html`. After that runs, you can view the documentation page at
`docs/build/html/index.html`. You'll need the build dependencies installed to build the docs.
