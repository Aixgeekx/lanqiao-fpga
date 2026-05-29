#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Add FPGA glossary and common Verilog errors to appendix."""

SCRIPT = "Aix_tools/generate_textbook_v3.py"

with open(SCRIPT, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Find the references section and insert glossary before it
ref_idx = None
for idx, line in enumerate(lines):
    if "\u53c2\u8003\u6587\u732e" in line and "sec_title" in line:
        ref_idx = idx
        break

if ref_idx is None:
    print("ERROR: Could not find references section")
    exit(1)

glossary_code = '''
    # ==================== FPGA术语速查 ====================
    story.append(Paragraph("E. FPGA术语速查", st['sec_title']))
    glossary = [
        [th("\u672f\u8bed"), th("\u82f1\u6587"), th("\u7b80\u8981\u89e3\u91ca")],
        [td("\u53ef\u7f16\u7a0b\u903b\u8f91\u5757"), td("CLB"), td("FPGA\u57fa\u672c\u903b\u8f91\u5355\u5143\uff0c\u5305\u542bLUT\u548c\u89e6\u53d1\u5668")],
        [td("\u67e5\u627e\u8868"), td("LUT"), td("\u5b9e\u73b0\u7ec4\u5408\u903b\u8f91\u7684\u57fa\u672c\u7ed3\u6784\uff0c\u5e38\u89c14\u8f93\u5165\u62166\u8f93\u5165")],
        [td("\u89e6\u53d1\u5668"), td("FF / Flip-Flop"), td("\u65f6\u5e8f\u903b\u8f91\u57fa\u672c\u5355\u5143\uff0c\u6bcf\u4e2aCLB\u5185\u542b2\u4e2a")],
        [td("\u5757RAM"), td("BRAM"), td("\u7247\u4e0a\u5b58\u50a8\u5668\uff0c\u7528\u4e8eFIFO\u3001\u67e5\u627e\u8868\u7b49")],
        [td("\u65f6\u949f\u7ba1\u7406\u5355\u5143"), td("CMT / MMCM / PLL"), td("\u65f6\u949f\u500d\u9891\u3001\u5206\u9891\u548c\u76f8\u79fb\u8c03\u6574")],
        [td("\u53ef\u7f16\u7a0bIO"), td("IOB"), td("FPGA\u5f15\u811a\u5355\u5143\uff0c\u652f\u6301LVCMOS33\u7b49\u591a\u79cd\u7535\u5e73")],
        [td("\u7efc\u5408"), td("Synthesis"), td("Verilog\u4ee3\u7801\u2192\u95e8\u7ea7\u7f51\u8868\u7684\u8f6c\u6362\u8fc7\u7a0b")],
        [td("\u5e03\u5c40\u5e03\u7ebf"), td("Place & Route"), td("\u5c06\u7efc\u5408\u7ed3\u679c\u6620\u5c04\u5230FPGA\u5177\u4f53\u8d44\u6e90\u5e76\u8fde\u7ebf")],
        [td("\u6bd4\u7279\u6d41"), td("Bitstream"), td("\u6700\u7ec8\u4e0b\u8f7d\u5230FPGA\u7684\u914d\u7f6e\u6587\u4ef6\uff0c.bit\u683c\u5f0f")],
        [td("\u5f02\u6b65\u590d\u4f4d"), td("Async Reset"), td("\u590d\u4f4d\u4fe1\u53f7\u7acb\u5373\u751f\u6548\uff0c\u4e0d\u7b49\u65f6\u949f\u6cbf")],
        [td("\u540c\u6b65\u590d\u4f4d"), td("Sync Reset"), td("\u590d\u4f4d\u4fe1\u53f7\u9700\u5728\u65f6\u949f\u6cbf\u5230\u6765\u65f6\u624d\u751f\u6548")],
        [td("\u4e9a\u7a33\u6001"), td("Metastability"), td("\u89e6\u53d1\u5668\u91c7\u6837\u8fb9\u6cbf\u9644\u8fd1\u53d8\u5316\u65f6\u7684\u4e0d\u786e\u5b9a\u72b6\u6001")],
        [td("\u4e24\u7ea7\u540c\u6b65\u5668"), td("2-FF Synchronizer"), td("\u89e3\u51b3\u8de8\u65f6\u949f\u57df\u4e9a\u7a33\u6001\u7684\u6807\u51c6\u65b9\u6cd5")],
        [td("\u72b6\u6001\u673a"), td("FSM"), td("\u63a7\u5236\u903b\u8f91\u7684\u6838\u5fc3\u7ed3\u6784\uff0c\u8d35\u5728\u4e09\u6bb5\u5f0f\u5199\u6cd5")],
        [td("\u963b\u585e\u8d4b\u503c"), td("Blocking (=)"), td("\u7ec4\u5408\u903b\u8f91\u4e2d\u4f7f\u7528\uff0c\u7acb\u5373\u751f\u6548")],
        [td("\u975e\u963b\u585e\u8d4b\u503c"), td("Non-blocking (<="), td("\u65f6\u5e8f\u903b\u8f91\u4e2d\u4f7f\u7528\uff0c\u65f6\u949f\u6cbf\u7edf\u4e00\u66f4\u65b0")],
    ]
    t = Table(glossary, colWidths=[3*cm, 3.5*cm, 8.5*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C['primary']),
        ('GRID', (0,0), (-1,-1), 0.5, C['border']),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [white, C['card_bg']]),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2), ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(table_caption(st, "FPGA\\u672f\\u8bed\\u901f\\u67e5"))
    story.append(t)
    story.append(Spacer(1, 5*mm))

    # ==================== 常见Verilog错误速查 ====================
    story.append(Paragraph("F. \u5e38\u89c1Verilog\u9519\u8bef\u4e0e\u4fee\u6b63", st['sec_title']))
    err_rows = [
        [th("\u9519\u8bef\u5199\u6cd5"), th("\u6b63\u786e\u5199\u6cd5"), th("\u539f\u56e0")],
        [td("always @(posedge clk) a = b;"), td("always @(posedge clk) a <= b;"), td("\u65f6\u5e8f\u5757\u5fc5\u987b\u7528\u975e\u963b\u585e\u8d4b\u503c")],
        [td("always @(*) a <= b;"), td("always @(*) a = b;"), td("\u7ec4\u5408\u5757\u5fc5\u987b\u7528\u963b\u585e\u8d4b\u503c")],
        [td("assign a = b + 1; (a\u662freg)"), td("wire a; assign a = b+1;"), td("assign\u53ea\u80fd\u9a71\u52a8wire")],
        [td("reg a; always @(*) a = in;"), td("wire a; assign a = in;"), td("\u7b80\u5355\u8d4b\u503c\u7528assign\u66f4\u6e05\u6670")],
        [td("always @(posedge clk) if(rst) ..."), td("always @(posedge clk or negedge rst_n) if(!rst_n) ..."), td("\u5f02\u6b65\u590d\u4f4d\u9700\u52a0\u5165\u654f\u611f\u5217\u8868")],
        [td("case \u7f3a少 default"), td("case ... default: ... endcase"), td("\u7efc\u5408\u5668\u4f1a\u751f\u6210\u9500\u5b58\u5668")],
        [td("for (i=0; i<8; i=i+1) ..."), td("generate for ... endgenerate"), td("for\u5faa\u73af\u5728always\u5916\u9700\u7528generate")],
    ]
    t = Table(err_rows, colWidths=[5*cm, 5.5*cm, 4.5*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C['primary']),
        ('GRID', (0,0), (-1,-1), 0.5, C['border']),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [white, C['card_bg']]),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2), ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('FONTSIZE', (0,0), (-1,-1), 7),
    ]))
    story.append(table_caption(st, "\u5e38\u89c1Verilog\u9519\u8bef\u4e0e\u4fee\u6b63"))
    story.append(t)

'''

# Insert before the references section
lines.insert(ref_idx, glossary_code)

with open(SCRIPT, "w", encoding="utf-8") as f:
    f.writelines(lines)

print(f"Inserted glossary and error guide at line {ref_idx}")
