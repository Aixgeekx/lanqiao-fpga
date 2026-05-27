#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
蓝桥杯FPGA XLINX 控制模块模版 - 代码参考手册
作者: Aix，极道工作室
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor, black, white, gray, lightgrey
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Preformatted, KeepTogether, ListFlowable, ListItem
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus.tableofcontents import TableOfContents

def register_fonts():
    """注册字体"""
    font_dir = "E:/素材/字体/font"

    # 注册MapleMono常规体
    regular_path = os.path.join(font_dir, "MapleMono-NF-CN-Medium.ttf")
    if os.path.exists(regular_path):
        pdfmetrics.registerFont(TTFont("MapleMono", regular_path))
        print(f"Registered: MapleMono")

    # 注册MapleMono斜体
    italic_path = os.path.join(font_dir, "MapleMono-NF-CN-MediumItalic.ttf")
    if os.path.exists(italic_path):
        pdfmetrics.registerFont(TTFont("MapleMono-Italic", italic_path))
        print(f"Registered: MapleMono-Italic")

    # 注册中文字体
    chinese_fonts = [
        ("C:/Windows/Fonts/msyh.ttc", "MicrosoftYaHei", 0),
        ("C:/Windows/Fonts/simhei.ttf", "SimHei", 0),
    ]

    for path, name, index in chinese_fonts:
        if os.path.exists(path):
            try:
                if path.endswith('.ttc'):
                    pdfmetrics.registerFont(TTFont(name, path, subfontIndex=index))
                else:
                    pdfmetrics.registerFont(TTFont(name, path))
                print(f"Registered: {name}")
            except Exception as e:
                print(f"Failed to register {name}: {e}")

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

def create_header_footer(canvas, doc):
    """创建页眉页脚"""
    canvas.saveState()

    # 页眉装饰线
    canvas.setStrokeColor(HexColor('#1a365d'))
    canvas.setLineWidth(1.5)
    canvas.line(2*cm, A4[1] - 1.5*cm, A4[0] - 2*cm, A4[1] - 1.5*cm)

    # 页眉左侧
    canvas.setFont("SimHei", 9)
    canvas.setFillColor(HexColor('#1a365d'))
    canvas.drawString(2*cm, A4[1] - 1.3*cm, "蓝桥杯FPGA XLINX 控制模块模版")

    # 页眉右侧
    canvas.setFont("MicrosoftYaHei", 7)
    canvas.drawRightString(A4[0] - 2*cm, A4[1] - 1.3*cm, "Aix · 极道工作室")

    # 页脚
    canvas.setStrokeColor(HexColor('#cbd5e0'))
    canvas.setLineWidth(0.5)
    canvas.line(2*cm, 2*cm, A4[0] - 2*cm, 2*cm)

    canvas.setFont("MicrosoftYaHei", 8)
    canvas.setFillColor(HexColor('#718096'))
    canvas.drawCentredString(A4[0]/2, 1.5*cm, f"— {doc.page} —")

    canvas.restoreState()

def create_cover_page():
    """创建精美封面 - 小册子风格"""
    story = []

    # 顶部间距
    story.append(Spacer(1, 2*cm))

    # 出版社/工作室标识
    publisher_style = ParagraphStyle(
        'Publisher',
        fontName='MicrosoftYaHei',
        fontSize=10,
        alignment=TA_CENTER,
        textColor=HexColor('#718096'),
        spaceAfter=2*cm
    )
    story.append(Paragraph("极道工作室 出品", publisher_style))

    # 装饰线 - 上
    deco_line = ParagraphStyle(
        'DecoLine',
        fontName='SimHei',
        fontSize=16,
        alignment=TA_CENTER,
        textColor=HexColor('#2b6cb0'),
        spaceAfter=0.5*cm
    )
    story.append(Paragraph("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", deco_line))

    # 主标题
    title_style = ParagraphStyle(
        'CoverTitle',
        fontName='SimHei',
        fontSize=32,
        leading=42,
        alignment=TA_CENTER,
        textColor=HexColor('#1a365d'),
        spaceAfter=0.3*cm
    )
    story.append(Paragraph("蓝桥杯FPGA", title_style))

    # 副标题
    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        fontName='SimHei',
        fontSize=24,
        leading=32,
        alignment=TA_CENTER,
        textColor=HexColor('#2b6cb0'),
        spaceAfter=0.5*cm
    )
    story.append(Paragraph("XLINX 控制模块模版", subtitle_style))

    # 装饰线 - 下
    story.append(Paragraph("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", deco_line))

    story.append(Spacer(1, 1*cm))

    # 书籍类型
    book_type_style = ParagraphStyle(
        'BookType',
        fontName='MicrosoftYaHei',
        fontSize=14,
        alignment=TA_CENTER,
        textColor=HexColor('#4a5568'),
        spaceAfter=1.5*cm
    )
    story.append(Paragraph("代码参考手册 · 竞赛备考专用", book_type_style))

    # 作者信息框
    author_box_style = ParagraphStyle(
        'AuthorBox',
        fontName='MicrosoftYaHei',
        fontSize=11,
        alignment=TA_CENTER,
        textColor=HexColor('#2d3748'),
        backColor=HexColor('#edf2f7'),
        borderWidth=1,
        borderColor=HexColor('#cbd5e0'),
        borderPadding=15,
        spaceAfter=0.5*cm
    )
    story.append(Paragraph("作者：Aix", author_box_style))

    # 工作室信息
    studio_style = ParagraphStyle(
        'Studio',
        fontName='MicrosoftYaHei',
        fontSize=10,
        alignment=TA_CENTER,
        textColor=HexColor('#718096'),
        spaceAfter=2*cm
    )
    story.append(Paragraph("极道工作室", studio_style))

    # 底部信息
    story.append(Spacer(1, 2*cm))

    # 版本信息
    version_style = ParagraphStyle(
        'Version',
        fontName='MicrosoftYaHei',
        fontSize=9,
        alignment=TA_CENTER,
        textColor=HexColor('#a0aec0')
    )
    story.append(Paragraph("V1.0 · 2026年5月", version_style))
    story.append(Paragraph("适用于蓝桥杯 FPGA 竞赛", version_style))

    return story

def create_inner_cover():
    """创建内封面（扉页）"""
    story = []

    story.append(Spacer(1, 4*cm))

    # 书名
    title_style = ParagraphStyle(
        'InnerTitle',
        fontName='SimHei',
        fontSize=28,
        leading=36,
        alignment=TA_CENTER,
        textColor=HexColor('#1a365d'),
        spaceAfter=0.5*cm
    )
    story.append(Paragraph("蓝桥杯FPGA", title_style))
    story.append(Paragraph("XLINX 控制模块模版", title_style))

    story.append(Spacer(1, 1*cm))

    # 副标题
    subtitle_style = ParagraphStyle(
        'InnerSubtitle',
        fontName='MicrosoftYaHei',
        fontSize=14,
        alignment=TA_CENTER,
        textColor=HexColor('#4a5568'),
        spaceAfter=3*cm
    )
    story.append(Paragraph("代码参考手册", subtitle_style))

    # 作者
    author_style = ParagraphStyle(
        'InnerAuthor',
        fontName='SimHei',
        fontSize=16,
        alignment=TA_CENTER,
        textColor=HexColor('#2d3748'),
        spaceAfter=0.5*cm
    )
    story.append(Paragraph("Aix  著", author_style))

    story.append(Spacer(1, 5*cm))

    # 出版信息
    pub_style = ParagraphStyle(
        'PubInfo',
        fontName='MicrosoftYaHei',
        fontSize=10,
        alignment=TA_CENTER,
        textColor=HexColor('#718096'),
        leading=18
    )
    story.append(Paragraph("极道工作室", pub_style))
    story.append(Paragraph("JIDAO STUDIO", pub_style))

    return story

def create_toc(driver_files, user_files):
    """创建目录（带页码）"""
    story = []

    # 目录标题
    toc_title_style = ParagraphStyle(
        'TOCTitle',
        fontName='SimHei',
        fontSize=22,
        leading=30,
        alignment=TA_CENTER,
        textColor=HexColor('#1a365d'),
        spaceBefore=1*cm,
        spaceAfter=1.5*cm
    )
    story.append(Paragraph("目  录", toc_title_style))

    # 创建目录表格数据
    toc_data = []

    # 章节标题样式
    section_style = ParagraphStyle(
        'TOCSection',
        fontName='SimHei',
        fontSize=12,
        textColor=HexColor('#1a365d'),
    )

    # 文件条目样式
    entry_style = ParagraphStyle(
        'TOCEntry',
        fontName='MicrosoftYaHei',
        fontSize=10,
        textColor=HexColor('#4a5568'),
    )

    # 页码样式
    page_style = ParagraphStyle(
        'TOCPage',
        fontName='MicrosoftYaHei',
        fontSize=10,
        textColor=HexColor('#4a5568'),
        alignment=TA_RIGHT,
    )

    # 第一章 Driver模块
    toc_data.append([Paragraph("第一章  Driver 模块代码", section_style), ""])

    # 预估页码（每页约60行代码）
    page_num = 4  # 从第4页开始（封面+扉页+目录）
    for idx, (fname, content) in enumerate(driver_files, 1):
        desc = get_module_description(fname)
        lines = content.count('\n') + 1
        pages_needed = max(1, lines // 60 + 1)

        toc_data.append([
            Paragraph(f"    1.{idx}  {fname}  ——  {desc}", entry_style),
            Paragraph(f"{page_num}", page_style)
        ])
        page_num += pages_needed

    # 第二章 User模块
    toc_data.append([Paragraph("第二章  User 模块代码", section_style), ""])

    for idx, (fname, content) in enumerate(user_files, 1):
        desc = get_module_description(fname)
        lines = content.count('\n') + 1
        pages_needed = max(1, lines // 60 + 1)

        toc_data.append([
            Paragraph(f"    2.{idx}  {fname}  ——  {desc}", entry_style),
            Paragraph(f"{page_num}", page_style)
        ])
        page_num += pages_needed

    # 创建表格
    table = Table(toc_data, colWidths=[14*cm, 2*cm])
    table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LINEBELOW', (0, 0), (-1, 0), 1, HexColor('#2b6cb0')),
        ('LINEBELOW', (0, -1), (-1, -1), 1, HexColor('#cbd5e0')),
    ]))

    story.append(table)

    return story

def get_module_description(filename):
    """获取模块功能描述"""
    descriptions = {
        'key_ctrl.v': '按键消抖控制模块',
        'led_display.v': 'LED显示驱动模块',
        'iic_drive.v': 'I2C底层驱动（多字节读写）',
        'eeprom_read_ctrl.v': 'EEPROM读取控制模块',
        'adc_ctrl.v': 'ADC控制模块（I2C接口）',
        'dac_ctrl.v': 'DAC控制模块（I2C接口）',
        'eeprom_write_ctrl.v': 'EEPROM写入控制模块',
        'uart_tx.v': 'UART发送模块',
        'uart_rx.v': 'UART接收模块',
        'spi_master.v': 'SPI主控模块',
        'ds1302_wr_drive.v': 'DS1302读写驱动模块',
        'ds1302_io_convert.v': 'DS1302 IO转换模块',
        'sram_ctrl.v': 'SRAM控制器',
        'w25q128_ctrl.v': 'W25Q128 Flash控制器',
        'seg_driver.v': '数码管驱动模块',
        'frequency_driver.v': '分频器模块',
        'led_proc.v': 'LED处理逻辑模块',
        'key_proc.v': '按键处理逻辑模块',
        'uart_parser.v': 'UART数据解析模块',
        'uart_string_sender.v': 'UART字符串发送模块',
        'seg_proc.v': '数码管处理模块',
        'ds1302_test.v': 'DS1302测试模块',
        'top_board.v': '板级顶层模块',
        'top.v': '系统顶层模块',
    }
    return descriptions.get(filename, 'Verilog模块')

def create_code_section(title, files, start_idx, doc):
    """创建代码章节"""
    story = []

    # 章节标题
    section_style = ParagraphStyle(
        'SectionTitle',
        fontName='SimHei',
        fontSize=20,
        leading=28,
        textColor=HexColor('#1a365d'),
        spaceBefore=1.5*cm,
        spaceAfter=0.8*cm,
    )
    story.append(Paragraph(title, section_style))

    # 装饰线
    line_style = ParagraphStyle(
        'SectionLine',
        fontName='SimHei',
        fontSize=10,
        alignment=TA_LEFT,
        textColor=HexColor('#2b6cb0'),
        spaceAfter=1*cm
    )
    story.append(Paragraph("━" * 45, line_style))

    # 文件标题样式
    file_title_style = ParagraphStyle(
        'FileTitle',
        fontName='SimHei',
        fontSize=12,
        leading=16,
        spaceBefore=1*cm,
        spaceAfter=0.3*cm,
        textColor=HexColor('#ffffff'),
        backColor=HexColor('#2b6cb0'),
        borderWidth=0,
        borderPadding=8,
        leftIndent=5,
    )

    # 模块说明样式
    desc_style = ParagraphStyle(
        'ModuleDesc',
        fontName='MicrosoftYaHei',
        fontSize=9,
        leading=14,
        textColor=HexColor('#2d3748'),
        backColor=HexColor('#f7fafc'),
        borderWidth=1,
        borderColor=HexColor('#e2e8f0'),
        borderPadding=10,
        spaceAfter=0.5*cm,
    )

    # 代码样式
    code_style = ParagraphStyle(
        'Code',
        fontName='MapleMono-Italic',
        fontSize=7,
        leading=9,
        leftIndent=0,
        rightIndent=0,
        spaceAfter=0,
        spaceBefore=0,
    )

    for idx, (fname, content) in enumerate(files, 1):
        # 文件标题
        story.append(Paragraph(f"{start_idx}.{idx}  {fname}", file_title_style))

        # 模块说明
        desc = get_module_description(fname)
        story.append(Paragraph(f"功能说明：{desc}", desc_style))

        # 代码内容
        lines = content.split('\n')
        chunk_size = 60
        for i in range(0, len(lines), chunk_size):
            chunk = '\n'.join(lines[i:i+chunk_size])
            if isinstance(chunk, bytes):
                chunk = chunk.decode('utf-8')
            code = Preformatted(chunk, code_style)
            story.append(code)

        story.append(Spacer(1, 5*mm))

    return story

def create_appendix():
    """创建附录"""
    story = []

    story.append(PageBreak())

    # 附录标题
    title_style = ParagraphStyle(
        'AppendixTitle',
        fontName='SimHei',
        fontSize=20,
        leading=28,
        alignment=TA_CENTER,
        textColor=HexColor('#1a365d'),
        spaceBefore=2*cm,
        spaceAfter=1.5*cm
    )
    story.append(Paragraph("附    录", title_style))

    # 附录内容
    content_style = ParagraphStyle(
        'AppendixContent',
        fontName='MicrosoftYaHei',
        fontSize=11,
        leading=20,
        textColor=HexColor('#4a5568'),
        spaceAfter=0.8*cm,
        leftIndent=1*cm,
        rightIndent=1*cm
    )

    story.append(Paragraph("关于本手册", ParagraphStyle(
        'AppendixSection',
        fontName='SimHei',
        fontSize=14,
        textColor=HexColor('#2d3748'),
        spaceBefore=1*cm,
        spaceAfter=0.5*cm
    )))

    story.append(Paragraph(
        "本手册收录了蓝桥杯 FPGA 竞赛常用的 Verilog 控制模块代码，"
        "涵盖驱动层和用户层两大类共 24 个模块。所有代码均经过实际验证，"
        "可直接用于竞赛项目开发。",
        content_style
    ))

    story.append(Paragraph(
        "本手册采用 MapleMono 等宽字体排版，英文代码使用斜体显示，"
        "便于阅读和区分。适合作为竞赛备考的快速查阅参考资料。",
        content_style
    ))

    story.append(Paragraph("作者简介", ParagraphStyle(
        'AppendixSection',
        fontName='SimHei',
        fontSize=14,
        textColor=HexColor('#2d3748'),
        spaceBefore=1.5*cm,
        spaceAfter=0.5*cm
    )))

    story.append(Paragraph(
        "Aix，极道工作室创始人，专注于 FPGA 嵌入式开发与教学。"
        "拥有丰富的蓝桥杯 FPGA 竞赛指导经验，致力于为参赛选手"
        "提供高质量的学习资料和开发工具。",
        content_style
    ))

    story.append(Spacer(1, 3*cm))

    # 版权信息
    copyright_style = ParagraphStyle(
        'Copyright',
        fontName='MicrosoftYaHei',
        fontSize=9,
        alignment=TA_CENTER,
        textColor=HexColor('#a0aec0'),
        leading=16
    )
    story.append(Paragraph("© 2026 极道工作室 版权所有", copyright_style))
    story.append(Paragraph("JIDAO STUDIO", copyright_style))

    return story

def generate_pdf(driver_files, user_files, output_path):
    """生成PDF文档"""
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=1.5*cm,
        rightMargin=1.5*cm,
        topMargin=2*cm,
        bottomMargin=2.5*cm
    )

    # 注册字体
    register_fonts()

    # 构建文档内容
    story = []

    # 封面
    story.extend(create_cover_page())
    story.append(PageBreak())

    # 内封面（扉页）
    story.extend(create_inner_cover())
    story.append(PageBreak())

    # 目录
    story.extend(create_toc(driver_files, user_files))
    story.append(PageBreak())

    # 第一章: Driver模块
    story.extend(create_code_section("第一章  Driver 模块代码", driver_files, 1, doc))
    story.append(PageBreak())

    # 第二章: User模块
    story.extend(create_code_section("第二章  User 模块代码", user_files, 2, doc))

    # 附录
    story.extend(create_appendix())

    # 构建PDF
    doc.build(story, onFirstPage=create_header_footer, onLaterPages=create_header_footer)
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

    output_path = os.path.join(results_dir, "蓝桥杯FPGA_XLINX_控制模块模版.pdf")
    generate_pdf(driver_files, user_files, output_path)

if __name__ == "__main__":
    main()