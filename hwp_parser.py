# -*- coding: utf-8 -*-
import os, zlib, zipfile
import xml.etree.ElementTree as ET
import olefile

def extract_text_from_hwpx(file_path):
    text_chunks = []
    with zipfile.ZipFile(file_path, "r") as zf:
        section_files = [f for f in zf.namelist() if f.startswith("Contents/section") and f.endswith(".xml")]
        section_files.sort()
        for s_file in section_files:
            xml_content = zf.read(s_file)
            root = ET.fromstring(xml_content)
            for elem in root.iter():
                if elem.tag.endswith("}t") and elem.text:
                    text_chunks.append(elem.text)
    return " ".join(text_chunks)

def extract_text_from_hwp(file_path):
    if not olefile.isOleFile(file_path):
        return ""
    ole = olefile.OleFileIO(file_path)
    dirs = ole.listdir()
    sections = [d for d in dirs if d[0] == "BodyText" and d[1].startswith("Section")]
    sections.sort(key=lambda x: x[1])
    full_text = []
    for sec in sections:
        stream = ole.openstream(sec)
        data = stream.read()
        try:
            unpacked = zlib.decompress(data, -15)
        except Exception:
            unpacked = data
        text = unpacked.decode("utf-16le", errors="ignore")
        clean = "".join([c for c in text if c.isprintable() or c in "\n\t "])
        full_text.append(clean)
    ole.close()
    return "\n".join(full_text)

def extract_hwp_or_hwpx(file_path):
    if not os.path.exists(file_path):
        return None, "파일을 찾을 수 없습니다."
    ext = os.path.splitext(file_path)[1].lower()
    try:
        if ext == ".hwpx":
            txt = extract_text_from_hwpx(file_path)
            return txt, "HWPX(XML)"
        elif ext == ".hwp":
            txt = extract_text_from_hwp(file_path)
            return txt, "HWP(Binary)"
        else:
            return None, f"지원하지 않는 확장자: {ext}"
    except Exception as e:
        return None, str(e)

if __name__ == "__main__":
    print("=" * 60)
    print(" [3단계] HWP / HWPX 네이티브 텍스트 추출 엔진 테스트")
    print("=" * 60)
    print("엔진 로드 완료: extract_hwp_or_hwpx() 준비됨")
    print("지원 포맷: .hwp (OLE2 5.0+), .hwpx (OWPML Open Specification)")
    print("=" * 60)
