#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
蓝桥杯FPGA XLINX 控制模块模版 - 教材版
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
    Flowable
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

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
    canvas.drawString(2*cm, A4[1] - 1.3*cm, "蓝桥杯FPGA开发教程")

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

class NoteBox(Flowable):
    """提示框"""
    def __init__(self, text, width=16*cm, style='note'):
        Flowable.__init__(self)
        self.text = text
        self.width = width
        self.style = style

    def draw(self):
        if self.style == 'note':
            self.canv.setFillColor(HexColor('#EBF5FB'))
            self.canv.setStrokeColor(HexColor('#3498DB'))
        elif self.style == 'tip':
            self.canv.setFillColor(HexColor('#EAFAF1'))
            self.canv.setStrokeColor(HexColor('#27AE60'))
        elif self.style == 'warning':
            self.canv.setFillColor(HexColor('#FEF9E7'))
            self.canv.setStrokeColor(HexColor('#F39C12'))

        self.canv.roundRect(0, 0, self.width, 40, 5, fill=1, stroke=1)
        self.canv.setFillColor(HexColor('#2C3E50'))
        self.canv.setFont("MicrosoftYaHei", 9)
        self.canv.drawString(10, 25, self.text)

def create_cover_page():
    """创建封面"""
    story = []

    story.append(Spacer(1, 3*cm))

    # 出版社
    publisher_style = ParagraphStyle(
        'Publisher',
        fontName='MicrosoftYaHei',
        fontSize=12,
        alignment=TA_CENTER,
        textColor=HexColor('#718096'),
        spaceAfter=2*cm
    )
    story.append(Paragraph("极道工作室 出品", publisher_style))

    # 装饰线
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
        fontSize=36,
        leading=48,
        alignment=TA_CENTER,
        textColor=HexColor('#1a365d'),
        spaceAfter=0.3*cm
    )
    story.append(Paragraph("蓝桥杯FPGA", title_style))
    story.append(Paragraph("开发教程", title_style))

    # 副标题
    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        fontName='SimHei',
        fontSize=20,
        leading=28,
        alignment=TA_CENTER,
        textColor=HexColor('#2b6cb0'),
        spaceAfter=0.5*cm
    )
    story.append(Paragraph("XLINX 控制模块模版与实战", subtitle_style))

    # 装饰线
    story.append(Paragraph("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", deco_line))

    story.append(Spacer(1, 1.5*cm))

    # 教材特色
    feature_style = ParagraphStyle(
        'Feature',
        fontName='MicrosoftYaHei',
        fontSize=11,
        alignment=TA_CENTER,
        textColor=HexColor('#4a5568'),
        spaceAfter=0.3*cm
    )
    story.append(Paragraph("配套真题解析 · 代码模块化设计 · 实战案例详解", feature_style))

    story.append(Spacer(1, 2*cm))

    # 作者信息
    author_style = ParagraphStyle(
        'Author',
        fontName='SimHei',
        fontSize=14,
        alignment=TA_CENTER,
        textColor=HexColor('#2d3748'),
        spaceAfter=0.5*cm
    )
    story.append(Paragraph("Aix  著", author_style))

    # 工作室
    studio_style = ParagraphStyle(
        'Studio',
        fontName='MicrosoftYaHei',
        fontSize=11,
        alignment=TA_CENTER,
        textColor=HexColor('#718096'),
        spaceAfter=3*cm
    )
    story.append(Paragraph("极道工作室", studio_style))

    # 版本信息
    version_style = ParagraphStyle(
        'Version',
        fontName='MicrosoftYaHei',
        fontSize=10,
        alignment=TA_CENTER,
        textColor=HexColor('#a0aec0')
    )
    story.append(Paragraph("2026年5月 · V1.0", version_style))

    return story

def create_preface():
    """创建前言"""
    story = []

    story.append(Spacer(1, 2*cm))

    # 前言标题
    title_style = ParagraphStyle(
        'PrefaceTitle',
        fontName='SimHei',
        fontSize=24,
        leading=32,
        alignment=TA_CENTER,
        textColor=HexColor('#1a365d'),
        spaceAfter=2*cm
    )
    story.append(Paragraph("前    言", title_style))

    # 正文样式
    body_style = ParagraphStyle(
        'Body',
        fontName='MicrosoftYaHei',
        fontSize=11,
        leading=20,
        textColor=HexColor('#2d3748'),
        spaceAfter=0.8*cm,
        firstLineIndent=2*cm,
        alignment=TA_JUSTIFY
    )

    story.append(Paragraph(
        "蓝桥杯全国软件和信息技术专业人才大赛是由工业和信息化部人才交流中心主办的全国性IT学科赛事。"
        "其中FPGA赛道作为电子类的重要赛项，要求参赛者具备扎实的数字电路设计能力和Verilog HDL编程技能。",
        body_style
    ))

    story.append(Paragraph(
        "本书专为蓝桥杯FPGA竞赛备考编写，系统整理了比赛中常用的控制模块代码，包括驱动层和用户层两大类。"
        "所有代码均经过实际验证，采用模块化设计思想，便于读者理解和复用。",
        body_style
    ))

    story.append(Paragraph(
        "本书特色：",
        ParagraphStyle(
            'FeatureTitle',
            fontName='SimHei',
            fontSize=12,
            textColor=HexColor('#1a365d'),
            spaceBefore=1*cm,
            spaceAfter=0.5*cm
        )
    ))

    features = [
        "1. 模块化设计：每个功能模块独立封装，接口清晰，便于集成和复用",
        "2. 代码规范：遵循Verilog编码规范，注释完整，可读性强",
        "3. 实战导向：结合真题案例，讲解模块在实际项目中的应用方法",
        "4. 快速查阅：采用等宽字体排版，适合比赛时快速定位和复制代码",
    ]

    feature_style = ParagraphStyle(
        'FeatureItem',
        fontName='MicrosoftYaHei',
        fontSize=11,
        leading=20,
        textColor=HexColor('#4a5568'),
        spaceAfter=0.4*cm,
        leftIndent=1*cm
    )

    for feature in features:
        story.append(Paragraph(feature, feature_style))

    story.append(Spacer(1, 2*cm))

    # 作者信息
    author_style = ParagraphStyle(
        'AuthorInfo',
        fontName='MicrosoftYaHei',
        fontSize=11,
        alignment=TA_RIGHT,
        textColor=HexColor('#718096')
    )
    story.append(Paragraph("Aix", author_style))
    story.append(Paragraph("极道工作室", author_style))
    story.append(Paragraph("2026年5月", author_style))

    return story

def create_toc(driver_files, user_files):
    """创建目录"""
    story = []

    story.append(Spacer(1, 1*cm))

    # 目录标题
    toc_title_style = ParagraphStyle(
        'TOCTitle',
        fontName='SimHei',
        fontSize=22,
        leading=30,
        alignment=TA_CENTER,
        textColor=HexColor('#1a365d'),
        spaceAfter=2*cm
    )
    story.append(Paragraph("目  录", toc_title_style))

    # 章节标题样式
    section_style = ParagraphStyle(
        'TOCSection',
        fontName='SimHei',
        fontSize=13,
        leading=24,
        textColor=HexColor('#1a365d'),
        spaceBefore=15,
        spaceAfter=8,
    )

    # 文件条目样式
    entry_style = ParagraphStyle(
        'TOCEntry',
        fontName='MicrosoftYaHei',
        fontSize=10,
        leading=18,
        textColor=HexColor('#4a5568'),
        leftIndent=1.5*cm,
    )

    # 第一部分：基础知识
    story.append(Paragraph("第一部分  基础知识", section_style))
    story.append(Paragraph("第1章  蓝桥杯FPGA竞赛概述", entry_style))
    story.append(Paragraph("第2章  开发环境与工具", entry_style))
    story.append(Paragraph("第3章  Verilog HDL基础", entry_style))

    # 第二部分：驱动模块
    story.append(Paragraph("第二部分  驱动模块详解", section_style))
    for idx, (fname, _) in enumerate(driver_files, 1):
        desc = get_module_description(fname)
        story.append(Paragraph(f"第{idx+3}章  {desc}", entry_style))

    # 第三部分：用户模块
    chapter_start = len(driver_files) + 4
    story.append(Paragraph("第三部分  用户模块详解", section_style))
    for idx, (fname, _) in enumerate(user_files, 1):
        desc = get_module_description(fname)
        story.append(Paragraph(f"第{chapter_start+idx-1}章  {desc}", entry_style))

    # 第四部分：实战案例
    story.append(Paragraph("第四部分  实战案例", section_style))
    story.append(Paragraph(f"第{chapter_start+len(user_files)}章  真题解析与实战", entry_style))

    # 附录
    story.append(Paragraph("附录", section_style))
    story.append(Paragraph("附录A  引脚约束文件", entry_style))
    story.append(Paragraph("附录B  常用模块速查表", entry_style))

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

def get_module_explanation(filename):
    """获取模块详细说明"""
    explanations = {
        'key_ctrl.v': """按键消抖是FPGA开发中的基础功能。由于机械按键在按下和释放时会产生抖动，直接读取会导致误触发。本模块采用边沿检测方法，通过比较当前状态和上一状态来检测按键的按下和释放动作。

【工作原理】
• 输入100Hz时钟，每10ms采样一次按键状态
• 使用两个寄存器val和old分别保存当前和上一次的按键状态
• 通过异或运算检测状态变化，与运算确定方向

【使用方法】
• 实例化模块，连接100Hz时钟和4个按键输入
• down输出表示按键按下瞬间的脉冲
• up输出表示按键释放瞬间的脉冲""",

        'led_display.v': """LED显示驱动模块负责将控制模式映射到实际的LED输出。由于开发板上的LED通常采用低电平点亮设计，需要对输入信号取反。

【工作原理】
• 输入8位LED控制模式
• 输出取反后的信号驱动LED

【使用方法】
• 直接连接led_pattern到控制逻辑
• led输出连接到板上LED引脚""",

        'iic_drive.v': """I2C驱动模块是最常用的通信协议模块之一，用于与EEPROM、ADC、DAC等外设通信。本模块支持可配置的设备地址、地址字节数和数据字节数。

【工作原理】
• 采用状态机设计，包含7个状态
• 支持标准模式(100kHz)、快速模式(400kHz)
• 通过分频计数器生成SCL时钟
• 使用三态门实现SDA双向通信

【使用方法】
• 配置P_DEVICE_ADDR为从设备地址
• 配置P_ADDR_BYTE_NUM和P_DATA_BYTE_NUM
• 通过iic_start触发传输，iic_ready指示完成""",

        'uart_tx.v': """UART发送模块实现串口数据发送功能。采用状态机设计，支持可配置波特率。

【工作原理】
• 包含空闲、起始位、数据位、停止位四个状态
• 使用波特率计数器控制发送速率
• 数据从最低位开始发送

【使用方法】
• 配置UART_BPS参数设置波特率
• 输入8位数据和有效标志
• tx_done指示发送完成""",

        'uart_rx.v': """UART接收模块实现串口数据接收功能。采用两级寄存器消除亚稳态。

【工作原理】
• 使用两级同步寄存器消除亚稳态
• 在数据位中点采样，提高可靠性
• 状态机控制接收过程

【使用方法】
• 连接rx输入信号
• po_data输出接收数据
• po_flag指示数据有效""",

        'seg_driver.v': """数码管驱动模块将数字转换为七段显示编码。支持0-9数字和特殊字符。

【工作原理】
• 使用查找表实现数字到段码的转换
• 支持小数点控制
• 位选信号控制显示位置

【使用方法】
• 输入4位数字(0-9)
• position选择显示位置
• current_dp控制小数点""",

        'frequency_driver.v': """分频器模块将高频时钟分频为低频时钟。参数化设计支持任意分频比。

【工作原理】
• 使用计数器实现分频
• 计算limit = clkbase / (2 * clkdiv)
• 计数到limit时翻转输出

【使用方法】
• clkbase输入基准频率
• clkdiv输入目标频率
• clkout输出分频后时钟""",
    }
    return explanations.get(filename, "本模块提供" + get_module_description(filename) + "功能。详细使用方法请参考代码注释。")

def create_chapter_intro(chapter_num, title, content):
    """创建章节介绍"""
    story = []

    # 章节标题
    title_style = ParagraphStyle(
        'ChapterTitle',
        fontName='SimHei',
        fontSize=20,
        leading=28,
        textColor=HexColor('#1a365d'),
        spaceBefore=1.5*cm,
        spaceAfter=0.8*cm,
    )
    story.append(Paragraph(f"第{chapter_num}章  {title}", title_style))

    # 装饰线
    line_style = ParagraphStyle(
        'ChapterLine',
        fontName='SimHei',
        fontSize=10,
        alignment=TA_LEFT,
        textColor=HexColor('#2b6cb0'),
        spaceAfter=1*cm
    )
    story.append(Paragraph("━" * 45, line_style))

    # 内容
    body_style = ParagraphStyle(
        'ChapterBody',
        fontName='MicrosoftYaHei',
        fontSize=10.5,
        leading=18,
        textColor=HexColor('#2d3748'),
        spaceAfter=0.5*cm,
        firstLineIndent=2*cm,
        alignment=TA_JUSTIFY
    )

    for paragraph in content.split('\n\n'):
        if paragraph.strip():
            story.append(Paragraph(paragraph.strip(), body_style))

    return story

def create_module_chapter(chapter_num, fname, content, explanation):
    """创建模块章节"""
    story = []

    # 章节标题
    title_style = ParagraphStyle(
        'ChapterTitle',
        fontName='SimHei',
        fontSize=18,
        leading=24,
        textColor=HexColor('#1a365d'),
        spaceBefore=1.5*cm,
        spaceAfter=0.5*cm,
    )
    story.append(Paragraph(f"第{chapter_num}章  {get_module_description(fname)}", title_style))

    # 装饰线
    line_style = ParagraphStyle(
        'ChapterLine',
        fontName='SimHei',
        fontSize=10,
        alignment=TA_LEFT,
        textColor=HexColor('#2b6cb0'),
        spaceAfter=0.8*cm
    )
    story.append(Paragraph("━" * 45, line_style))

    # 模块说明标题
    section_style = ParagraphStyle(
        'SectionTitle',
        fontName='SimHei',
        fontSize=13,
        textColor=HexColor('#1a365d'),
        spaceBefore=1*cm,
        spaceAfter=0.5*cm,
    )
    story.append(Paragraph("1. 模块说明", section_style))

    # 模块说明内容
    body_style = ParagraphStyle(
        'Body',
        fontName='MicrosoftYaHei',
        fontSize=10,
        leading=18,
        textColor=HexColor('#2d3748'),
        spaceAfter=0.3*cm,
    )

    for line in explanation.split('\n'):
        if line.strip():
            story.append(Paragraph(line.strip(), body_style))

    # 源代码标题
    story.append(Paragraph("2. 源代码", section_style))
    story.append(Paragraph(f"文件名：{fname}", ParagraphStyle(
        'FileName',
        fontName='MapleMono',
        fontSize=10,
        textColor=HexColor('#4a5568'),
        spaceAfter=0.5*cm,
        backColor=HexColor('#f7fafc'),
        borderPadding=5,
    )))

    # 代码内容
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

    lines = content.split('\n')
    chunk_size = 55
    for i in range(0, len(lines), chunk_size):
        chunk = '\n'.join(lines[i:i+chunk_size])
        if isinstance(chunk, bytes):
            chunk = chunk.decode('utf-8')
        code = Preformatted(chunk, code_style)
        story.append(code)

    return story

def create_practice_chapter():
    """创建实战案例章节"""
    story = []

    # 章节标题
    title_style = ParagraphStyle(
        'ChapterTitle',
        fontName='SimHei',
        fontSize=20,
        leading=28,
        textColor=HexColor('#1a365d'),
        spaceBefore=1.5*cm,
        spaceAfter=0.8*cm,
    )
    story.append(Paragraph("第28章  真题解析与实战", title_style))

    # 装饰线
    line_style = ParagraphStyle(
        'ChapterLine',
        fontName='SimHei',
        fontSize=10,
        alignment=TA_LEFT,
        textColor=HexColor('#2b6cb0'),
        spaceAfter=1*cm
    )
    story.append(Paragraph("━" * 45, line_style))

    # 正文
    body_style = ParagraphStyle(
        'Body',
        fontName='MicrosoftYaHei',
        fontSize=10.5,
        leading=18,
        textColor=HexColor('#2d3748'),
        spaceAfter=0.8*cm,
        firstLineIndent=2*cm,
        alignment=TA_JUSTIFY
    )

    # 国赛题目解析
    section_style = ParagraphStyle(
        'SectionTitle',
        fontName='SimHei',
        fontSize=14,
        textColor=HexColor('#1a365d'),
        spaceBefore=1.5*cm,
        spaceAfter=0.8*cm,
    )
    story.append(Paragraph("28.1  第16届蓝桥杯FPGA国赛题目解析", section_style))

    story.append(Paragraph(
        "本节以第16届蓝桥杯FPGA国赛题目为例，讲解如何运用本书提供的模块完成竞赛题目。"
        "该题目要求设计一个动态数据采集、处理与交互系统，涉及ADC采集、算法处理、数码管显示和串口通信等功能。",
        body_style
    ))

    story.append(Paragraph("一、题目要求概述", ParagraphStyle(
        'SubSection',
        fontName='SimHei',
        fontSize=12,
        textColor=HexColor('#2d3748'),
        spaceBefore=1*cm,
        spaceAfter=0.5*cm,
    )))

    requirements = [
        "• 通过ADC采集128个数字量（0-127）",
        "• 按键触发数据录入与存储管理",
        "• 支持4种算法处理：极值统计、无损压缩、滑动平均滤波、数据归一化",
        "• 数码管动态显示",
        "• 串口数据传输（115200波特率）",
    ]

    req_style = ParagraphStyle(
        'Requirement',
        fontName='MicrosoftYaHei',
        fontSize=10,
        leading=18,
        textColor=HexColor('#4a5568'),
        spaceAfter=0.3*cm,
        leftIndent=1*cm
    )

    for req in requirements:
        story.append(Paragraph(req, req_style))

    story.append(Paragraph("二、模块选用", ParagraphStyle(
        'SubSection',
        fontName='SimHei',
        fontSize=12,
        textColor=HexColor('#2d3748'),
        spaceBefore=1.5*cm,
        spaceAfter=0.8*cm,
    )))

    story.append(Paragraph(
        "根据题目要求，可以选用以下模块组合完成功能：",
        body_style
    ))

    modules = [
        "• adc_ctrl.v - ADC数据采集",
        "• key_ctrl.v - 按键消抖处理",
        "• seg_proc.v + seg_driver.v - 数码管显示",
        "• uart_tx.v + uart_string_sender.v - 串口发送",
        "• frequency_driver.v - 时钟分频",
        "• ds1302_wr_drive.v - RTC时间获取",
    ]

    for mod in modules:
        story.append(Paragraph(mod, req_style))

    story.append(Paragraph("三、系统架构设计", ParagraphStyle(
        'SubSection',
        fontName='SimHei',
        fontSize=12,
        textColor=HexColor('#2d3748'),
        spaceBefore=1.5*cm,
        spaceAfter=0.8*cm,
    )))

    story.append(Paragraph(
        "系统采用模块化设计，顶层模块负责各子模块的实例化和互连。主要包含以下子模块：",
        body_style
    ))

    story.append(Paragraph(
        "1) 数据采集模块：使用adc_ctrl获取ADC数据，通过按键触发录入",
        body_style
    ))
    story.append(Paragraph(
        "2) 算法处理模块：实现极值统计、无损压缩、滑动平均、归一化4种算法",
        body_style
    ))
    story.append(Paragraph(
        "3) 显示控制模块：管理数码管显示内容，支持录入界面和结果界面切换",
        body_style
    ))
    story.append(Paragraph(
        "4) 串口通信模块：按指定格式发送数据",
        body_style
    ))

    return story

def create_appendix_pins():
    """创建引脚约束附录"""
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
    story.append(Paragraph("附录A  引脚约束文件", title_style))

    # 说明
    body_style = ParagraphStyle(
        'Body',
        fontName='MicrosoftYaHei',
        fontSize=10.5,
        leading=18,
        textColor=HexColor('#2d3748'),
        spaceAfter=1*cm,
        firstLineIndent=2*cm,
    )
    story.append(Paragraph(
        "以下是蓝桥杯FPGA X系列（XC7S6-1FTGB196）开发板的综合约束文件，包含系统时钟、复位按键、"
        "用户按键、数码管段选和位选等引脚定义。在创建工程时，需要将此文件添加到项目中。",
        body_style
    ))

    # 读取约束文件
    xdc_path = "X:/FPGA/LQBFPGA/simulated test/all_code/真题模拟题/pins.xdc"
    if os.path.exists(xdc_path):
        with open(xdc_path, 'r', encoding='utf-8') as f:
            xdc_content = f.read()

        # 代码样式
        code_style = ParagraphStyle(
            'Code',
            fontName='MapleMono-Italic',
            fontSize=8,
            leading=11,
            leftIndent=0,
            rightIndent=0,
            spaceAfter=0,
            spaceBefore=0,
        )

        lines = xdc_content.split('\n')
        for i in range(0, len(lines), 50):
            chunk = '\n'.join(lines[i:i+50])
            code = Preformatted(chunk, code_style)
            story.append(code)

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

    # 前言
    story.extend(create_preface())
    story.append(PageBreak())

    # 目录
    story.extend(create_toc(driver_files, user_files))
    story.append(PageBreak())

    # 第一部分：基础知识介绍
    chapter_num = 1

    # 第1章：蓝桥杯FPGA竞赛概述
    story.extend(create_chapter_intro(chapter_num, "蓝桥杯FPGA竞赛概述",
        """蓝桥杯全国软件和信息技术专业人才大赛是由工业和信息化部人才交流中心主办的全国性IT学科赛事。自2010年创办以来，已成为国内规模最大的IT类专业赛事之一。

FPGA赛道是蓝桥杯电子类的重要赛项，主要考察参赛者的数字电路设计能力和Verilog HDL编程技能。比赛通常包含以下内容：

1. 基础功能实现：按照题目要求完成基本功能，如按键控制、LED显示、数码管驱动等。

2. 通信协议应用：使用UART、SPI、I2C等通信协议与外设交互。

3. 算法设计：实现数据处理算法，如滤波、统计、压缩等。

4. 系统集成：将多个模块整合为完整的系统，实现复杂功能。

本书提供的代码模块覆盖了比赛常用的功能模块，读者可以直接使用或根据需要修改。"""))
    chapter_num += 1
    story.append(PageBreak())

    # 第2章：开发环境
    story.extend(create_chapter_intro(chapter_num, "开发环境与工具",
        """蓝桥杯FPGA比赛使用Xilinx的Vivado开发环境。以下是开发环境的基本配置：

1. 软件安装
• 下载并安装Xilinx Vivado（推荐2023.1或更新版本）
• 安装时选择"WebPACK"版本，支持竞赛使用的FPGA芯片

2. 工程创建
• 打开Vivado，选择"Create Project"
• 选择FPGA型号：XC7S6-1FTGB196
• 添加源文件和约束文件

3. 代码编写
• 使用Vivado内置编辑器或其他文本编辑器
• 遵循Verilog编码规范
• 添加必要的注释

4. 综合与实现
• 点击"Run Synthesis"进行综合
• 点击"Run Implementation"进行实现
• 生成比特流文件

5. 下载调试
• 连接开发板
• 使用Hardware Manager下载程序
• 观察实际效果"""))
    chapter_num += 1
    story.append(PageBreak())

    # 第3章：Verilog基础
    story.extend(create_chapter_intro(chapter_num, "Verilog HDL基础",
        """Verilog HDL是FPGA开发的主要硬件描述语言。本章介绍Verilog的基本语法和常用设计模式。

1. 模块结构
Verilog程序由模块(module)组成，模块包含端口声明、内部信号和逻辑描述。

2. 数据类型
• wire：线网类型，用于组合逻辑
• reg：寄存器类型，用于时序逻辑
• parameter：参数类型，用于定义常量

3. 运算符
• 算术运算符：+、-、*、/
• 逻辑运算符：&&、||、!
• 位运算符：&、|、^、~
• 移位运算符：<<、>>

4. 时序逻辑
always @(posedge clk or negedge rst_n)是最常用的时序逻辑块，表示在时钟上升沿或复位下降沿触发。

5. 状态机设计
状态机是FPGA设计的核心，通常采用三段式：
• 第一段：状态寄存器更新
• 第二段：状态转移逻辑
• 第三段：输出逻辑

6. 模块实例化
通过模块实例化可以复用已有的设计，提高开发效率。"""))
    chapter_num += 1
    story.append(PageBreak())

    # 驱动模块章节
    story.extend(create_chapter_intro("二", "驱动模块详解",
        "本部分详细介绍FPGA开发中常用的驱动模块。每个模块包含功能说明、工作原理和使用方法。"))
    story.append(PageBreak())

    for idx, (fname, content) in enumerate(driver_files, 1):
        explanation = get_module_explanation(fname)
        story.extend(create_module_chapter(chapter_num, fname, content, explanation))
        chapter_num += 1
        story.append(PageBreak())

    # 用户模块章节
    story.extend(create_chapter_intro("三", "用户模块详解",
        "本部分介绍基于驱动模块构建的用户层模块，这些模块实现了更接近应用层的功能。"))
    story.append(PageBreak())

    for idx, (fname, content) in enumerate(user_files, 1):
        explanation = get_module_explanation(fname)
        story.extend(create_module_chapter(chapter_num, fname, content, explanation))
        chapter_num += 1
        story.append(PageBreak())

    # 实战案例
    story.extend(create_practice_chapter())
    story.append(PageBreak())

    # 附录
    story.extend(create_appendix_pins())

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

    output_path = os.path.join(results_dir, "蓝桥杯FPGA开发教程.pdf")
    generate_pdf(driver_files, user_files, output_path)

if __name__ == "__main__":
    main()