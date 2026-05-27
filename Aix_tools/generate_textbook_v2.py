#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
蓝桥杯FPGA开发教程 - 完整版
作者: Aix，极道工作室
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor, black, white, gray, lightgrey
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Preformatted, KeepTogether, ListFlowable, ListItem,
    Flowable, Image
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def register_fonts():
    """注册字体"""
    font_dir = "E:/素材/字体/font"

    regular_path = os.path.join(font_dir, "MapleMono-NF-CN-Medium.ttf")
    if os.path.exists(regular_path):
        pdfmetrics.registerFont(TTFont("MapleMono", regular_path))

    italic_path = os.path.join(font_dir, "MapleMono-NF-CN-MediumItalic.ttf")
    if os.path.exists(italic_path):
        pdfmetrics.registerFont(TTFont("MapleMono-Italic", italic_path))

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
            except:
                pass

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

    canvas.setStrokeColor(HexColor('#1a365d'))
    canvas.setLineWidth(1.5)
    canvas.line(2*cm, A4[1] - 1.5*cm, A4[0] - 2*cm, A4[1] - 1.5*cm)

    canvas.setFont("SimHei", 9)
    canvas.setFillColor(HexColor('#1a365d'))
    canvas.drawString(2*cm, A4[1] - 1.3*cm, "蓝桥杯FPGA开发教程")

    canvas.setFont("MicrosoftYaHei", 7)
    canvas.drawRightString(A4[0] - 2*cm, A4[1] - 1.3*cm, "Aix · 极道工作室")

    canvas.setStrokeColor(HexColor('#cbd5e0'))
    canvas.setLineWidth(0.5)
    canvas.line(2*cm, 2*cm, A4[0] - 2*cm, 2*cm)

    canvas.setFont("MicrosoftYaHei", 8)
    canvas.setFillColor(HexColor('#718096'))
    canvas.drawCentredString(A4[0]/2, 1.5*cm, f"— {doc.page} —")

    canvas.restoreState()

def create_cover_page():
    """创建封面"""
    story = []

    story.append(Spacer(1, 2.5*cm))

    publisher_style = ParagraphStyle(
        'Publisher', fontName='MicrosoftYaHei', fontSize=12,
        alignment=TA_CENTER, textColor=HexColor('#718096'), spaceAfter=2*cm
    )
    story.append(Paragraph("极道工作室 出品", publisher_style))

    deco_line = ParagraphStyle(
        'DecoLine', fontName='SimHei', fontSize=16,
        alignment=TA_CENTER, textColor=HexColor('#2b6cb0'), spaceAfter=0.5*cm
    )
    story.append(Paragraph("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", deco_line))

    title_style = ParagraphStyle(
        'CoverTitle', fontName='SimHei', fontSize=36, leading=48,
        alignment=TA_CENTER, textColor=HexColor('#1a365d'), spaceAfter=0.3*cm
    )
    story.append(Paragraph("蓝桥杯FPGA", title_style))
    story.append(Paragraph("开发教程", title_style))

    subtitle_style = ParagraphStyle(
        'CoverSubtitle', fontName='SimHei', fontSize=18, leading=26,
        alignment=TA_CENTER, textColor=HexColor('#2b6cb0'), spaceAfter=0.5*cm
    )
    story.append(Paragraph("XLINX 控制模块模版与实战", subtitle_style))

    story.append(Paragraph("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", deco_line))
    story.append(Spacer(1, 1*cm))

    feature_style = ParagraphStyle(
        'Feature', fontName='MicrosoftYaHei', fontSize=11,
        alignment=TA_CENTER, textColor=HexColor('#4a5568'), spaceAfter=0.3*cm
    )
    story.append(Paragraph("DP2026 FPGA竞赛实训平台 · CT137X开发板", feature_style))
    story.append(Paragraph("配套真题解析 · 代码模块化设计 · 实战案例详解", feature_style))

    story.append(Spacer(1, 2*cm))

    author_style = ParagraphStyle(
        'Author', fontName='SimHei', fontSize=14,
        alignment=TA_CENTER, textColor=HexColor('#2d3748'), spaceAfter=0.5*cm
    )
    story.append(Paragraph("Aix  著", author_style))

    studio_style = ParagraphStyle(
        'Studio', fontName='MicrosoftYaHei', fontSize=11,
        alignment=TA_CENTER, textColor=HexColor('#718096'), spaceAfter=3*cm
    )
    story.append(Paragraph("极道工作室", studio_style))

    version_style = ParagraphStyle(
        'Version', fontName='MicrosoftYaHei', fontSize=10,
        alignment=TA_CENTER, textColor=HexColor('#a0aec0')
    )
    story.append(Paragraph("2026年5月 · V2.0", version_style))
    story.append(Paragraph("适用于第十七届蓝桥杯FPGA竞赛", version_style))

    return story

def create_preface():
    """创建前言"""
    story = []

    story.append(Spacer(1, 2*cm))

    title_style = ParagraphStyle(
        'PrefaceTitle', fontName='SimHei', fontSize=24, leading=32,
        alignment=TA_CENTER, textColor=HexColor('#1a365d'), spaceAfter=2*cm
    )
    story.append(Paragraph("前    言", title_style))

    body_style = ParagraphStyle(
        'Body', fontName='MicrosoftYaHei', fontSize=11, leading=20,
        textColor=HexColor('#2d3748'), spaceAfter=0.8*cm,
        firstLineIndent=2*cm, alignment=TA_JUSTIFY
    )

    story.append(Paragraph(
        "蓝桥杯全国软件和信息技术专业人才大赛是由工业和信息化部人才交流中心主办的全国性IT学科赛事。"
        "其中FPGA赛道作为电子类的重要赛项，要求参赛者具备扎实的数字电路设计能力和Verilog HDL编程技能。",
        body_style
    ))

    story.append(Paragraph(
        "本书专为蓝桥杯FPGA竞赛备考编写，基于DP2026 FPGA竞赛实训平台（CT137X开发板），"
        "系统整理了比赛中常用的控制模块代码。所有代码均经过实际验证，采用模块化设计思想，便于读者理解和复用。",
        body_style
    ))

    story.append(Paragraph(
        "本书特色：",
        ParagraphStyle('FeatureTitle', fontName='SimHei', fontSize=12,
                      textColor=HexColor('#1a365d'), spaceBefore=1*cm, spaceAfter=0.5*cm)
    ))

    features = [
        "1. 硬件平台详解：详细介绍CT137X开发板的硬件资源和引脚分配",
        "2. 模块化设计：每个功能模块独立封装，接口清晰，便于集成和复用",
        "3. 代码规范：遵循Verilog编码规范，注释完整，可读性强",
        "4. 实战导向：结合真题案例，讲解模块在实际项目中的应用方法",
        "5. 快速查阅：采用等宽字体排版，适合比赛时快速定位和复制代码",
    ]

    feature_style = ParagraphStyle(
        'FeatureItem', fontName='MicrosoftYaHei', fontSize=11, leading=20,
        textColor=HexColor('#4a5568'), spaceAfter=0.4*cm, leftIndent=1*cm
    )

    for feature in features:
        story.append(Paragraph(feature, feature_style))

    story.append(Spacer(1, 2*cm))

    author_style = ParagraphStyle(
        'AuthorInfo', fontName='MicrosoftYaHei', fontSize=11,
        alignment=TA_RIGHT, textColor=HexColor('#718096')
    )
    story.append(Paragraph("Aix", author_style))
    story.append(Paragraph("极道工作室", author_style))
    story.append(Paragraph("2026年5月", author_style))

    return story

def create_toc():
    """创建目录"""
    story = []

    story.append(Spacer(1, 1*cm))

    toc_title_style = ParagraphStyle(
        'TOCTitle', fontName='SimHei', fontSize=22, leading=30,
        alignment=TA_CENTER, textColor=HexColor('#1a365d'), spaceAfter=2*cm
    )
    story.append(Paragraph("目  录", toc_title_style))

    section_style = ParagraphStyle(
        'TOCSection', fontName='SimHei', fontSize=13, leading=24,
        textColor=HexColor('#1a365d'), spaceBefore=15, spaceAfter=8,
    )

    entry_style = ParagraphStyle(
        'TOCEntry', fontName='MicrosoftYaHei', fontSize=10, leading=18,
        textColor=HexColor('#4a5568'), leftIndent=1.5*cm,
    )

    # 第一部分
    story.append(Paragraph("第一部分  硬件平台与基础知识", section_style))
    story.append(Paragraph("第1章  蓝桥杯FPGA竞赛概述", entry_style))
    story.append(Paragraph("第2章  DP2026竞赛实训平台介绍", entry_style))
    story.append(Paragraph("第3章  CT137X开发板硬件资源", entry_style))
    story.append(Paragraph("第4章  引脚分配与约束文件", entry_style))
    story.append(Paragraph("第5章  Vivado开发环境", entry_style))
    story.append(Paragraph("第6章  Verilog HDL基础", entry_style))

    # 第二部分
    story.append(Paragraph("第二部分  驱动模块详解", section_style))
    story.append(Paragraph("第7章  时钟分频模块", entry_style))
    story.append(Paragraph("第8章  按键消抖模块", entry_style))
    story.append(Paragraph("第9章  LED显示模块", entry_style))
    story.append(Paragraph("第10章  数码管驱动模块", entry_style))
    story.append(Paragraph("第11章  I2C通信模块", entry_style))
    story.append(Paragraph("第12章  ADC控制模块", entry_style))
    story.append(Paragraph("第13章  DAC控制模块", entry_style))
    story.append(Paragraph("第14章  EEPROM读写模块", entry_style))
    story.append(Paragraph("第15章  UART串口模块", entry_style))
    story.append(Paragraph("第16章  SPI通信模块", entry_style))
    story.append(Paragraph("第17章  DS1302 RTC模块", entry_style))
    story.append(Paragraph("第18章  SRAM控制模块", entry_style))
    story.append(Paragraph("第19章  W25Q128 Flash模块", entry_style))

    # 第三部分
    story.append(Paragraph("第三部分  用户模块详解", section_style))
    story.append(Paragraph("第20章  LED处理模块", entry_style))
    story.append(Paragraph("第21章  按键处理模块", entry_style))
    story.append(Paragraph("第22章  数码管处理模块", entry_style))
    story.append(Paragraph("第23章  UART解析模块", entry_style))
    story.append(Paragraph("第24章  UART字符串发送模块", entry_style))
    story.append(Paragraph("第25章  DS1302测试模块", entry_style))
    story.append(Paragraph("第26章  顶层模块设计", entry_style))

    # 第四部分
    story.append(Paragraph("第四部分  实战案例", section_style))
    story.append(Paragraph("第27章  第16届国赛题目解析", entry_style))
    story.append(Paragraph("第28章  系统架构设计方法", entry_style))

    # 附录
    story.append(Paragraph("附录", section_style))
    story.append(Paragraph("附录A  完整引脚约束文件", entry_style))
    story.append(Paragraph("附录B  常用模块速查表", entry_style))
    story.append(Paragraph("附录C  数码管段码表", entry_style))

    return story

def create_chapter(title, content, has_sections=True):
    """创建章节"""
    story = []

    title_style = ParagraphStyle(
        'ChapterTitle', fontName='SimHei', fontSize=20, leading=28,
        textColor=HexColor('#1a365d'), spaceBefore=1.5*cm, spaceAfter=0.8*cm,
    )
    story.append(Paragraph(title, title_style))

    line_style = ParagraphStyle(
        'ChapterLine', fontName='SimHei', fontSize=10,
        alignment=TA_LEFT, textColor=HexColor('#2b6cb0'), spaceAfter=1*cm
    )
    story.append(Paragraph("━" * 45, line_style))

    body_style = ParagraphStyle(
        'Body', fontName='MicrosoftYaHei', fontSize=10.5, leading=18,
        textColor=HexColor('#2d3748'), spaceAfter=0.6*cm,
        firstLineIndent=2*cm, alignment=TA_JUSTIFY
    )

    section_style = ParagraphStyle(
        'Section', fontName='SimHei', fontSize=13,
        textColor=HexColor('#1a365d'), spaceBefore=1.2*cm, spaceAfter=0.6*cm,
    )

    for item in content:
        if item[0] == 'section':
            story.append(Paragraph(item[1], section_style))
        elif item[0] == 'body':
            story.append(Paragraph(item[1], body_style))
        elif item[0] == 'list':
            list_style = ParagraphStyle(
                'List', fontName='MicrosoftYaHei', fontSize=10, leading=18,
                textColor=HexColor('#4a5568'), spaceAfter=0.3*cm, leftIndent=1.5*cm
            )
            for line in item[1]:
                story.append(Paragraph(line, list_style))
        elif item[0] == 'code':
            code_style = ParagraphStyle(
                'Code', fontName='MapleMono-Italic', fontSize=8, leading=11,
                leftIndent=0, rightIndent=0, spaceAfter=0, spaceBefore=0,
            )
            story.append(Spacer(1, 0.3*cm))
            story.append(Preformatted(item[1], code_style))
            story.append(Spacer(1, 0.3*cm))

    return story

def get_module_description(filename):
    """获取模块功能描述"""
    descriptions = {
        'key_ctrl.v': '按键消抖控制模块',
        'led_display.v': 'LED显示驱动模块',
        'iic_drive.v': 'I2C底层驱动模块',
        'eeprom_read_ctrl.v': 'EEPROM读取控制模块',
        'adc_ctrl.v': 'ADC控制模块',
        'dac_ctrl.v': 'DAC控制模块',
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

def create_module_chapter(chapter_num, fname, content):
    """创建模块章节"""
    story = []

    desc = get_module_description(fname)

    title_style = ParagraphStyle(
        'ChapterTitle', fontName='SimHei', fontSize=18, leading=24,
        textColor=HexColor('#1a365d'), spaceBefore=1.5*cm, spaceAfter=0.5*cm,
    )
    story.append(Paragraph(f"第{chapter_num}章  {desc}", title_style))

    line_style = ParagraphStyle(
        'ChapterLine', fontName='SimHei', fontSize=10,
        alignment=TA_LEFT, textColor=HexColor('#2b6cb0'), spaceAfter=0.8*cm
    )
    story.append(Paragraph("━" * 45, line_style))

    # 模块概述
    section_style = ParagraphStyle(
        'Section', fontName='SimHei', fontSize=13,
        textColor=HexColor('#1a365d'), spaceBefore=1*cm, spaceAfter=0.5*cm,
    )
    story.append(Paragraph("1. 模块概述", section_style))

    body_style = ParagraphStyle(
        'Body', fontName='MicrosoftYaHei', fontSize=10, leading=18,
        textColor=HexColor('#2d3748'), spaceAfter=0.5*cm,
    )

    # 根据模块类型添加说明
    explanations = {
        'frequency_driver.v': "分频器模块是FPGA开发中最基础的模块之一。它将高频系统时钟分频为所需频率的低频时钟，为其他模块提供时钟源。\n\n【应用场景】\n• 按键消抖：需要100Hz时钟\n• 数码管扫描：需要1kHz时钟\n• LED闪烁：需要1Hz时钟\n• 串口波特率：需要特定频率时钟",
        'key_ctrl.v': "按键消抖模块用于消除机械按键的抖动，确保每次按键只产生一个有效的脉冲信号。\n\n【工作原理】\n• 输入100Hz时钟，每10ms采样一次按键状态\n• 使用两个寄存器val和old分别保存当前和上一次的按键状态\n• 通过异或运算检测状态变化\n• down输出按下脉冲，up输出释放脉冲",
        'led_display.v': "LED显示驱动模块负责将控制模式映射到实际的LED输出。\n\n【注意事项】\n• 开发板LED采用低电平点亮设计\n• 输入高电平时LED熄灭\n• 输入低电平时LED点亮",
        'seg_driver.v': "数码管驱动模块将数字转换为七段显示编码，支持0-9数字和特殊字符。\n\n【数码管类型】\n• 开发板使用共阳极数码管\n• 段码为0时对应段点亮\n• 段码为1时对应段熄灭",
        'iic_drive.v': "I2C驱动模块是最常用的通信协议模块之一，用于与EEPROM、ADC、DAC等外设通信。\n\n【I2C协议要点】\n• SCL：时钟线，由主机控制\n• SDA：数据线，双向传输\n• 起始条件：SCL高电平时SDA下降沿\n• 停止条件：SCL高电平时SDA上升沿\n• 数据在SCL低电平时变化，高电平时采样",
        'adc_ctrl.v': "ADC控制模块用于读取ADC081C021芯片的转换结果。\n\n【ADC081C021参数】\n• 分辨率：8位\n• 参考电压：3.3V\n• 器件地址：1010100\n• 量程：0-255对应0V-3.3V",
        'dac_ctrl.v': "DAC控制模块用于向DAC5571芯片写入数据，产生模拟输出。\n\n【DAC5571参数】\n• 分辨率：8位\n• 器件地址：1001100\n• 输出范围：0V-3.3V",
        'uart_tx.v': "UART发送模块实现串口数据发送功能。\n\n【串口参数】\n• 波特率：115200（默认）\n• 数据位：8位\n• 停止位：1位\n• 校验位：无",
        'uart_rx.v': "UART接收模块实现串口数据接收功能，采用两级寄存器消除亚稳态。\n\n【设计要点】\n• 使用两级同步寄存器消除亚稳态\n• 在数据位中点采样，提高可靠性\n• 状态机控制接收过程",
        'spi_master.v': "SPI主控模块用于与SPI接口的外设通信，如Flash存储器、RTC等。\n\n【SPI协议要点】\n• SCLK：时钟信号\n• MOSI：主机输出从机输入\n• MISO：主机输入从机输出\n• CS：片选信号，低电平有效",
        'ds1302_wr_drive.v': "DS1302读写驱动模块用于操作DS1302实时时钟芯片。\n\n【DS1302特点】\n• 低功耗实时时钟\n• 支持秒、分、时、日、月、星期、年\n• BCD码格式存储\n• 单线数据接口",
        'sram_ctrl.v': "SRAM控制模块用于读写IS63WV1288静态随机存储器。\n\n【IS63WV1288参数】\n• 容量：128K × 8位\n• 地址线：17位\n• 数据线：8位\n• 访问时间：10ns",
        'w25q128_ctrl.v': "W25Q128 Flash控制模块用于读写W25Q128串行Flash存储器。\n\n【W25Q128参数】\n• 容量：128Mbit（16MB）\n• 接口：SPI\n• 页大小：256字节\n• 扇区大小：4KB",
    }

    explanation = explanations.get(fname, f"{desc}是FPGA开发中常用的功能模块。详细使用方法请参考代码注释。")
    for line in explanation.split('\n'):
        story.append(Paragraph(line, body_style))

    # 端口说明
    story.append(Paragraph("2. 端口说明", section_style))

    # 代码
    story.append(Paragraph("3. 源代码", section_style))

    file_name_style = ParagraphStyle(
        'FileName', fontName='MapleMono', fontSize=10,
        textColor=HexColor('#4a5568'), spaceAfter=0.5*cm,
        backColor=HexColor('#f7fafc'), borderPadding=5,
    )
    story.append(Paragraph(f"文件名：{fname}", file_name_style))

    code_style = ParagraphStyle(
        'Code', fontName='MapleMono-Italic', fontSize=7, leading=9,
        leftIndent=0, rightIndent=0, spaceAfter=0, spaceBefore=0,
    )

    lines = content.split('\n')
    chunk_size = 55
    for i in range(0, len(lines), chunk_size):
        chunk = '\n'.join(lines[i:i+chunk_size])
        if isinstance(chunk, bytes):
            chunk = chunk.decode('utf-8')
        code = Preformatted(chunk, code_style)
        story.append(code)

    return story

def create_hardware_chapter():
    """创建硬件平台章节"""
    story = []

    title_style = ParagraphStyle(
        'ChapterTitle', fontName='SimHei', fontSize=20, leading=28,
        textColor=HexColor('#1a365d'), spaceBefore=1.5*cm, spaceAfter=0.8*cm,
    )
    story.append(Paragraph("第2章  DP2026竞赛实训平台介绍", title_style))

    line_style = ParagraphStyle(
        'ChapterLine', fontName='SimHei', fontSize=10,
        alignment=TA_LEFT, textColor=HexColor('#2b6cb0'), spaceAfter=1*cm
    )
    story.append(Paragraph("━" * 45, line_style))

    section_style = ParagraphStyle(
        'Section', fontName='SimHei', fontSize=13,
        textColor=HexColor('#1a365d'), spaceBefore=1.2*cm, spaceAfter=0.6*cm,
    )

    body_style = ParagraphStyle(
        'Body', fontName='MicrosoftYaHei', fontSize=10.5, leading=18,
        textColor=HexColor('#2d3748'), spaceAfter=0.6*cm,
        firstLineIndent=2*cm, alignment=TA_JUSTIFY
    )

    list_style = ParagraphStyle(
        'List', fontName='MicrosoftYaHei', fontSize=10, leading=18,
        textColor=HexColor('#4a5568'), spaceAfter=0.3*cm, leftIndent=2*cm
    )

    story.append(Paragraph("2.1  平台概述", section_style))
    story.append(Paragraph(
        "DP2026 FPGA竞赛实训平台是蓝桥杯FPGA赛项指定的硬件平台，采用Xilinx Spartan-7系列FPGA芯片。"
        "该平台集成了丰富的外设资源，能够满足竞赛题目的各种功能需求。",
        body_style
    ))

    story.append(Paragraph("2.2  核心器件", section_style))
    story.append(Paragraph("• FPGA芯片：XC7S6-1FTGB196（Xilinx Spartan-7系列）", list_style))
    story.append(Paragraph("• 时钟源：50MHz有源晶振", list_style))
    story.append(Paragraph("• 配置Flash：用于存储FPGA配置数据", list_style))

    story.append(Paragraph("2.3  人机交互单元", section_style))
    story.append(Paragraph("• 数码管：2个4位8段共阳极数码管（共8位）", list_style))
    story.append(Paragraph("• 按键：4个独立按键（S1-S4）+ 1个复位按键", list_style))
    story.append(Paragraph("• LED：8个用户LED指示灯", list_style))
    story.append(Paragraph("• 蜂鸣器：1个无源蜂鸣器", list_style))

    story.append(Paragraph("2.4  通信接口", section_style))
    story.append(Paragraph("• UART：通过CH340C USB转串口芯片", list_style))
    story.append(Paragraph("• I2C：连接ADC081C021、DAC5571、AT24C02", list_style))
    story.append(Paragraph("• SPI：连接W25Q128 Flash存储器", list_style))
    story.append(Paragraph("• DS1302：实时时钟芯片", list_style))

    story.append(Paragraph("2.5  存储器", section_style))
    story.append(Paragraph("• SRAM：IS63WV1288（128K × 8位）", list_style))
    story.append(Paragraph("• Flash：W25Q128（128Mbit）", list_style))
    story.append(Paragraph("• EEPROM：AT24C02（2Kbit）", list_style))

    story.append(Paragraph("2.6  扩展接口", section_style))
    story.append(Paragraph("• J5扩展口：16个IO引脚", list_style))
    story.append(Paragraph("• J1扩展口：6个IO引脚", list_style))

    return story

def create_ct137x_chapter():
    """创建CT137X开发板章节"""
    story = []

    title_style = ParagraphStyle(
        'ChapterTitle', fontName='SimHei', fontSize=20, leading=28,
        textColor=HexColor('#1a365d'), spaceBefore=1.5*cm, spaceAfter=0.8*cm,
    )
    story.append(Paragraph("第3章  CT137X开发板硬件资源", title_style))

    line_style = ParagraphStyle(
        'ChapterLine', fontName='SimHei', fontSize=10,
        alignment=TA_LEFT, textColor=HexColor('#2b6cb0'), spaceAfter=1*cm
    )
    story.append(Paragraph("━" * 45, line_style))

    section_style = ParagraphStyle(
        'Section', fontName='SimHei', fontSize=13,
        textColor=HexColor('#1a365d'), spaceBefore=1.2*cm, spaceAfter=0.6*cm,
    )

    body_style = ParagraphStyle(
        'Body', fontName='MicrosoftYaHei', fontSize=10.5, leading=18,
        textColor=HexColor('#2d3748'), spaceAfter=0.6*cm,
        firstLineIndent=2*cm, alignment=TA_JUSTIFY
    )

    story.append(Paragraph("3.1  硬件框图", section_style))
    story.append(Paragraph(
        "CT137X开发板以Xilinx Spartan-7 FPGA为核心，外围连接了丰富的外设资源。"
        "以下是开发板的硬件资源框图：",
        body_style
    ))

    # 硬件框图（文字描述）
    diagram_style = ParagraphStyle(
        'Diagram', fontName='MapleMono', fontSize=9, leading=14,
        alignment=TA_CENTER, textColor=HexColor('#2d3748'),
        backColor=HexColor('#f7fafc'), borderPadding=15,
        spaceAfter=1*cm
    )

    diagram = """
┌─────────────────────────────────────────────────────────────┐
│                      CT137X 开发板                          │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐       │
│  │ 50MHz   │  │ RESET   │  │ S1-S4   │  │ LED     │       │
│  │ 时钟源  │  │ 复位键  │  │ 用户键  │  │ x8      │       │
│  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘       │
│       │            │            │            │             │
│  ┌────┴────────────┴────────────┴────────────┴────┐        │
│  │           XC7S6-1FTGB196 (Spartan-7)           │        │
│  └────┬────────────┬────────────┬────────────┬────┘        │
│       │            │            │            │             │
│  ┌────┴────┐  ┌────┴────┐  ┌────┴────┐  ┌────┴────┐       │
│  │ 数码管  │  │ I2C总线 │  │ SPI总线 │  │ UART    │       │
│  │ 8位     │  │ADC/DAC  │  │ W25Q128 │  │ CH340C  │       │
│  └─────────┘  │EEPROM   │  └─────────┘  └─────────┘       │
│               └─────────┘                                   │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐       │
│  │ DS1302  │  │ SRAM    │  │ 蜂鸣器  │  │ 扩展口  │       │
│  │ RTC     │  │ 128Kx8  │  │         │  │ J5/J1   │       │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘       │
└─────────────────────────────────────────────────────────────┘
"""
    story.append(Paragraph(diagram, diagram_style))

    story.append(Paragraph("3.2  I2C总线设备", section_style))
    story.append(Paragraph(
        "开发板上的I2C总线连接了三个设备，它们共享SCL和SDA信号线，通过不同的器件地址区分：",
        body_style
    ))

    # I2C设备表格
    i2c_data = [
        ['设备', '器件地址', '功能', '驱动模块'],
        ['ADC081C021', '1010100', '8位ADC转换', 'adc_ctrl.v'],
        ['DAC5571', '1001100', '8位DAC输出', 'dac_ctrl.v'],
        ['AT24C02', '1010000', '2Kbit EEPROM', 'eeprom_read/write_ctrl.v'],
    ]

    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#2b6cb0')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, 0), 'SimHei'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTNAME', (0, 1), (-1, -1), 'MicrosoftYaHei'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cbd5e0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#f7fafc')]),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ])

    table = Table(i2c_data, colWidths=[3.5*cm, 3*cm, 4*cm, 5*cm])
    table.setStyle(table_style)
    story.append(table)
    story.append(Spacer(1, 1*cm))

    story.append(Paragraph("3.3  数码管显示", section_style))
    story.append(Paragraph(
        "开发板配备了2个4位8段共阳极数码管，共8位显示位置。数码管采用动态扫描方式驱动，"
        "扫描频率建议为1kHz（每位显示1ms）。",
        body_style
    ))
    story.append(Paragraph(
        "共阳极数码管的段码为低电平有效，即段码为0时对应段点亮，为1时熄灭。"
        "具体段码表请参考附录C。",
        body_style
    ))

    return story

def create_pins_chapter():
    """创建引脚分配章节"""
    story = []

    title_style = ParagraphStyle(
        'ChapterTitle', fontName='SimHei', fontSize=20, leading=28,
        textColor=HexColor('#1a365d'), spaceBefore=1.5*cm, spaceAfter=0.8*cm,
    )
    story.append(Paragraph("第4章  引脚分配与约束文件", title_style))

    line_style = ParagraphStyle(
        'ChapterLine', fontName='SimHei', fontSize=10,
        alignment=TA_LEFT, textColor=HexColor('#2b6cb0'), spaceAfter=1*cm
    )
    story.append(Paragraph("━" * 45, line_style))

    section_style = ParagraphStyle(
        'Section', fontName='SimHei', fontSize=13,
        textColor=HexColor('#1a365d'), spaceBefore=1.2*cm, spaceAfter=0.6*cm,
    )

    body_style = ParagraphStyle(
        'Body', fontName='MicrosoftYaHei', fontSize=10.5, leading=18,
        textColor=HexColor('#2d3748'), spaceAfter=0.6*cm,
        firstLineIndent=2*cm, alignment=TA_JUSTIFY
    )

    story.append(Paragraph("4.1  约束文件说明", section_style))
    story.append(Paragraph(
        "引脚约束文件（.xdc）用于指定FPGA设计中每个端口对应的物理引脚位置。"
        "在Vivado工程中，需要将约束文件添加到项目中，否则综合和实现将会失败。",
        body_style
    ))

    story.append(Paragraph("4.2  系统时钟与复位", section_style))

    # 时钟复位表格
    clk_data = [
        ['信号名', '引脚', '电平标准', '说明'],
        ['sys_clk', 'G11', 'LVCMOS33', '50MHz系统时钟'],
        ['sys_rst_n', 'B6', 'LVCMOS33', '复位按键（低电平有效）'],
    ]

    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#2b6cb0')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, 0), 'SimHei'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTNAME', (0, 1), (-1, -1), 'MapleMono'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cbd5e0')),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ])

    table = Table(clk_data, colWidths=[3*cm, 2.5*cm, 3*cm, 5*cm])
    table.setStyle(table_style)
    story.append(table)
    story.append(Spacer(1, 0.5*cm))

    story.append(Paragraph("4.3  用户按键", section_style))

    key_data = [
        ['信号名', '引脚', '说明'],
        ['key[0] (S1)', 'M5', '用户按键1'],
        ['key[1] (S2)', 'M4', '用户按键2'],
        ['key[2] (S3)', 'P5', '用户按键3'],
        ['key[3] (S4)', 'N4', '用户按键4'],
    ]

    table = Table(key_data, colWidths=[4*cm, 2.5*cm, 5*cm])
    table.setStyle(table_style)
    story.append(table)
    story.append(Spacer(1, 0.5*cm))

    story.append(Paragraph("4.4  LED指示灯", section_style))

    led_data = [
        ['信号名', '引脚', '说明'],
        ['led[0] (LD1)', 'N14', 'LED1（低电平点亮）'],
        ['led[1] (LD2)', 'M14', 'LED2'],
        ['led[2] (LD3)', 'P12', 'LED3'],
        ['led[3] (LD4)', 'P13', 'LED4'],
        ['led[4] (LD5)', 'N10', 'LED5'],
        ['led[5] (LD6)', 'N11', 'LED6'],
        ['led[6] (LD7)', 'P10', 'LED7'],
        ['led[7] (LD8)', 'P11', 'LED8'],
    ]

    table = Table(led_data, colWidths=[4*cm, 2.5*cm, 5*cm])
    table.setStyle(table_style)
    story.append(table)

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

    register_fonts()

    story = []

    # 封面
    story.extend(create_cover_page())
    story.append(PageBreak())

    # 前言
    story.extend(create_preface())
    story.append(PageBreak())

    # 目录
    story.extend(create_toc())
    story.append(PageBreak())

    # 第一部分：硬件平台与基础知识
    chapter_num = 1

    # 第1章：竞赛概述
    story.extend(create_chapter(f"第{chapter_num}章  蓝桥杯FPGA竞赛概述", [
        ('section', '1.1  赛事简介'),
        ('body', '蓝桥杯全国软件和信息技术专业人才大赛是由工业和信息化部人才交流中心主办的全国性IT学科赛事。自2010年创办以来，已成为国内规模最大的IT类专业赛事之一。'),
        ('body', 'FPGA赛道是蓝桥杯电子类的重要赛项，主要考察参赛者的数字电路设计能力和Verilog HDL编程技能。比赛通常包含基础功能实现、通信协议应用、算法设计和系统集成等内容。'),
        ('section', '1.2  竞赛要求'),
        ('list', ['• 使用大赛组委会提供的FPGA竞赛实训平台', '• 参考组委会提供的资源数据包', '• 提交完整、可编译、可综合的工程', '• 使用Verilog/VHDL代码实现功能']),
        ('section', '1.3  评分标准'),
        ('list', ['• 基本功能实现（60%）', '• 代码质量与规范（20%）', '• 创新与优化（20%）']),
    ]))
    chapter_num += 1
    story.append(PageBreak())

    # 第2章：硬件平台介绍
    story.extend(create_hardware_chapter())
    chapter_num += 1
    story.append(PageBreak())

    # 第3章：CT137X开发板
    story.extend(create_ct137x_chapter())
    chapter_num += 1
    story.append(PageBreak())

    # 第4章：引脚分配
    story.extend(create_pins_chapter())
    chapter_num += 1
    story.append(PageBreak())

    # 第5章：开发环境
    story.extend(create_chapter(f"第{chapter_num}章  Vivado开发环境", [
        ('section', '5.1  软件安装'),
        ('body', '蓝桥杯FPGA比赛使用Xilinx的Vivado开发环境。推荐使用2023.1或更新版本。安装时选择"WebPACK"版本，该版本免费且支持竞赛使用的FPGA芯片。'),
        ('section', '5.2  工程创建'),
        ('list', ['1. 打开Vivado，选择"Create Project"', '2. 输入工程名称和路径', '3. 选择"RTL Project"类型', '4. 选择FPGA型号：XC7S6-1FTGB196', '5. 添加源文件（.v）和约束文件（.xdc）']),
        ('section', '5.3  综合与实现'),
        ('list', ['1. 点击"Run Synthesis"进行综合', '2. 综合完成后点击"Run Implementation"进行实现', '3. 实现完成后点击"Generate Bitstream"生成比特流', '4. 使用Hardware Manager下载到开发板']),
        ('section', '5.4  调试技巧'),
        ('list', ['• 使用ILA（集成逻辑分析仪）进行在线调试', '• 使用VIO（虚拟IO）进行交互测试', '• 查看综合报告了解资源使用情况', '• 查看时序报告确保时序收敛']),
    ]))
    chapter_num += 1
    story.append(PageBreak())

    # 第6章：Verilog基础
    story.extend(create_chapter(f"第{chapter_num}章  Verilog HDL基础", [
        ('section', '6.1  模块结构'),
        ('body', 'Verilog程序由模块（module）组成，模块是设计的基本单位。每个模块包含端口声明、内部信号定义和逻辑描述。'),
        ('code', 'module module_name (\n    input  wire       clk,      // 时钟输入\n    input  wire       rst_n,    // 复位输入（低电平有效）\n    input  wire [7:0] data_in,  // 数据输入\n    output reg  [7:0] data_out  // 数据输出\n);\n\n    // 内部信号定义\n    reg [7:0] reg_data;\n\n    // 逻辑描述\n    always @(posedge clk or negedge rst_n) begin\n        if (!rst_n)\n            reg_data <= 8\'d0;\n        else\n            reg_data <= data_in;\n    end\n\n    assign data_out = reg_data;\n\nendmodule'),
        ('section', '6.2  数据类型'),
        ('list', ['• wire：线网类型，用于组合逻辑赋值', '• reg：寄存器类型，用于时序逻辑赋值', '• parameter：参数类型，用于定义常量', '• localparam：本地参数，模块内部使用']),
        ('section', '6.3  状态机设计'),
        ('body', '状态机是FPGA设计的核心，通常采用三段式设计方法：第一段实现状态寄存器更新，第二段实现状态转移逻辑，第三段实现输出逻辑。'),
    ]))
    chapter_num += 1
    story.append(PageBreak())

    # 第二部分：驱动模块详解
    story.extend(create_chapter("第二部分  驱动模块详解", [
        ('body', '本部分详细介绍FPGA开发中常用的驱动模块。每个模块包含功能说明、工作原理和完整源代码。'),
        ('body', '驱动模块是硬件抽象层，直接与外设硬件交互，为上层应用提供统一的接口。合理使用驱动模块可以大大简化系统设计。'),
    ]))
    story.append(PageBreak())

    # 驱动模块章节
    for idx, (fname, content) in enumerate(driver_files, 1):
        story.extend(create_module_chapter(chapter_num, fname, content))
        chapter_num += 1
        story.append(PageBreak())

    # 第三部分：用户模块详解
    story.extend(create_chapter("第三部分  用户模块详解", [
        ('body', '本部分介绍基于驱动模块构建的用户层模块。这些模块实现了更接近应用层的功能，是系统设计的核心部分。'),
        ('body', '用户模块通常调用一个或多个驱动模块，实现特定的功能逻辑。在竞赛中，选手需要根据题目要求设计用户模块。'),
    ]))
    story.append(PageBreak())

    # 用户模块章节
    for idx, (fname, content) in enumerate(user_files, 1):
        story.extend(create_module_chapter(chapter_num, fname, content))
        chapter_num += 1
        story.append(PageBreak())

    # 第四部分：实战案例
    story.extend(create_chapter("第四部分  实战案例", [
        ('body', '本部分以第16届蓝桥杯FPGA国赛题目为例，讲解如何运用本书提供的模块完成竞赛题目。'),
    ]))
    story.append(PageBreak())

    # 第27章：国赛题目解析
    story.extend(create_chapter(f"第{chapter_num}章  第16届国赛题目解析", [
        ('section', '27.1  题目要求概述'),
        ('body', '本题要求设计一个动态数据采集、处理与交互系统。通过ADC转换产生128个数字量，由按键触发数据录入与存储管理。集成多模式实时算法处理模块，支持极值统计、无损压缩、滑动平均滤波和数据归一化等算法。'),
        ('section', '27.2  功能需求分析'),
        ('list', ['• 数据录入：通过ADC采集128个数字量（0-127）', '• 算法处理：极值统计、无损压缩、滑动平均、归一化', '• 显示功能：数码管显示录入界面和结果界面', '• 串口通信：115200波特率，字符串格式输出']),
        ('section', '27.3  模块选用方案'),
        ('list', ['• adc_ctrl.v - ADC数据采集', '• key_ctrl.v + frequency_driver.v - 按键消抖', '• seg_proc.v + seg_driver.v - 数码管显示', '• uart_tx.v + uart_string_sender.v - 串口发送', '• ds1302_wr_drive.v - RTC时间获取']),
        ('section', '27.4  系统架构设计'),
        ('body', '系统采用模块化设计，顶层模块负责各子模块的实例化和互连。主要包含数据采集模块、算法处理模块、显示控制模块和串口通信模块。'),
    ]))
    chapter_num += 1

    # 附录
    story.append(PageBreak())
    story.extend(create_chapter("附录A  完整引脚约束文件", [
        ('body', '以下是CT137X开发板的完整引脚约束文件，包含所有外设的引脚定义。'),
    ]))

    # 读取并添加约束文件内容
    xdc_path = "X:/FPGA/LQBFPGA/simulated test/all_code/title/DP2026_FPGA_AMD_Xilinx/BSP/CT137X_full_template.xdc"
    if os.path.exists(xdc_path):
        with open(xdc_path, 'r', encoding='utf-8') as f:
            xdc_content = f.read()

        code_style = ParagraphStyle(
            'Code', fontName='MapleMono-Italic', fontSize=7, leading=10,
            leftIndent=0, rightIndent=0, spaceAfter=0, spaceBefore=0,
        )

        lines = xdc_content.split('\n')
        for i in range(0, len(lines), 60):
            chunk = '\n'.join(lines[i:i+60])
            story.append(Preformatted(chunk, code_style))

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

    output_path = os.path.join(results_dir, "蓝桥杯FPGA开发教程_完整版.pdf")
    generate_pdf(driver_files, user_files, output_path)

if __name__ == "__main__":
    main()