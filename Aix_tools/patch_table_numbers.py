#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Patch generate_textbook_v3.py to add table/figure numbering and references."""

SCRIPT = "Aix_tools/generate_textbook_v3.py"

with open(SCRIPT, "r", encoding="utf-8") as f:
    lines = f.readlines()

insertions = []  # (line_index_0_based, text_to_insert)

# === TABLE CAPTIONS ===
table_captions = {
    287: "\u7eb8\u8d28\u4f7f\u7528\u5efa\u8bae",
    303: "\u96f6\u57fa\u784014\u5929\u5b66\u4e60\u8def\u7ebf",
    328: "\u8d5b\u573a\u901f\u67e5\u5361",
    709: "I2C\u8bbe\u5907\u5730\u5740\u8868",
    737: "\u6570\u7801\u7ba1\u6bb5\u7801\u8868\uff08\u5171\u9633\u6781\uff09",
    759: "\u7535\u6e90\u914d\u7f6e",
    815: "Vivado\u5de5\u7a0b\u521b\u5efa\u6d41\u7a0b",
    843: "\u5b8c\u6574\u5f15\u811a\u6620\u5c04\u8868",
    920: "\u7b2c17\u5c4a\u7701\u8d5b\u9898\u76ee\u6458\u8981",
    935: "\u7a0b\u5e8f\u8bbe\u8ba1\u9898FSM\u901f\u67e5",
    952: "\u771f\u9898\u8bad\u7ec3\u7d22\u5f15\u4e0e\u9519\u9898\u590d\u76d8",
    965: "\u9519\u9898\u590d\u76d8\u6a21\u677f",
    983: "\u7b2c16\u5c4a\u56fd\u8d5b\u6a21\u5757\u4e0e\u8981\u6c42",
    998: "\u754c\u9762\u4e0e\u6309\u952e\u529f\u80fd\u901f\u67e5",
    1013: "\u4e32\u53e3\u4e0a\u62a5\u683c\u5f0f",
    1093: "SPI\u6a21\u5f0f\u914d\u7f6e",
    1247: "DS1302\u5bc4\u5b58\u5668\u5730\u5740\u8868",
    1268: "W25Q128 SPI\u547d\u4ee4\u8868",
    1294: "\u5b98\u65b9\u8d44\u6599\u4f9d\u636e\u901f\u67e5",
    1317: "CT137X\u5173\u952e\u786c\u4ef6\u4e8b\u5b9e",
}

for line_num, caption_text in sorted(table_captions.items()):
    idx = line_num - 1
    if idx < len(lines) and "story.append(t)" in lines[idx]:
        indent = lines[idx][:len(lines[idx]) - len(lines[idx].lstrip())]
        insertions.append((idx, f'{indent}story.append(table_caption(st, "{caption_text}"))\n'))
    else:
        print(f"WARNING: Line {line_num} unexpected: {lines[idx].rstrip()[:60] if idx < len(lines) else 'OOB'}")

# === FIGURE CAPTIONS ===
figure_count = 0
for idx, line in enumerate(lines):
    if "add_exam_image(story," in line and not line.strip().startswith("def "):
        figure_count += 1
        indent = line[:len(line) - len(line.lstrip())]
        insertions.append((idx, f'{indent}story.append(figure_caption(st, "\u9898\u9762\u9875"))\n'))

print(f"Found {figure_count} add_exam_image calls")

# === REFERENCES ===
ref_block = '''
    # ==================== \u53c2\u8003\u6587\u732e ====================
    story.append(Spacer(1, 8*mm))
    story.append(Paragraph("\u53c2\u8003\u6587\u732e", st['sec_title']))
    refs = [
        "1. Xilinx. 7 Series FPGAs Data Sheet: Overview (DS180).",
        "2. Xilinx. Spartan-7 FPGA Packaging and Pinout (UG475).",
        "3. \u56db\u68af\u79d1\u6280. CT137X FPGA\u7ade\u8d5b\u5b9e\u8bad\u5e73\u53f0\u7528\u6237\u624b\u518c (CT137X_UM.pdf).",
        "4. \u56db\u68af\u79d1\u6280. CT137X\u5f15\u811a\u5206\u914d\u8868 (CT137X_PIN.pdf).",
        "5. \u56db\u68af\u79d1\u6280. CT137X\u539f\u7406\u56fe (CT137X_SCH.pdf).",
        "6. Texas Instruments. ADC081C021 8-Bit ADC with ALERT Data Sheet.",
        "7. Texas Instruments. DAC5571 8-Bit DAC Data Sheet.",
        "8. Microchip. AT24C02 2Kbit EEPROM Data Sheet.",
        "9. Maxim Integrated. DS1302 Trickle Charge Timekeeping Chip Data Sheet.",
        "10. ISSI. IS63WV1288 128Kx8 Low Power SRAM Data Sheet.",
        "11. Winbond. W25Q128FV 128Mbit SPI Flash Data Sheet.",
        "12. \u84dd\u6865\u676f\u5927\u8d5b\u7ec4\u59d4\u4f1a. \u7b2c16/17\u5c4a\u84dd\u6865\u676fFPGA\u7701\u8d5b/\u56fd\u8d5b\u771f\u9898.",
    ]
    for ref in refs:
        story.append(Paragraph(ref, st['body']))
'''

for idx, line in enumerate(lines):
    if "\u6781\u9053\u5de5\u4f5c\u5ba4" in line and "\u7248\u6743\u6240\u6709" in line:
        insertions.append((idx, ref_block))
        break

# Sort reverse to preserve line numbers
insertions.sort(key=lambda x: x[0], reverse=True)

for idx, text in insertions:
    lines.insert(idx, text)

with open(SCRIPT, "w", encoding="utf-8") as f:
    f.writelines(lines)

print(f"Applied {len(insertions)} insertions total")
print(f"  Table captions: {len(table_captions)}")
print(f"  Figure captions: {figure_count}")
print(f"  References: 1 block")
