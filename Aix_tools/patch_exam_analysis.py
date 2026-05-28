#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Patch generate_textbook_v3.py to add structured exam analysis sections."""

SCRIPT = "Aix_tools/generate_textbook_v3.py"

with open(SCRIPT, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Find the line "add_exam_training_index(story, st)" in build_chapter3
# Insert the 17th province objective analysis BEFORE the exam training index
insert_idx = None
for idx, line in enumerate(lines):
    if "add_exam_training_index(story, st)" in line and "def " not in line:
        insert_idx = idx
        break

if insert_idx is None:
    print("ERROR: Could not find add_exam_training_index call")
    exit(1)

# Build the analysis section as Python code to insert
analysis_code = '''
    # ==================== 第17届省赛客观题逐题解析 ====================
    story.append(Paragraph("第17届省赛客观题逐题解析", st['sub_title']))
    story.append(Paragraph("以下为10道客观题的正确答案和逐题分析，每题1.5分，共15分。错题不要只记选项，要回到对应章节重新理解原理。", st['body']))
    obj_qa = [
        ("01", "FPGA内部资源包含哪些", "ABCD", "FPGA四大核心资源：RAM(BRAM)、布线资源、可编程逻辑块(CLB)、可编程IO单元(IOB)。"),
        ("02", "FPGA复位电路说法", "ACD", "异步复位立即生效(A对)，但抗干扰不如同步复位(B错)；可设高低有效(C对)；同步复位需时钟沿(D对)。"),
        ("03", "SPI通信协议说法", "AB", "SPI支持全双工(A对)、有独立SCK(B对)；用CS片选而非地址(C错)；无ACK机制(D错)。"),
        ("04", "移位寄存器说法", "BCD", "移位寄存器是时序电路(A错)；可由触发器级联(B对)、实现延迟(C对)、串并转换(D对)。"),
        ("05", "差分信号线优点", "ABD", "抗共模干扰(A对)、降EMI(B对)；差分需两根线(C错)；低压高速(D对)。"),
        ("06", "RS-232串口说法", "AC", "负逻辑电平(A对)；单端信号非差分(B错)；异步无时钟(C对)；TTL需电平转换(D错)。"),
        ("07", "USB2.0 ESD防护参数", "ABC", "结电容(A)、导通电压(B)、封装寄生(C)是关键；散热功率(D)非关键。"),
        ("08", "卡诺图化简目的", "BC", "找最简表达式(B对)、减少逻辑门(C对)；与时序违例(A)和工作频率(D)无关。"),
        ("09", "I2C 400kHz发4KB需时", "B", "4096字节x9时钟/字节=36864, 36866/400kHz\\u224892ms。"),
        ("10", "仿真正常硬件偶尔死机", "CD", "电源噪声(C)和跨时钟域亚稳态(D)是常见硬件独有bug。"),
    ]
    for num, question, answer, explanation in obj_qa:
        story.append(Paragraph(f"<b>{num}. {question}</b>  \\u2192 {answer}", st['body']))
        story.append(Paragraph(explanation, st['comment']))

    # ==================== 第17届省赛设计题实现指南 ====================
    story.append(Paragraph("第17届省赛设计题实现指南", st['sub_title']))
    story.append(Paragraph("串行工序控制器：IDLE\\u2192LOAD\\u2192PROCESS\\u2192INSPECT\\u2192UNLOAD循环，支持N次循环、暂停恢复、ADC阈值检测和1kHz PWM输出。以下为关键实现要点。", st['body']))

    design_rows = [
        [Paragraph("设计要素", st['th']), Paragraph("具体要求", st['th']), Paragraph("实现抓手", st['th'])],
        [Paragraph("状态机", st['td']), Paragraph("6状态：IDLE/LOAD/PROCESS/INSPECT/UNLOAD/ERROR", st['td_l']), Paragraph("三段式FSM，跳转条件见状态表", st['td_l'])],
        [Paragraph("倒计时", st['td']), Paragraph("LOAD/UNLOAD=5秒，PROCESS/INSPECT=8秒", st['td_l']), Paragraph("50MHz计数器，状态切换时重载", st['td_l'])],
        [Paragraph("按键有效性", st['td']), Paragraph("S1/S2仅IDLE有效，S3仅工序状态有效，S4仅ERROR有效", st['td_l']), Paragraph("用state条件门控消抖后的按键脉冲", st['td_l'])],
        [Paragraph("PWM输出", st['td']), Paragraph("PROCESS: 1kHz 90%占空比；INSPECT: 1kHz 10%占空比", st['td_l']), Paragraph("50000周期计数器，比较阈值切换", st['td_l'])],
        [Paragraph("ERROR触发", st['td']), Paragraph("INSPECT中ADC<32立即跳ERROR", st['td_l']), Paragraph("在INSPECT状态内检测ADC值", st['td_l'])],
        [Paragraph("LED指示", st['td']), Paragraph("LD1-LD5各对应一个工序，LD6在ERROR时0.2s闪烁", st['td_l']), Paragraph("LD6用10M周期计数器翻转", st['td_l'])],
    ]
    t = Table(design_rows, colWidths=[2.5*cm, 5.5*cm, 6*cm])
    t.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), C['primary']), ('GRID', (0,0), (-1,-1), 0.5, C['border']),
                           ('ROWBACKGROUNDS', (0,1), (-1,-1), [white, C['card_bg']]), ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                           ('TOPPADDING', (0,0), (-1,-1), 3), ('BOTTOMPADDING', (0,0), (-1,-1), 3)]))
    story.append(table_caption(st, "17届省赛设计题关键实现要素"))
    story.append(t)

'''

# Insert the analysis code before the add_exam_training_index line
lines.insert(insert_idx, analysis_code)

with open(SCRIPT, "w", encoding="utf-8") as f:
    f.writelines(lines)

print(f"Inserted exam analysis section at line {insert_idx}")
print("Added: 17th province objective Q&A (10 questions) + design guide")
