#!/usr/bin/env python3
"""Convert a Markdown document to Word: python3 tools/md_to_docx.py <file.md> [<out.docx>]

Used for the Interface Definition Document: Bob writes it in Markdown from the .md template, and this
script turns it into a .docx next to it. Handles headings, paragraphs, bold, italic, inline code,
bullet lists, tables (with a grey header row), block quotes and code blocks.
Pure Python standard library: works on Windows, macOS and Linux with no extra packages.
"""
import os
import re
import sys
import zipfile
from xml.sax.saxutils import escape

FONT = "Verdana"
HEADING_SIZES = {1: 32, 2: 26, 3: 22, 4: 20, 5: 18, 6: 18}  # half-points


def run(text, bold=False, italic=False, mono=False, size=18, color=None):
    props = f'<w:rFonts w:ascii="{"Courier New" if mono else FONT}" w:hAnsi="{"Courier New" if mono else FONT}"/>'
    props += "<w:b/>" if bold else ""
    props += "<w:i/>" if italic else ""
    props += f'<w:color w:val="{color}"/>' if color else ""
    props += f'<w:sz w:val="{size}"/>'
    return f'<w:r><w:rPr>{props}</w:rPr><w:t xml:space="preserve">{escape(text)}</w:t></w:r>'


def runs(text, size=18, bold=False, italic=False, color=None):
    """Inline Markdown (**bold**, *italic*, `code`) to Word runs."""
    out = []
    for part in re.split(r"(\*\*[^*]+\*\*|`[^`]+`|(?<![*\w])\*[^*]+\*(?!\w))", text):
        if not part:
            continue
        if part.startswith("**"):
            out.append(run(part[2:-2], True, italic, size=size, color=color))
        elif part.startswith("`"):
            out.append(run(part[1:-1], bold, italic, mono=True, size=size, color=color))
        elif part.startswith("*") and part.endswith("*") and len(part) > 2:
            out.append(run(part[1:-1], bold, True, size=size, color=color))
        else:
            out.append(run(part.replace("&lt;", "<").replace("&gt;", ">"), bold, italic, size=size, color=color))
    return "".join(out)


def para(content, before=60, after=60, indent=None):
    ind = f'<w:ind w:left="{indent}" w:hanging="240"/>' if indent else ""
    return f'<w:p><w:pPr><w:spacing w:before="{before}" w:after="{after}"/>{ind}</w:pPr>{content}</w:p>'


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def table(rows):
    cols = max(len(r) for r in rows)
    border = "".join(f'<w:{s} w:val="single" w:sz="4" w:color="808080"/>'
                     for s in ("top", "left", "bottom", "right", "insideH", "insideV"))
    xml = (f'<w:tbl><w:tblPr><w:tblW w:w="5000" w:type="pct"/><w:tblBorders>{border}</w:tblBorders></w:tblPr>'
           f'<w:tblGrid>{"<w:gridCol/>" * cols}</w:tblGrid>')
    for n, r in enumerate(rows):
        xml += "<w:tr>"
        for c in r + [""] * (cols - len(r)):
            shade = '<w:shd w:val="clear" w:color="auto" w:fill="BFBFBF"/>' if n == 0 else ""
            xml += (f"<w:tc><w:tcPr>{shade}</w:tcPr>"
                    f"{para(runs(c, size=17, bold=(n == 0)), 20, 20)}</w:tc>")
        xml += "</w:tr>"
    return xml + "</w:tbl>" + para("", 0, 60)


def to_document(md):
    body, lines, i = [], md.splitlines(), 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("```"):
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                body.append(para(run(lines[i], mono=True, size=16), 0, 0))
                i += 1
        elif re.match(r"#{1,6} ", line):
            level = len(line) - len(line.lstrip("#"))
            body.append(para(runs(line[level + 1:], size=HEADING_SIZES[level], bold=True), 240, 120))
        elif line.lstrip().startswith("|") and i + 1 < len(lines) and re.match(r"^\s*\|?[\s:|-]+\|?\s*$", lines[i + 1]):
            rows = [cells(line)]
            i += 2
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                rows.append(cells(lines[i]))
                i += 1
            body.append(table(rows))
            continue
        elif re.match(r"\s*[-*] ", line):
            depth = (len(line) - len(line.lstrip())) // 2
            item = re.sub(r"^\s*[-*] ", "", line)
            body.append(para(run("• ") + runs(item), 20, 20, indent=360 + 360 * depth))
        elif line.startswith(">"):
            body.append(para(runs(line.lstrip("> "), italic=True, color="C00000")))
        elif line.strip():
            body.append(para(runs(line)))
        i += 1
    ns = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'
    sect = '<w:sectPr><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1134" w:right="1134" w:bottom="1134" w:left="1134"/></w:sectPr>'
    return f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document {ns}><w:body>{"".join(body)}{sect}</w:body></w:document>'


CONTENT_TYPES = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                 '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
                 '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
                 '<Default Extension="xml" ContentType="application/xml"/>'
                 '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
                 '</Types>')
RELS = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
        '</Relationships>')


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    src = sys.argv[1]
    dst = sys.argv[2] if len(sys.argv) > 2 else os.path.splitext(src)[0] + ".docx"
    with open(src, encoding="utf-8") as f:
        md = f.read()
    with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", CONTENT_TYPES)
        z.writestr("_rels/.rels", RELS)
        z.writestr("word/document.xml", to_document(md))
    print(f"WROTE {dst}")


if __name__ == "__main__":
    main()
