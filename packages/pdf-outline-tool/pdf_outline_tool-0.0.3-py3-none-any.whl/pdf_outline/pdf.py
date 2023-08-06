from io import StringIO
from PyPDF2 import PdfReader, PdfWriter


def pdf2toc(pdf, offset):
    # offset is used to fix up the generated page number deviation
    def traverse(root, children):
        for child in children:
            if isinstance(child, dict):
                title = child.title
                page = pdf.get_destination_page_number(child) + offset
                entry = {"title": title, "page": page, "children": []}
                root["children"].append(entry)
            elif isinstance(child, list):
                new_root = root["children"][-1]
                new_children = child
                traverse(new_root, new_children)
            else:
                assert False

    toc = {"title": "TOP", "page": -1, "children": []}
    outlines = pdf.outline
    traverse(toc, outlines)

    return toc


def toc2text(toc, indentation, delimiter):
    textbuffer = StringIO()

    def traverse(root, indent):
        title = root["title"]
        page = root["page"]
        children = root["children"]
        line = " " * indent + f"{title}{delimiter}{page}\n"
        textbuffer.write(line)
        if children:
            for child in children:
                traverse(child, indent + indentation)

    traverse(toc, 0)

    return textbuffer.getvalue()


def toc2pdf(pdf_writer, toc):
    def traverse(root, parent=None):
        title = root["title"]
        page = root["page"]
        children = root["children"]

        new_parent = pdf_writer.add_outline_item(title, page, parent)
        for child in children:
            traverse(child, new_parent)

    for child in toc["children"]:
        traverse(child)


def text2toc(lines, indentation, delimiter):
    indent2parent = {0: None}
    for line in lines:
        indent = (len(line) - len(line.lstrip())) / indentation
        title, page = line.strip().split(delimiter)
        entry = {"title": title, "page": page, "children": []}

        parent = indent2parent[indent]
        if parent is not None:
            parent["children"].append(entry)

        indent2parent[indent + 1] = entry

    toc = indent2parent[1]

    return toc


def gen_toc_from_pdf(pdf_path, txt_path, offset=0, indentation=2, delimiter="::"):
    # offset is used to fix up the generated page number deviation
    pdf = PdfReader(pdf_path)

    toc = pdf2toc(pdf, offset)
    text = toc2text(toc, indentation, delimiter)

    with open(txt_path, "wt") as f:
        f.write(text)


def gen_pdf_with_toc(pdf_path, new_pdf_path, txt_path, indentation=2, delimiter="::"):
    pdf = PdfReader(pdf_path)
    new_pdf = PdfWriter()
    for page in pdf.pages:
        new_pdf.add_page(page)

    with open(txt_path, "rt") as f:
        lines = f.readlines()
    toc = text2toc(lines, indentation, delimiter)

    toc2pdf(new_pdf, toc)
    with open(new_pdf_path, "wb") as f:
        new_pdf.write(f)
