from pathlib import Path
import re
import sys

try:
    import fitz
except Exception as exc:
    raise SystemExit(f"repair_pdf_stats error: cannot import fitz: {exc}")

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "results" / "蓝桥杯FPGA开发教程_详细注释版.pdf"

if not PDF.exists():
    raise SystemExit("repair_pdf_stats error: pdf not found")

doc = fitz.open(PDF)
text = "".join(page.get_text() for page in doc)
chars = len(text)
table_numbers = [int(n) for n in re.findall(r"表\s*(\d+)", text)]
tables = max(table_numbers) if table_numbers else 0

paths = [
    ROOT / ".claude" / "progress.md",
    ROOT / "Aix_tools" / "readme.md",
    ROOT / "project" / "lanqiao-fpga-textbook" / "README.md",
    ROOT / "project" / "lanqiao-fpga-textbook" / "docs" / "Aix_tools_readme.md",
]
docs_dir = ROOT / "project" / "lanqiao-fpga-textbook" / "docs"
paths.extend(p for p in docs_dir.glob("*FPGA*.md") if p.is_file())

patterns = [
    (r"正文可抽取字符：\d+", f"正文可抽取字符：{chars}"),
    (r"正文可抽取字符 \d+ 个", f"正文可抽取字符 {chars} 个"),
    (r"全部\d+个表格", f"全部{tables}个表格"),
    (r"\d+个表格全部带", f"{tables}个表格全部带"),
    (r"表格编号：\d+个表格", f"表格编号：{tables}个表格"),
]

changed = []
for path in paths:
    if not path.exists():
        continue
    old = path.read_text(encoding="utf-8")
    new = old
    for pattern, repl in patterns:
        new = re.sub(pattern, repl, new)
    if new != old:
        path.write_text(new, encoding="utf-8")
        changed.append(str(path.relative_to(ROOT)).replace("\\", "/"))

if changed:
    print("repair_pdf_stats fixed " + ", ".join(changed))
