# -*- coding: utf-8 -*-
"""
将同目录「技术可行性报告正文.md」转为 Word。
正文：宋体 + Times New Roman，小四 12pt，黑色；标题黑体分级。
临时文件仅在系统 Temp，输出目录仅生成 技术可行性报告正文.docx。
依赖：pandoc、py -3
"""
import io
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"


def q(name):
    return "{%s}%s" % (W, name)


def get_ref_bytes():
    r = subprocess.run(
        ["pandoc", "--print-default-data-file", "reference.docx"],
        capture_output=True,
    )
    r.check_returncode()
    return r.stdout


def patch_styles(styles_xml: bytes) -> bytes:
    root = ET.fromstring(styles_xml)
    dd = root.find(".//" + q("docDefaults"))
    if dd is not None:
        rprd = dd.find(q("rPrDefault"))
        if rprd is not None:
            rpr = rprd.find(q("rPr"))
            if rpr is not None:
                for el in list(rpr):
                    if el.tag.endswith("rFonts") or el.tag.endswith("color"):
                        rpr.remove(el)
                rf = ET.Element(q("rFonts"))
                rf.set(q("ascii"), "Times New Roman")
                rf.set(q("hAnsi"), "Times New Roman")
                rf.set(q("eastAsia"), "SimSun")
                rf.set(q("cs"), "Times New Roman")
                rpr.insert(0, rf)
                if not any(e.tag.endswith("color") for e in rpr):
                    co = ET.Element(q("color"))
                    co.set(q("val"), "000000")
                    ins = 0
                    for i, e in enumerate(rpr):
                        if e.tag.endswith("szCs"):
                            ins = i + 1
                    rpr.insert(ins, co)

    def style_rpr(style_id, east_asia, ascii_font, sz_half, bold=False):
        for st in root.findall(".//" + q("style")):
            if st.get(q("styleId")) != style_id:
                continue
            if st.get(q("type")) == "table":
                return
            rpr = st.find(q("rPr"))
            if rpr is None:
                typ = st.get(q("type"))
                if typ not in ("paragraph", "character"):
                    return
                rpr = ET.SubElement(st, q("rPr"))
            for tag in ("rFonts", "sz", "szCs", "color", "b", "bCs"):
                for el in list(rpr):
                    if el.tag.endswith(tag):
                        rpr.remove(el)
            rf = ET.SubElement(rpr, q("rFonts"))
            rf.set(q("ascii"), ascii_font)
            rf.set(q("hAnsi"), ascii_font)
            rf.set(q("eastAsia"), east_asia)
            rf.set(q("cs"), ascii_font)
            ET.SubElement(rpr, q("sz")).set(q("val"), str(sz_half))
            ET.SubElement(rpr, q("szCs")).set(q("val"), str(sz_half))
            ET.SubElement(rpr, q("color")).set(q("val"), "000000")
            if bold:
                ET.SubElement(rpr, q("b"))
                ET.SubElement(rpr, q("bCs"))
            break

    for sid in (
        "BodyText",
        "FirstParagraph",
        "Compact",
        "BlockText",
        "Abstract",
        "Bibliography",
        "Definition",
        "DefinitionTerm",
        "FootnoteText",
        "FootnoteBlockText",
    ):
        style_rpr(sid, "SimSun", "Times New Roman", 24)

    style_rpr("Heading1", "SimHei", "Times New Roman", 30)
    style_rpr("Heading2", "SimHei", "Times New Roman", 28)
    style_rpr("Heading3", "SimHei", "Times New Roman", 24, bold=True)
    style_rpr("Heading4", "SimHei", "Times New Roman", 24, bold=True)
    style_rpr("Heading5", "SimHei", "Times New Roman", 22)
    style_rpr("Heading6", "SimHei", "Times New Roman", 22)
    style_rpr("Title", "SimHei", "Times New Roman", 44)
    style_rpr("Subtitle", "SimHei", "Times New Roman", 28)
    style_rpr("Author", "SimSun", "Times New Roman", 24)
    style_rpr("Date", "SimSun", "Times New Roman", 24)
    style_rpr("TOCHeading", "SimHei", "Times New Roman", 28)
    style_rpr("Caption", "SimSun", "Times New Roman", 20)
    style_rpr("TableCaption", "SimSun", "Times New Roman", 20)
    style_rpr("ImageCaption", "SimSun", "Times New Roman", 20)
    style_rpr("VerbatimChar", "Consolas", "Consolas", 18)
    for sid, sz, bd in [
        ("Heading1Char", 30, False),
        ("Heading2Char", 28, False),
        ("Heading3Char", 24, True),
        ("Heading4Char", 24, True),
        ("Heading5Char", 22, True),
        ("Heading6Char", 22, True),
    ]:
        style_rpr(sid, "SimHei", "Times New Roman", sz, bold=bd)

    ET.register_namespace("w", W)
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def main():
    here = Path(__file__).resolve().parent
    md_src = here / "技术可行性报告正文.md"
    out_final = here / "技术可行性报告正文.docx"
    if len(sys.argv) >= 2:
        md_src = Path(sys.argv[1]).resolve()
    if len(sys.argv) >= 3:
        out_final = Path(sys.argv[2]).resolve()
    if not md_src.is_file():
        sys.exit("找不到: %s" % md_src)
    with open(md_src, "r", encoding="utf-8") as f:
        md_text = f.read()
    tmpd = tempfile.mkdtemp(prefix="pdc_")
    md_tmp = os.path.join(tmpd, "in.md")
    out_tmp = os.path.join(tmpd, "out.docx")
    try:
        with open(md_tmp, "w", encoding="utf-8") as f:
            f.write(md_text)
        ref_data = get_ref_bytes()
        zin = zipfile.ZipFile(io.BytesIO(ref_data), "r")
        ref_path = os.path.join(tmpd, "ref.docx")
        with zipfile.ZipFile(ref_path, "w", zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                data = zin.read(item.filename)
                if item.filename == "word/styles.xml":
                    data = patch_styles(data)
                zout.writestr(item, data)
        zin.close()
        subprocess.run(
            [
                "pandoc",
                md_tmp,
                "-o",
                out_tmp,
                "--reference-doc=" + ref_path,
                "-f",
                "markdown",
                "-t",
                "docx",
                "--standalone",
            ],
            check=True,
        )
        shutil.copy2(out_tmp, str(out_final))
    finally:
        shutil.rmtree(tmpd, ignore_errors=True)
    print("OK:", out_final)


if __name__ == "__main__":
    main()
