#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用reportlab生成包含driver和user文件夹中所有Verilog代码的PDF文档
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor, black, white, gray
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Preformatted, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

def find_and_register_fonts():
    """查找并注册中文字体，返回可用的等宽字体名"""
    # 尝试注册CID字体（内置中文支持）
    try:
        pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
        print("Registered CID font: STSong-Light")
    except:
        pass

    # 尝试注册TrueType字体
    font_configs = [
        ("C:/Windows/Fonts/msyh.ttc", "MicrosoftYaHei", 0),      # 微软雅黑
        ("C:/Windows/Fonts/msyhbd.ttc", "MicrosoftYaHeiBold", 0), # 微软雅黑粗体
        ("C:/Windows/Fonts/simsun.ttc", "SimSun", 0),             # 宋体
        ("C:/Windows/Fonts/simhei.ttf", "SimHei", 0),             # 黑体
        ("C:/Windows/Fonts/simkai.ttf", "SimKai", 0),             # 楷体
        ("C:/Windows/Fonts/simfang.ttf", "FangSong", 0),          # 仿宋
        ("C:/Windows/Fonts/consola.ttf", "Consolas", 0),          # Consolas等宽
    ]

    registered_fonts = {}
    for path, name, index in font_configs:
        if os.path.exists(path):
            try:
                if path.endswith('.ttc'):
                    pdfmetrics.registerFont(TTFont(name, path, subfontIndex=index))
                else:
                    pdfmetrics.registerFont(TTFont(name, path))
                registered_fonts[name] = True
                print(f"Registered font: {name} from {path}")
            except Exception as e:
                print(f"Failed to register {name}: {e}")

    return registered_fonts

def read_verilog_files(folder_path):
    """读取指定文件夹中的所有Verilog文件"""
    verilog_files = []
    for file in sorted(os.listdir(folder_path)):
        if file.endswith('.v'):
            file_path = os.path.join(folder_path, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            verilog_files.append((file, content))
    return verilog_files

def escape_xml(text):
    """转义XML特殊字符"""
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    text = text.replace('"', '&quot;')
    text = text.replace("'", '&apos;')
    return text

def header_footer(canvas, doc):
    """页眉页脚"""
    canvas.saveState()
    # 页眉
    canvas.setFont("Helvetica-Bold", 9)
    canvas.drawString(2*cm, A4[1] - 1.2*cm, "FPGA Verilog Code Reference")
    canvas.drawRightString(A4[0] - 2*cm, A4[1] - 1.2*cm, "Competition Quick Reference")
    canvas.setStrokeColor(HexColor('#333333'))
    canvas.line(2*cm, A4[1] - 1.4*cm, A4[0] - 2*cm, A4[1] - 1.4*cm)
    # 页脚
    canvas.setFont("Helvetica", 8)
    canvas.drawCentredString(A4[0]/2, 1*cm, f"Page {doc.page}")
    canvas.restoreState()

def generate_pdf(driver_files, user_files, output_path):
    """生成PDF文档"""
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=1.5*cm,
        rightMargin=1.5*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )

    # 注册字体
    registered_fonts = find_and_register_fonts()

    # 选择代码字体 - 优先使用支持中文的等宽字体
    # SimSun是等宽的，适合代码显示
    code_font = 'SimSun' if 'SimSun' in registered_fonts else 'Courier'
    # 标题使用黑体或微软雅黑
    title_font = 'SimHei' if 'SimHei' in registered_fonts else 'Helvetica-Bold'
    body_font = 'MicrosoftYaHei' if 'MicrosoftYaHei' in registered_fonts else 'SimSun' if 'SimSun' in registered_fonts else 'Helvetica'

    print(f"Using code font: {code_font}")
    print(f"Using title font: {title_font}")
    print(f"Using body font: {body_font}")

    # 定义样式
    styles = getSampleStyleSheet()

    # 代码样式 - 使用支持中文的等宽字体
    code_style = ParagraphStyle(
        'Code',
        parent=styles['Normal'],
        fontName=code_font,
        fontSize=7,
        leading=9,
        leftIndent=0,
        rightIndent=0,
        spaceAfter=0,
        spaceBefore=0,
    )

    # 标题样式
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontName=title_font,
        fontSize=24,
        leading=30,
        alignment=TA_CENTER,
        spaceAfter=20
    )

    # 副标题样式
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontName=body_font,
        fontSize=14,
        alignment=TA_CENTER,
        leading=18
    )

    # 文件名标题样式
    file_title_style = ParagraphStyle(
        'FileTitle',
        parent=styles['Heading2'],
        fontName=title_font,
        fontSize=12,
        leading=14,
        spaceBefore=8,
        spaceAfter=4,
        textColor=HexColor('#1a5276'),
        borderWidth=1,
        borderColor=HexColor('#1a5276'),
        borderPadding=4,
    )

    # 目录标题样式
    section_style = ParagraphStyle(
        'Section',
        parent=styles['Heading1'],
        fontName=title_font,
        fontSize=16,
        leading=20,
        spaceBefore=20,
        spaceAfter=10,
        textColor=HexColor('#0d3b66'),
    )

    # 信息样式
    info_style = ParagraphStyle(
        'Info',
        parent=styles['Normal'],
        fontName=body_font,
        fontSize=11,
        alignment=TA_CENTER,
        leading=18
    )

    # 列表样式
    list_style = ParagraphStyle(
        'List',
        parent=styles['Normal'],
        fontName=code_font,
        fontSize=9,
        leading=14,
        leftIndent=2*cm
    )

    # 列表标题样式
    list_title_style = ParagraphStyle(
        'ListTitle',
        parent=styles['Normal'],
        fontName=title_font,
        fontSize=10
    )

    # 构建文档内容
    story = []

    # ===== 封面 =====
    story.append(Spacer(1, 5*cm))
    story.append(Paragraph("FPGA Verilog 代码参考手册", title_style))
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph("比赛快速查阅版", subtitle_style))
    story.append(Spacer(1, 2*cm))

    # 统计信息
    story.append(Paragraph(f"Driver 模块: {len(driver_files)} 个文件", info_style))
    story.append(Paragraph(f"User 模块: {len(user_files)} 个文件", info_style))
    story.append(Paragraph(f"共计: {len(driver_files) + len(user_files)} 个 Verilog 文件", info_style))
    story.append(Spacer(1, 3*cm))

    # 文件列表
    story.append(Paragraph("<b>Driver 模块文件:</b>", list_title_style))
    for fname, _ in driver_files:
        story.append(Paragraph(f"  {fname}", list_style))
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph("<b>User 模块文件:</b>", list_title_style))
    for fname, _ in user_files:
        story.append(Paragraph(f"  {fname}", list_style))

    story.append(PageBreak())

    # ===== Driver 文件夹代码 =====
    story.append(Paragraph("1. Driver 模块代码", section_style))
    story.append(Spacer(1, 0.3*cm))

    for idx, (fname, content) in enumerate(driver_files, 1):
        # 文件标题
        story.append(Paragraph(f"1.{idx}  {fname}", file_title_style))
        story.append(Spacer(1, 2*mm))

        # 代码内容 - 使用Preformatted保留格式
        lines = content.split('\n')
        # 每页大约能放70行代码，按段落分割避免溢出
        chunk_size = 65
        for i in range(0, len(lines), chunk_size):
            chunk = '\n'.join(lines[i:i+chunk_size])
            # 确保内容是UTF-8编码
            if isinstance(chunk, bytes):
                chunk = chunk.decode('utf-8')
            code = Preformatted(chunk, code_style)
            story.append(code)

        story.append(Spacer(1, 5*mm))

    # ===== User 文件夹代码 =====
    story.append(PageBreak())
    story.append(Paragraph("2. User 模块代码", section_style))
    story.append(Spacer(1, 0.3*cm))

    for idx, (fname, content) in enumerate(user_files, 1):
        story.append(Paragraph(f"2.{idx}  {fname}", file_title_style))
        story.append(Spacer(1, 2*mm))

        lines = content.split('\n')
        chunk_size = 65
        for i in range(0, len(lines), chunk_size):
            chunk = '\n'.join(lines[i:i+chunk_size])
            if isinstance(chunk, bytes):
                chunk = chunk.decode('utf-8')
            code = Preformatted(chunk, code_style)
            story.append(code)

        story.append(Spacer(1, 5*mm))

    # 构建PDF
    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print(f"PDF generated successfully: {output_path}")

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(script_dir)

    driver_path = os.path.join(base_dir, "driver")
    user_path = os.path.join(base_dir, "user")
    results_dir = os.path.join(base_dir, "results")
    os.makedirs(results_dir, exist_ok=True)

    print(f"Reading driver files from: {driver_path}")
    driver_files = read_verilog_files(driver_path)
    print(f"Found {len(driver_files)} Verilog files")

    print(f"Reading user files from: {user_path}")
    user_files = read_verilog_files(user_path)
    print(f"Found {len(user_files)} Verilog files")

    output_path = os.path.join(results_dir, "verilog_code_reference.pdf")
    generate_pdf(driver_files, user_files, output_path)

if __name__ == "__main__":
    main()