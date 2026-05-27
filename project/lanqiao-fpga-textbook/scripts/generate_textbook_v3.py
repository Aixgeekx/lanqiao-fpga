#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
蓝桥杯FPGA开发教程 - 详细代码注释版 + 目录页码索引 + 美化排版
作者: Aix，极道工作室
"""

import os
import re
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor, black, white
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Preformatted, KeepTogether, Flowable, Image as RLImage
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image as PILImage

# ==================== 颜色主题 ====================
C = {
    'primary':    HexColor('#1a365d'),   # 深蓝主色
    'secondary':  HexColor('#2b6cb0'),   # 中蓝
    'accent':     HexColor('#3182ce'),   # 亮蓝
    'light_bg':   HexColor('#ebf8ff'),   # 浅蓝背景
    'card_bg':    HexColor('#f7fafc'),   # 卡片背景
    'border':     HexColor('#bee3f8'),   # 边框蓝
    'text':       HexColor('#1a202c'),   # 正文黑
    'text_light': HexColor('#4a5568'),   # 副文灰
    'muted':      HexColor('#a0aec0'),   # 淡灰
    'warn_bg':    HexColor('#fffff0'),   # 警告黄背景
    'warn_border':HexColor('#ecc94b'),   # 警告黄边框
    'code_bg':    HexColor('#2d3748'),   # 代码深色背景
    'code_fg':    HexColor('#e2e8f0'),   # 代码前景色
    'comment_fg': HexColor('#63b3ed'),   # 注释蓝色
}

# ==================== 字体注册 ====================
def register_fonts():
    font_dir = "E:/素材/字体/font"
    for name, file in [("MapleMono", "MapleMono-NF-CN-Medium.ttf"),
                        ("MapleMono-Italic", "MapleMono-NF-CN-MediumItalic.ttf")]:
        p = os.path.join(font_dir, file)
        if os.path.exists(p):
            pdfmetrics.registerFont(TTFont(name, p))
    for path, name in [("C:/Windows/Fonts/simhei.ttf", "SimHei"),
                        ("C:/Windows/Fonts/msyh.ttc", "MSYH")]:
        if os.path.exists(path):
            try:
                idx = 0 if path.endswith('.ttc') else None
                pdfmetrics.registerFont(TTFont(name, path, subfontIndex=idx) if idx is not None else TTFont(name, path))
            except: pass

# ==================== 目录页码追踪 ====================
class ChapterMarker(Flowable):
    """插入章节标记，用于记录页码"""
    def __init__(self, key, chapter_map):
        Flowable.__init__(self)
        self.key = key
        self.chapter_map = chapter_map
        self.width = 0
        self.height = 0
    def draw(self):
        self.chapter_map[self.key] = self.canv.getPageNumber()

chapter_pages = {}  # 全局页码记录

# ==================== 样式定义 ====================
def S():
    s = {}
    # 封面
    s['cover_title'] = ParagraphStyle('CT', fontName='SimHei', fontSize=32, leading=44, alignment=TA_CENTER, textColor=C['primary'])
    s['cover_sub'] = ParagraphStyle('CS', fontName='SimHei', fontSize=22, leading=30, alignment=TA_CENTER, textColor=C['secondary'])
    s['cover_info'] = ParagraphStyle('CI', fontName='MSYH', fontSize=11, alignment=TA_CENTER, textColor=C['text_light'])
    # 章节标题
    s['ch_title'] = ParagraphStyle('CHT', fontName='SimHei', fontSize=22, leading=30, textColor=C['primary'], spaceBefore=5*mm, spaceAfter=3*mm)
    s['sec_title'] = ParagraphStyle('ST', fontName='SimHei', fontSize=13, leading=18, textColor=C['secondary'], spaceBefore=6*mm, spaceAfter=2*mm)
    s['sub_title'] = ParagraphStyle('SUB', fontName='SimHei', fontSize=10.5, leading=15, textColor=HexColor('#2c5282'), spaceBefore=4*mm, spaceAfter=1.5*mm)
    # 正文
    s['body'] = ParagraphStyle('BD', fontName='MSYH', fontSize=9, leading=14, textColor=C['text'], spaceAfter=2*mm)
    # 文件标题
    s['file_title'] = ParagraphStyle('FT', fontName='SimHei', fontSize=11, leading=15, textColor=white, backColor=C['secondary'], borderPadding=7, spaceBefore=6*mm, spaceAfter=2*mm)
    # 描述框
    s['desc_box'] = ParagraphStyle('DB', fontName='MSYH', fontSize=8.5, leading=13, textColor=C['text'], backColor=C['card_bg'], borderWidth=1, borderColor=C['border'], borderPadding=8, spaceAfter=2*mm)
    # 注释框
    s['comment'] = ParagraphStyle('CM', fontName='MSYH', fontSize=8, leading=12, textColor=HexColor('#2c5282'), backColor=C['light_bg'], borderWidth=0, borderPadding=6, spaceAfter=2*mm, leftIndent=8)
    # 提示框
    s['tip'] = ParagraphStyle('TP', fontName='MSYH', fontSize=8, leading=12, textColor=HexColor('#744210'), backColor=C['warn_bg'], borderWidth=1, borderColor=C['warn_border'], borderPadding=6, spaceAfter=3*mm)
    # 代码
    s['code'] = ParagraphStyle('CD', fontName='MapleMono-Italic', fontSize=6.5, leading=8.5, spaceAfter=0, spaceBefore=0, textColor=HexColor('#1a202c'))
    # 表格
    s['th'] = ParagraphStyle('TH', fontName='SimHei', fontSize=8, textColor=white, alignment=TA_CENTER)
    s['td'] = ParagraphStyle('TD', fontName='MSYH', fontSize=7.5, textColor=C['text'], alignment=TA_CENTER)
    s['td_l'] = ParagraphStyle('TDL', fontName='MSYH', fontSize=7.5, textColor=C['text'], alignment=TA_LEFT)
    s['caption'] = ParagraphStyle('CAP', fontName='MSYH', fontSize=7.5, leading=10, textColor=C['text_light'], alignment=TA_CENTER, spaceBefore=1*mm, spaceAfter=1.5*mm)
    # 目录
    s['toc_title'] = ParagraphStyle('TOCT', fontName='SimHei', fontSize=22, alignment=TA_CENTER, textColor=C['primary'], spaceBefore=8*mm, spaceAfter=8*mm)
    s['toc_ch'] = ParagraphStyle('TOCCH', fontName='SimHei', fontSize=11, textColor=C['primary'], spaceBefore=4*mm, spaceAfter=1*mm)
    s['toc_entry'] = ParagraphStyle('TOCE', fontName='MSYH', fontSize=9, textColor=C['text_light'], leftIndent=8*mm)
    s['toc_page'] = ParagraphStyle('TOCP', fontName='MSYH', fontSize=9, textColor=C['text_light'], alignment=TA_RIGHT)
    return s

# ==================== 装饰元素 ====================
class DecorLine(Flowable):
    """水平装饰线"""
    def __init__(self, width=16*cm, color=C['secondary'], thickness=1.5):
        Flowable.__init__(self)
        self.width = width
        self.height = 3*mm
        self.color = color
        self.thickness = thickness
    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(self.thickness)
        self.canv.line(0, 1.5*mm, self.width, 1.5*mm)

class ColorBar(Flowable):
    """彩色装饰条"""
    def __init__(self, width=16*cm, height=2*mm, colors=None):
        Flowable.__init__(self)
        self.width = width
        self.height = height
        self.colors = colors or [C['primary'], C['secondary'], C['accent']]
    def draw(self):
        seg = self.width / len(self.colors)
        for i, c in enumerate(self.colors):
            self.canv.setFillColor(c)
            self.canv.rect(i*seg, 0, seg+1, self.height, fill=1, stroke=0)

# ==================== 页眉页脚 ====================
def header_footer(canvas, doc):
    canvas.saveState()
    # 页眉装饰线
    canvas.setStrokeColor(C['secondary'])
    canvas.setLineWidth(2)
    canvas.line(2*cm, A4[1]-1.4*cm, A4[0]-2*cm, A4[1]-1.4*cm)
    # 页眉文字
    canvas.setFont("SimHei", 8)
    canvas.setFillColor(C['primary'])
    canvas.drawString(2*cm, A4[1]-1.2*cm, "蓝桥杯FPGA开发教程")
    canvas.setFont("MSYH", 7)
    canvas.setFillColor(C['muted'])
    canvas.drawRightString(A4[0]-2*cm, A4[1]-1.2*cm, "Aix · 极道工作室")
    # 页脚
    canvas.setStrokeColor(C['border'])
    canvas.setLineWidth(0.8)
    canvas.line(2*cm, 2*cm, A4[0]-2*cm, 2*cm)
    # 页码居中
    canvas.setFont("SimHei", 9)
    canvas.setFillColor(C['secondary'])
    canvas.drawCentredString(A4[0]/2, 1.4*cm, f"— {doc.page} —")
    canvas.restoreState()

def cover_header_footer(canvas, doc):
    """封面页无页眉页脚"""
    pass

# ==================== 读取Verilog文件 ====================
MODULE_ORDER = {
    'driver': [
        'key_ctrl.v', 'led_display.v', 'frequency_driver.v', 'iic_drive.v',
        'adc_ctrl.v', 'dac_ctrl.v', 'eeprom_read_ctrl.v', 'eeprom_write_ctrl.v',
        'uart_tx.v', 'uart_rx.v', 'spi_master.v', 'ds1302_wr_drive.v',
        'ds1302_io_convert.v', 'sram_ctrl.v', 'w25q128_ctrl.v', 'seg_driver.v'
    ],
    'user': [
        'led_proc.v', 'key_proc.v', 'uart_parser.v', 'uart_string_sender.v',
        'seg_proc.v', 'ds1302_test.v', 'top_board.v', 'top.v'
    ],
}

def read_verilog(folder):
    files = []
    folder_key = os.path.basename(folder).lower()
    order = {name: idx for idx, name in enumerate(MODULE_ORDER.get(folder_key, []))}
    names = sorted(os.listdir(folder), key=lambda name: (order.get(name, 999), name))
    for f in names:
        if f.endswith('.v'):
            with open(os.path.join(folder, f), 'r', encoding='utf-8') as fh:
                files.append((f, fh.read()))
    return files

def get_module_desc(fname):
    d = {
        'key_ctrl.v': '按键消抖与边沿检测', 'led_display.v': 'LED显示取反驱动',
        'iic_drive.v': 'I2C底层多字节读写驱动', 'eeprom_read_ctrl.v': 'AT24C02 EEPROM读控制',
        'adc_ctrl.v': 'ADC081C021 ADC读取控制', 'dac_ctrl.v': 'DAC5571 DAC写入控制',
        'eeprom_write_ctrl.v': 'AT24C02 EEPROM写控制', 'uart_tx.v': 'UART串口发送模块',
        'uart_rx.v': 'UART串口接收模块', 'spi_master.v': 'SPI主控模块',
        'ds1302_wr_drive.v': 'DS1302 RTC完整读写控制', 'ds1302_io_convert.v': 'DS1302 IO与数据转换',
        'sram_ctrl.v': 'IS63WV1288 SRAM控制器', 'w25q128_ctrl.v': 'W25Q128 Flash控制器',
        'seg_driver.v': '数码管段码与位选驱动', 'frequency_driver.v': '通用分频器',
        'led_proc.v': 'LED模式控制逻辑', 'key_proc.v': '按键处理与模式切换',
        'uart_parser.v': 'UART数据解析状态机', 'uart_string_sender.v': 'UART字符串批量发送',
        'seg_proc.v': '数码管动态扫描处理', 'ds1302_test.v': 'DS1302 RTC测试控制',
        'top_board.v': '板级顶层引脚映射', 'top.v': '系统顶层功能集成',
    }
    return d.get(fname, 'Verilog模块')

# ==================== 封面 ====================
def build_cover(st):
    story = []
    story.append(Spacer(1, 2.5*cm))
    story.append(ColorBar(colors=[C['primary'], C['secondary'], C['accent'], C['secondary'], C['primary']]))
    story.append(Spacer(1, 1.5*cm))
    story.append(Paragraph("极道工作室  出品", st['cover_info']))
    story.append(Spacer(1, 2*cm))
    # 主标题
    story.append(Paragraph("蓝桥杯 FPGA", st['cover_title']))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph("开发教程", st['cover_sub']))
    story.append(Spacer(1, 8*mm))
    story.append(ColorBar(width=8*cm, colors=[C['accent'], C['secondary'], C['accent']]))
    story.append(Spacer(1, 8*mm))
    story.append(Paragraph("详细代码注释版 · 竞赛备考专用", ParagraphStyle('VT', fontName='MSYH', fontSize=13, alignment=TA_CENTER, textColor=C['text_light'])))
    story.append(Spacer(1, 1.5*cm))
    # 信息框
    box = ParagraphStyle('BOX', fontName='MSYH', fontSize=10, alignment=TA_CENTER, textColor=C['text'],
                         backColor=C['card_bg'], borderWidth=1.5, borderColor=C['border'], borderPadding=14, spaceAfter=3*mm)
    story.append(Paragraph("作者：Aix", box))
    story.append(Paragraph("极道工作室  ·  JIDAO STUDIO", st['cover_info']))
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph("基于 DP2026 竞赛实训平台", st['cover_info']))
    story.append(Paragraph("CT137X 开发板 · Xilinx Spartan-7 XC7S6", st['cover_info']))
    story.append(Spacer(1, 2*cm))
    story.append(ColorBar(colors=[C['primary'], C['secondary'], C['accent'], C['secondary'], C['primary']]))
    story.append(Spacer(1, 5*mm))
    story.append(Paragraph("V3.0 · 2026年5月", ParagraphStyle('V3', fontName='MSYH', fontSize=9, alignment=TA_CENTER, textColor=C['muted'])))
    story.append(PageBreak())
    return story

# ==================== 目录（带页码） ====================
def build_toc(st):
    story = []
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph("目    录", st['toc_title']))
    story.append(DecorLine(color=C['secondary'], thickness=2))
    story.append(Spacer(1, 5*mm))

    # TOC条目：key = chapter_pages中的key
    toc_items = [
        ("ch1",  "第一章  硬件平台概览", True),
        ("ch1_1","1.1  DP2026 FPGA竞赛实训平台", False),
        ("ch1_2","1.2  硬件资源配置", False),
        ("ch1_3","1.3  I2C设备地址表", False),
        ("ch1_4","1.4  数码管段码表", False),
        ("ch1_5","1.5  电源配置", False),
        ("ch2",  "第二章  引脚约束与配置", True),
        ("ch2_1","2.1  XDC约束文件说明", False),
        ("ch2_2","2.2  完整引脚映射表", False),
        ("ch3",  "第三章  核心原理与真题实战", True),
        ("ch3_1","3.1  数字系统设计方法", False),
        ("ch3_2","3.2  I2C/UART/SPI通信协议", False),
        ("ch3_3","3.3  板载外设时序原理", False),
        ("ch3_4","3.4  第16届国赛算法拆解", False),
        ("ch3_5","3.5  全部真题与模拟题题面", False),
        ("ch4",  "第四章  Driver 驱动模块详解", True),
        ("ch4_1","4.1   key_ctrl.v — 按键消抖", False),
        ("ch4_2","4.2   led_display.v — LED驱动", False),
        ("ch4_3","4.3   frequency_driver.v — 分频器", False),
        ("ch4_4","4.4   iic_drive.v — I2C驱动", False),
        ("ch4_5","4.5   adc_ctrl.v — ADC控制", False),
        ("ch4_6","4.6   dac_ctrl.v — DAC控制", False),
        ("ch4_7","4.7   eeprom_read_ctrl.v — EEPROM读", False),
        ("ch4_8","4.8   eeprom_write_ctrl.v — EEPROM写", False),
        ("ch4_9","4.9   uart_tx.v — 串口发送", False),
        ("ch4_10","4.10  uart_rx.v — 串口接收", False),
        ("ch4_11","4.11  spi_master.v — SPI主控", False),
        ("ch4_12","4.12  ds1302_wr_drive.v — RTC读写", False),
        ("ch4_13","4.13  ds1302_io_convert.v — RTC IO转换", False),
        ("ch4_14","4.14  sram_ctrl.v — SRAM控制", False),
        ("ch4_15","4.15  w25q128_ctrl.v — Flash控制", False),
        ("ch4_16","4.16  seg_driver.v — 数码管驱动", False),
        ("ch5",  "第五章  User 应用模块详解", True),
        ("ch5_1","5.1   led_proc.v — LED模式控制", False),
        ("ch5_2","5.2   key_proc.v — 按键处理", False),
        ("ch5_3","5.3   uart_parser.v — 串口解析", False),
        ("ch5_4","5.4   uart_string_sender.v — 串口发送", False),
        ("ch5_5","5.5   seg_proc.v — 数码管扫描", False),
        ("ch5_6","5.6   ds1302_test.v — RTC测试", False),
        ("ch5_7","5.7   top_board.v — 板级顶层", False),
        ("ch5_8","5.8   top.v — 系统顶层", False),
        ("appendix", "附录  参考表格", True),
    ]

    toc_data = []
    for key, title, is_chapter in toc_items:
        if is_chapter:
            toc_data.append([
                Paragraph(f"<b>{title}</b>", st['toc_ch']),
                Paragraph(f"<b>{chapter_pages.get(key, '…')}</b>",
                          ParagraphStyle('TCP', fontName='SimHei', fontSize=11, textColor=C['primary'], alignment=TA_RIGHT))
            ])
        else:
            toc_data.append([
                Paragraph(title, st['toc_entry']),
                Paragraph(str(chapter_pages.get(key, '…')), st['toc_page'])
            ])

    table = Table(toc_data, colWidths=[13.5*cm, 2.5*cm])
    table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LINEBELOW', (0,0), (-1,0), 0.8, C['border']),
    ]))
    story.append(table)
    story.append(PageBreak())
    return story

# ==================== 代码注释字典 ====================
def get_line_explanations(fname):
    E = {}
    if fname == 'key_ctrl.v':
        E = {
            'module key_ctrl': '▶ 模块定义：按键消抖与边沿检测。输入100Hz时钟(由frequency_divider从50MHz分频)，输出down(按下)和up(释放)单周期脉冲',
            'input  wire       clk_100': '▶ 100Hz消抖时钟：周期10ms，天然过滤机械按键抖动(通常<10ms)',
            'input  wire [3:0] key_in': '▶ 按键输入：CT137X板S1(M5)/S2(M4)/S3(P5)/S4(N4)，低电平有效',
            'output reg  [3:0] down': '▶ 按下脉冲：检测到下降沿(1→0)时输出一个时钟周期高脉冲',
            'output reg  [3:0] up': '▶ 释放脉冲：检测到上升沿(0→1)时输出一个时钟周期高脉冲',
            'reg [3:0] val': '▶ 当前采样值：每个clk_100周期锁存key_in',
            'reg [3:0] old': '▶ 上周期值：与val比较实现边沿检测',
            'val  <= 4\'b1111': '▶ 复位：假设未按下(高电平)，因按键低电平有效',
            'old <= val': '▶ 保存当前值：下一周期用于与新采样值比较',
            'val <= key_in': '▶ 采样：锁存当前按键物理电平',
            'down <= val & (val ^ old)': '▶ 下降沿检测：异或找变化位，与val相与找1→0的位(按下瞬间)',
            'up   <= ~val & (val ^ old)': '▶ 上升沿检测：异或找变化位，与~val相与找0→1的位(释放瞬间)',
        }
    elif fname == 'led_display.v':
        E = {
            'module led_display': '▶ LED驱动：CT137X板LED阳极经电阻接3.3V，FPGA输出低电平点亮，需取反',
            'led = ~led_pattern': '▶ 取反输出：逻辑1=亮 → 物理0=亮，匹配硬件电路',
        }
    elif fname == 'frequency_driver.v':
        E = {
            'module frequency_divider': '▶ 通用分频器：输入基准频率和目标频率，输出分频时钟',
            'input  wire [31:0] clkbase': '▶ 基准频率(Hz)：如50MHz传入50_000_000',
            'input  wire [31:0] clkdiv': '▶ 目标频率(Hz)：如1kHz传入1000',
            'limit = clkbase / (2 * clkdiv)': '▶ 计数上限：50MHz/(2×1kHz)=25000，每25000个时钟翻转一次',
            'clkout  <= ~clkout': '▶ 翻转输出：计到上限时翻转，产生方波',
        }
    elif fname == 'iic_drive.v':
        E = {
            'module iic_drive': '▶ I2C底层驱动：支持多字节读写，CT137X板ADC/DAC/EEPROM共用I2C总线(SCL=E11,SDA=M10)',
            'P_SYS_CLK = 28\'d50_000_000': '▶ 系统时钟50MHz(G11引脚有源晶振)',
            'P_IIC_SCL = 28\'d125_000': '▶ I2C时钟125kHz(标准100k~快速400k之间)',
            'P_DEVICE_ADDR = 7\'b1010_100': '▶ 器件地址：ADC=1010100, EEPROM=1010XXX, DAC=1001100',
            'SCL_CNT_MAX = P_SYS_CLK / P_IIC_SCL - 1': '▶ SCL分频：50MHz/125kHz-1=399，每400系统时钟一个SCL周期',
            'assign active = iic_start && iic_ready': '▶ 激活：外部请求 且 模块空闲时启动传输',
            'start_device_write = {1\'b0,P_DEVICE_ADDR,1\'b0}': '▶ 写命令拼接：起始位+7位地址+写标志(0)',
            'start_device_read = {1\'b0,P_DEVICE_ADDR,1\'b1}': '▶ 读命令拼接：起始位+7位地址+读标志(1)',
            'assign sda_in = !sda_ctrl ? iic_sda : 1\'b1': '▶ 三态门输入：sda_ctrl=0时读SDA线',
            'assign iic_sda = sda_ctrl ? sda_out : 1\'bz': '▶ 三态门输出：sda_ctrl=1时驱动SDA，否则高阻',
            'scl_nedge_flag <= (cnt_scl == 0)': '▶ SCL下降沿：计数器到0时产生',
            'scl_pedge_flag <= (cnt_scl == SCL_CNT_MAX / 2)': '▶ SCL上升沿：计数器到一半时产生',
            'w_sda_flag <= (cnt_scl == SCL_CNT_MAX / 4)': '▶ SDA写时机：SCL低电平1/4处更新数据',
            'r_sda_flag <= (cnt_scl == SCL_CNT_MAX * 3 / 4)': '▶ SDA读时机：SCL高电平3/4处采样数据',
        }
    elif fname == 'adc_ctrl.v':
        E = {
            'module adc_ctrl': '▶ ADC081C021控制：电位器RV1模拟电压→8位数字量(0-127)，I2C接口',
            'P_DEVICE_ADDR = 7\'b1010_100': '▶ ADC器件地址1010100(数据手册规定)',
            'iic_rw_flag(1\'b1)': '▶ 固定读操作：ADC只需读取转换结果',
            'assign ad_data = iic_r_data[11:4]': '▶ 提取有效位：16位原始数据取bit[11:4]作为8位输出',
        }
    elif fname == 'dac_ctrl.v':
        E = {
            'module dac_ctrl': '▶ DAC5571控制：8位数字→模拟电压，输出到D4指示灯和TP1测试点',
            'P_DEVICE_ADDR = 7\'b100_1100': '▶ DAC器件地址1001100',
            'assign iic_w_data = {4\'b0000, da_data, 4\'b0000}': '▶ 格式转换：8位数据放中间，前后补4个0，匹配DAC5571的12位格式',
        }
    elif fname == 'eeprom_read_ctrl.v':
        E = {
            'module eeprom_read_ctrl': '▶ AT24C02读控制：2Kbit(256字节)EEPROM，I2C接口，1字节地址寻址',
            'P_DEVICE_ADDR = 7\'b101_0000': '▶ EEPROM地址1010XXX，A2A1A0全接地=000',
        }
    elif fname == 'uart_tx.v':
        E = {
            'module uart_tx': '▶ UART发送：CT137X板TX→F12→CH340C→USB→电脑，115200/8N1',
            'BAUD_CNT_MAX = CLK_FREQ / UART_BPS': '▶ 波特率计数：50MHz/115200≈434，每434时钟发1位',
            'localparam IDLE': '▶ 空闲：TX保持高电平',
            'localparam START': '▶ 起始位：TX拉低1个波特率周期',
            'localparam DATA': '▶ 数据位：LSB first逐位发送8位',
            'localparam STOP': '▶ 停止位：TX拉高1个波特率周期',
            'tx <= pi_data[bit_cnt]': '▶ 位输出：bit_cnt 0→7，先发最低位',
        }
    elif fname == 'uart_rx.v':
        E = {
            'module uart_rx': '▶ UART接收：RX←E12←CH340C←USB←电脑',
            'rx_reg1 <= rx': '▶ 一级同步：将异步rx同步到系统时钟域',
            'rx_reg2 <= rx_reg1': '▶ 二级同步：消除亚稳态',
            'if (!rx_reg2)': '▶ 起始位检测：rx下降沿表示一帧开始',
            'baud_cnt == BAUD_CNT_MAX / 2 - 1': '▶ 中点采样：起始位中间确认有效，避免毛刺',
            'rx_data <= {rx_reg2, rx_data[7:1]}': '▶ 右移接收：8位全部收完后rx_data=完整数据',
        }
    elif fname == 'spi_master.v':
        E = {
            'module spi_master': '▶ SPI主控：驱动DS1302 RTC，DS1302用类SPI接口(CE高有效，与标准SPI相反)',
            'SPI_CPOL = 1\'b0': '▶ 时钟极性0：空闲时SCLK低',
            'SPI_CPHA = 1\'b0': '▶ 时钟相位0：上升沿采样，下降沿更新',
            'spi_mosi = mosi_shift[7]': '▶ MOSI：始终发移位寄存器最高位(MSB first)',
            'mosi_shift <= {mosi_shift[6:0],mosi_shift[7]}': '▶ 左移发送：每完成一位左移',
            'miso_shift <= {miso_shift[6:0],spi_miso}': '▶ 左移接收：逐位从MISO接收',
        }
    elif fname == 'ds1302_wr_drive.v':
        E = {
            'module ds1302_wr_drive': '▶ DS1302完整读写控制：一次操作可读/写全部7个时间寄存器',
            'WRITE_WP: write_addr <= 8\'h8e': '▶ 写保护解除：向0x8E写0x00关闭写保护',
            'WRITE_SEC: write_addr <= 8\'h80': '▶ 秒寄存器写地址0x80',
            'READ_SEC: read_addr <= 8\'h81': '▶ 秒寄存器读地址0x81(=写地址+1)',
        }
    elif fname == 'ds1302_io_convert.v':
        E = {
            'module ds1302_io_convert': '▶ DS1302 IO转换：①LSB↔MSB位序翻转 ②单IO↔双IO端口转换 ③CE极性转换',
            'ds1302_data = ~ds1302_io_ctrl ? ds1302_mosi : 1\'bz': '▶ 三态门：写时驱动，读时高阻',
            'ds1302_read_data <= {receive_data[0],...,receive_data[7]}': '▶ 位序翻转：SPI的MSB-first→DS1302的LSB-first',
        }
    elif fname == 'sram_ctrl.v':
        E = {
            'module sram_ctrl': '▶ IS63WV1288 SRAM：128K×8位异步SRAM，17位地址+8位数据',
            'sram_ce_n = ... ? 1\'b0 : 1\'b1': '▶ 片选：读写时拉低CE',
            'sram_oe_n = ... ? 1\'b0 : 1\'b1': '▶ 输出使能：仅读时拉低OE',
            'sram_we_n = ... ? 1\'b0 : 1\'b1': '▶ 写使能：仅写时拉低WE',
        }
    elif fname == 'w25q128_ctrl.v':
        E = {
            'module w25q128_ctrl': '▶ W25Q128 Flash：128Mbit SPI NOR Flash，支持读ID/读/写/擦除',
            'OP_READ_JEDEC_ID': '▶ 读JEDEC ID：0x9F命令，返回3字节厂商+设备ID',
            'OP_READ_BYTE': '▶ 读字节：0x03+3字节地址，返回1字节',
            'OP_WRITE_BYTE': '▶ 写字节：0x02+3字节地址+1字节数据，需先发WREN(0x06)',
            'OP_SECTOR_ERASE': '▶ 扇区擦除：0x20+3字节地址，擦除4KB',
            'S_LAUNCH_WREN': '▶ 写使能：写/擦除前必须发0x06',
            'S_LAUNCH_POLL': '▶ 轮询：读状态寄存器bit0(WIP)等待操作完成',
        }
    elif fname == 'seg_driver.v':
        E = {
            'module seg_driver': '▶ 数码管驱动：共阳极8段，段选D3-A5，位选B2-F2，低电平有效',
            'SEG_0 = 8\'b1100_0000': '▶ 数字0段码：A~F亮(0)，G灭(1)=0xC0',
            'SEG_NULL = 8\'b1111_1111': '▶ 全灭：所有段都灭=0xFF',
            'if (current_dp) segment_data[7] = 1\'b0': '▶ 小数点：bit[7]=SEGDP，0=点亮',
            'digit_sel = ~(8\'b0000_0001 << position)': '▶ 位选译码：左移后取反(COM低有效)',
        }
    elif fname == 'seg_proc.v':
        E = {
            'module seg_proc': '▶ 数码管扫描：32位数据→8位数码管，1kHz扫描(每1ms切一位)',
            'current_num = seg_number_in[(7-bits)*4+:4]': '▶ 位选择：根据扫描索引提取4位数字',
            'bits <= (bits == 3\'d7) ? 3\'d0 : bits + 3\'d1': '▶ 扫描循环：0→1→...→7→0，125Hz刷新',
        }
    elif fname == 'led_proc.v':
        E = {
            'module led_proc': '▶ LED模式控制：4种模式(左移/右移/闪烁/固定)，1Hz驱动',
            '{led_pattern[6:0], led_pattern[7]}': '▶ 左移循环：流水灯左移',
            '{led_pattern[0], led_pattern[7:1]}': '▶ 右移循环：流水灯右移',
            '~led_pattern': '▶ 闪烁：每秒取反',
            '8\'b1010_1010': '▶ 固定：奇数位亮偶数位灭',
        }
    elif fname == 'key_proc.v':
        E = {
            'module key_proc': '▶ 按键处理：集成消抖+模式切换，S1-S4分别选模式0-3',
            'frequency_divider u_frequency_divider': '▶ 分频：50MHz→100Hz供消抖',
            'key_ctrl key_ctrl_inst': '▶ 消抖实例：输出消抖后的按下脉冲',
        }
    elif fname == 'uart_parser.v':
        E = {
            'module uart_parser': '▶ 串口解析：接收\\r\\n结尾的字符串命令，解析首字符为命令码',
            'if (po_data == 8\'h0D)': '▶ 检测\\r(0x0D)',
            'if (po_data == 8\'h0A)': '▶ 检测\\n(0x0A)，\\r\\n确认命令结束',
            '"A": cmd_signal <= 8\'h01': '▶ 命令解析：A→0x01, W→0x00',
        }
    elif fname == 'uart_string_sender.v':
        E = {
            'module uart_string_sender': '▶ 串口批量发送：宽总线→逐字节UART发送，支持动态长度',
            'pi_data <= string_data[(data_length-1-cnt)*8+:8]': '▶ 字节提取：从宽总线取当前字节',
        }
    elif fname == 'ds1302_test.v':
        E = {
            'module ds1302_test': '▶ DS1302测试控制：管理RTC初始化、CH位清除、读写流程',
            'CH = read_second[7]': '▶ CH位：秒寄存器最高位，=1表示时钟暂停',
            'write_second_reg <= {1\'b0, read_second[6:0]}': '▶ 清除CH：保持秒值，最高位清零',
        }
    elif fname == 'top_board.v':
        E = {
            'module top_board': '▶ 板级顶层：CT137X物理引脚名→内部信号名映射',
            'assign sys_rst_n = ~RESET': '▶ 复位转换：板上RESET高有效→内部低有效',
            'assign key = {S4, S3, S2, S1}': '▶ 按键拼接：4个独立按键→4位总线',
            'top u_top': '▶ 实例化系统顶层：所有逻辑在top模块中',
        }
    elif fname == 'top.v':
        E = {
            'module top': '▶ 系统顶层：集成按键/LED/数码管/蜂鸣器全部功能',
            'BUZ_ACTIVE_LOW = 1\'b1': '▶ 蜂鸣器低有效(NPN三极管驱动)',
            'key_ctrl u_key': '▶ 消抖实例：S1加1/S2减1/S3切LED模式/S4切蜂鸣器模式',
            'led_proc u_led_proc': '▶ LED实例：根据led_mode控制显示模式',
            'seg_proc u_seg_proc': '▶ 数码管实例：COM1-4计数值，COM5LED模式，COM6蜂鸣器模式',
        }
    return E

def get_usage_info(fname):
    info = {
        'key_ctrl.v': "▶ 硬件：S1(M5)/S2(M4)/S3(P5)/S4(N4)，低电平有效。需先用frequency_divider分频到100Hz作为消抖时钟。",
        'led_display.v': "▶ 硬件：LD1(N14)~LD8(P11)，阳极经电阻接3.3V，FPGA输出低电平点亮。",
        'iic_drive.v': "▶ 硬件：I2C总线SCL(E11)+SDA(M10)，连接ADC(1010100)/DAC(1001100)/EEPROM(1010000)。SDA需上拉电阻(板上已集成)。",
        'adc_ctrl.v': "▶ 硬件：ADC081C021连接电位器RV1(0~3.3V)，断开R90可测外部信号。输出8位(0-127)。",
        'dac_ctrl.v': "▶ 硬件：DAC5571输出接D4指示灯和TP1测试点，断开R74可驱动外部电路。",
        'uart_tx.v': "▶ 硬件：TX→F12→CH340C→USB→电脑。电脑端串口助手设置115200/8N1。",
        'uart_rx.v': "▶ 硬件：RX←E12←CH340C←USB←电脑。两级寄存器消除亚稳态。",
        'seg_driver.v': "▶ 硬件：段选SEGA(D3)~SEGDP(A5)，位选COM1(B2)~COM8(F2)，共阳极低电平有效。",
        'sram_ctrl.v': "▶ 硬件：IS63WV1288，17位地址A0-A16，8位数据D0-D7，CE/OE/WE低有效。",
        'w25q128_ctrl.v': "▶ 硬件：CS(D12)/SCK(D13)/IO0(G14)/IO1(F14)/IO2(F13)/IO3(E13)。U3=配置Flash，U10=用户Flash。",
        'ds1302_wr_drive.v': "▶ 硬件：SCLK(A10)/CE(A12)/DATA(A13)。需配合ds1302_io_convert和spi_master使用。",
        'frequency_driver.v': "▶ 用法：frequency_divider #(.clkbase(50M), .clkdiv(100)) 产生100Hz时钟。",
    }
    return info.get(fname, "")

# ==================== 带注释代码块 ====================
def build_annotated_code(fname, content, st):
    elements = []
    explanations = get_line_explanations(fname)
    lines = content.split('\n')
    annotated = []
    for line in lines:
        stripped = line.strip()
        matched = None
        for key, exp in explanations.items():
            if key in stripped:
                matched = exp
                break
        if matched:
            annotated.append(f"// {matched}")
        annotated.append(line)

    chunk_size = 55
    for i in range(0, len(annotated), chunk_size):
        chunk = '\n'.join(annotated[i:i+chunk_size])
        elements.append(Preformatted(chunk, st['code']))
    return elements

# ==================== 硬件章节 ====================
def build_chapter1(st):
    story = []
    story.append(ChapterMarker("ch1", chapter_pages))
    story.append(Paragraph("第一章  硬件平台概览", st['ch_title']))
    story.append(DecorLine())
    story.append(Spacer(1, 3*mm))

    story.append(ChapterMarker("ch1_1", chapter_pages))
    story.append(Paragraph("1.1  DP2026 FPGA竞赛实训平台", st['sec_title']))
    story.append(Paragraph("蓝桥杯FPGA竞赛实训平台由四梯科技设计生产，基于Xilinx Spartan-7 XC7S6-1FTGB196。"
                           "芯片提供6000 Logic Cells、7500 CLB、180KB Block RAM、2个CMT、100个IO，适合中等规模设计。", st['body']))

    story.append(ChapterMarker("ch1_2", chapter_pages))
    story.append(Paragraph("1.2  硬件资源配置", st['sec_title']))

    def th(t): return Paragraph(t, st['th'])
    def td(t): return Paragraph(t, st['td'])

    hw = [
        [th("外设"), th("型号"), th("接口"), th("FPGA引脚")],
        [td("系统时钟"), td("50MHz有源晶振"), td("单端"), td("G11")],
        [td("复位按键"), td("RESET 高有效"), td("GPIO"), td("B6")],
        [td("按键S1-S4"), td("低有效"), td("GPIO"), td("M5/M4/P5/N4")],
        [td("LED LD1-LD8"), td("低电平点亮"), td("GPIO"), td("N14~P11")],
        [td("ADC"), td("ADC081C021 8位"), td("I2C"), td("SCL=E11,SDA=M10")],
        [td("DAC"), td("DAC5571 8位"), td("I2C"), td("共用I2C")],
        [td("EEPROM"), td("AT24C02 2Kbit"), td("I2C"), td("共用I2C")],
        [td("Flash"), td("W25Q128 128Mbit"), td("SPI"), td("CS=D12,SCK=D13")],
        [td("RTC"), td("DS1302"), td("类SPI"), td("SCLK=A10,CE=A12,IO=A13")],
        [td("SRAM"), td("IS63WV1288 128Kx8"), td("并口"), td("A0-A16,D0-D7")],
        [td("数码管"), td("8位共阳极8段"), td("段+位"), td("SEG=D3~A5,COM=B2~F2")],
        [td("UART"), td("CH340C USB转串口"), td("UART"), td("TX=F12,RX=E12")],
        [td("蜂鸣器"), td("无源,NPN驱动"), td("GPIO"), td("L5")],
    ]
    t = Table(hw, colWidths=[2.8*cm, 3.5*cm, 2.2*cm, 4.8*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C['primary']),
        ('TEXTCOLOR', (0,0), (-1,0), white),
        ('GRID', (0,0), (-1,-1), 0.5, C['border']),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [white, C['card_bg']]),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t)
    story.append(Spacer(1, 3*mm))

    story.append(ChapterMarker("ch1_3", chapter_pages))
    story.append(Paragraph("1.3  I2C设备地址表", st['sec_title']))
    story.append(Paragraph("ADC/DAC/EEPROM共用I2C总线(SCL=E11, SDA=M10)，通过7位器件地址区分。", st['body']))
    i2c = [
        [th("器件"), th("型号"), th("7位地址"), th("读地址"), th("写地址"), th("说明")],
        [td("ADC"), td("ADC081C021"), td("1010100"), td("0xA9"), td("0xA8"), td("8位ADC，测电位器")],
        [td("DAC"), td("DAC5571"), td("1001100"), td("0x99"), td("0x98"), td("8位DAC，模拟输出")],
        [td("EEPROM"), td("AT24C02"), td("1010000"), td("0xA1"), td("0xA0"), td("2Kbit，256字节")],
    ]
    t = Table(i2c, colWidths=[1.6*cm, 2.3*cm, 2*cm, 1.8*cm, 1.8*cm, 3.8*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C['primary']),
        ('GRID', (0,0), (-1,-1), 0.5, C['border']),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [white, C['card_bg']]),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t)

    story.append(ChapterMarker("ch1_4", chapter_pages))
    story.append(Paragraph("1.4  数码管段码表（共阳极）", st['sec_title']))
    seg = [
        [th("数字"), th("段码(二进制)"), th("十六进制"), th("点亮的段")],
        [td("0"), td("1100_0000"), td("0xC0"), td("A,B,C,D,E,F")],
        [td("1"), td("1111_1001"), td("0xF9"), td("B,C")],
        [td("2"), td("1010_0100"), td("0xA4"), td("A,B,D,E,G")],
        [td("3"), td("1011_0000"), td("0xB0"), td("A,B,C,D,G")],
        [td("4"), td("1001_1001"), td("0x99"), td("B,C,F,G")],
        [td("5"), td("1001_0010"), td("0x92"), td("A,C,D,F,G")],
        [td("6"), td("1000_0010"), td("0x82"), td("A,C,D,E,F,G")],
        [td("7"), td("1111_1000"), td("0xF8"), td("A,B,C")],
        [td("8"), td("1000_0000"), td("0x80"), td("A,B,C,D,E,F,G")],
        [td("9"), td("1001_0000"), td("0x90"), td("A,B,C,D,F,G")],
        [td("灭"), td("1111_1111"), td("0xFF"), td("无")],
    ]
    t = Table(seg, colWidths=[1.5*cm, 3.5*cm, 2.5*cm, 4.5*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C['primary']),
        ('GRID', (0,0), (-1,-1), 0.5, C['border']),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [white, C['card_bg']]),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t)

    story.append(ChapterMarker("ch1_5", chapter_pages))
    story.append(Paragraph("1.5  电源配置", st['sec_title']))
    pwr = [
        [th("电源"), th("电压"), th("说明")],
        [td("VCCINT"), td("+1.0V"), td("FPGA内核电压")],
        [td("VCCBRAM"), td("+1.0V"), td("Block RAM供电")],
        [td("VCCAUX"), td("+1.8V"), td("模拟组件电压")],
        [td("VCCO_14"), td("+3.3V"), td("Bank14 IO(RTC/LED/ADC等)")],
        [td("VCCO_34"), td("+3.3V"), td("Bank34 IO(数码管/按键/SRAM)")],
    ]
    t = Table(pwr, colWidths=[3*cm, 2*cm, 8.3*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C['primary']),
        ('GRID', (0,0), (-1,-1), 0.5, C['border']),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [white, C['card_bg']]),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t)
    story.append(Paragraph("<b>重要：</b>所有IO Bank均为3.3V，Vivado中必须设置IOSTANDARD为LVCMOS33。", st['tip']))
    story.append(PageBreak())
    return story

# ==================== 引脚约束章节 ====================
def build_chapter2(st):
    story = []
    story.append(ChapterMarker("ch2", chapter_pages))
    story.append(Paragraph("第二章  引脚约束与配置", st['ch_title']))
    story.append(DecorLine())
    story.append(Spacer(1, 3*mm))

    story.append(ChapterMarker("ch2_1", chapter_pages))
    story.append(Paragraph("2.1  XDC约束文件说明", st['sec_title']))
    story.append(Paragraph("XDC文件定义FPGA引脚物理约束。CT137X使用Spartan-7 XC7S6-1FTGB196，所有IO为LVCMOS33。", st['body']))
    xdc = """# 必须包含的基础配置
set_property CFGBVS VCCO [current_design]           # 配置Bank电压=VCCO(3.3V)
set_property CONFIG_VOLTAGE 3.3 [current_design]     # 配置电压3.3V

# 系统时钟 50MHz (G11引脚)
set_property -dict {PACKAGE_PIN G11 IOSTANDARD LVCMOS33} [get_ports {clk}]
create_clock -period 20.000 -name clk [get_ports {clk}]  # 20ns=50MHz

# 复位按键 (B6引脚，高有效！)
set_property -dict {PACKAGE_PIN B6 IOSTANDARD LVCMOS33} [get_ports {rst}]

# 用户按键 (低有效)
set_property -dict {PACKAGE_PIN M5 IOSTANDARD LVCMOS33} [get_ports {key[0]}]  # S1
set_property -dict {PACKAGE_PIN M4 IOSTANDARD LVCMOS33} [get_ports {key[1]}]  # S2"""
    story.append(Preformatted(xdc, st['code']))
    story.append(Spacer(1, 3*mm))

    story.append(ChapterMarker("ch2_2", chapter_pages))
    story.append(Paragraph("2.2  完整引脚映射表", st['sec_title']))
    def th(t): return Paragraph(t, st['th'])
    def td(t): return Paragraph(t, st['td'])
    pins = [
        [th("功能"), th("引脚"), th("FPGA"), th("功能"), th("引脚"), th("FPGA")],
        [td("S1"), td("key[0]"), td("M5"), td("LD1"), td("led[0]"), td("N14")],
        [td("S2"), td("key[1]"), td("M4"), td("LD2"), td("led[1]"), td("M14")],
        [td("S3"), td("key[2]"), td("P5"), td("LD3"), td("led[2]"), td("P12")],
        [td("S4"), td("key[3]"), td("N4"), td("LD4"), td("led[3]"), td("P13")],
        [td("UART TX"), td("uart_tx"), td("F12"), td("LD5"), td("led[4]"), td("N10")],
        [td("UART RX"), td("uart_rx"), td("E12"), td("LD6"), td("led[5]"), td("N11")],
        [td("I2C SCL"), td("scl"), td("E11"), td("LD7"), td("led[6]"), td("P10")],
        [td("I2C SDA"), td("sda"), td("M10"), td("LD8"), td("led[7]"), td("P11")],
        [td("蜂鸣器"), td("buz"), td("L5"), td("RTC SCLK"), td("rtc_sclk"), td("A10")],
        [td("RTC CE"), td("rtc_ce"), td("A12"), td("RTC DATA"), td("rtc_data"), td("A13")],
    ]
    t = Table(pins, colWidths=[1.8*cm, 1.8*cm, 1.3*cm, 1.8*cm, 1.8*cm, 1.3*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C['primary']),
        ('GRID', (0,0), (-1,-1), 0.5, C['border']),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [white, C['card_bg']]),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t)
    story.append(Paragraph("完整约束见CT137X_full_template.xdc，使用智能proc自动匹配多种端口命名。", st['tip']))
    story.append(PageBreak())
    return story

def add_paras(story, paras, st, style='body'):
    for para in paras:
        story.append(Paragraph(para, st[style]))

def safe_xml(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def exam_image_groups(base_dir):
    img_dir = os.path.join(base_dir, "真题模拟题", "extracted_images")
    if not os.path.isdir(img_dir):
        return []
    groups = {}
    for name in os.listdir(img_dir):
        if name.lower().endswith(".png"):
            key = re.sub(r"_page\d+\.png$", "", name)
            groups.setdefault(key, []).append(os.path.join(img_dir, name))
    def page_no(path):
        m = re.search(r"_page(\d+)\.png$", os.path.basename(path))
        return int(m.group(1)) if m else 0
    order = [
        "第十六届 蓝桥杯（电子类）FPGA设计与开发省赛真题",
        "十六届蓝桥杯FPGA模拟试题I",
        "十六届蓝桥杯FPGA模拟试题Ⅱ",
        "十六届蓝桥杯FPGA模拟试题Ⅲ",
        "第十七届FPGA模拟考试Ⅰ",
        "第十七届FPGA模拟考试Ⅱ",
    ]
    return [(name, sorted(groups[name], key=page_no)) for name in order if name in groups]

def add_exam_image(story, path, st):
    with PILImage.open(path) as img:
        w, h = img.size
    max_w, max_h = 16.2*cm, 21.5*cm
    scale = min(max_w / w, max_h / h)
    story.append(RLImage(path, width=w*scale, height=h*scale))
    story.append(Paragraph(os.path.basename(path), st['caption']))

# ==================== 真题实战章节 ====================
def build_chapter3(st, base_dir=None):
    story = []
    story.append(ChapterMarker("ch3", chapter_pages))
    story.append(Paragraph("第三章  核心原理与真题实战", st['ch_title']))
    story.append(DecorLine())
    story.append(Spacer(1, 3*mm))

    story.append(ChapterMarker("ch3_1", chapter_pages))
    story.append(Paragraph("3.1  数字系统设计方法", st['sec_title']))
    add_paras(story, [
        "FPGA不是按顺序执行程序的单片机，而是在芯片内部生成真实的并行数字电路。Verilog代码中的每个寄存器、组合表达式和状态机，综合后都会变成触发器、查找表、连线和片上存储资源。因此读题时不能只问“这段程序怎么跑”，而要问“这条数据通路在哪里、寄存器什么时候更新、控制信号由哪个状态产生”。",
        "竞赛工程最稳的拆法是五层：输入采样层负责按键、串口、ADC等异步或低速输入；时序控制层负责分频、计数和状态机；数据存储层负责寄存器数组、SRAM或Flash；算法层负责最大最小、滤波、压缩等计算；显示输出层负责数码管、LED和UART上报。这样拆分后，单个模块容易仿真，也便于在赛场上快速定位问题。",
        "状态机是FPGA控制逻辑的核心。三段式状态机把“当前状态寄存器”“下一状态判断”“输出控制”分开写，优点是波形清楚、组合环路风险低、综合结果稳定。Moore型状态机的输出只取决于当前状态，输出更稳；Mealy型状态机的输出同时取决于状态和输入，响应更快但更容易产生毛刺。竞赛中外设时序优先用Moore，按键触发或握手响应可适当使用Mealy。",
        "亚稳态来自跨时钟域或异步输入。例如UART_RX、按键和外部IO都不一定和50MHz系统时钟对齐，信号刚好在采样边沿附近变化时，触发器可能短时间处于不确定电平。工程上常用两级同步器：第一级承担亚稳态风险，第二级输出给后续逻辑，虽然不能把风险降为零，但能把故障概率降到工程可接受范围。",
        "机械按键不是理想开关，按下和松开时金属触点会抖动，持续时间通常为几毫秒到十几毫秒。如果直接用50MHz采样，一个按键动作可能被识别成很多次。常见做法是先分频到100Hz或50Hz，相当于每10ms或20ms采样一次；只有相邻采样值稳定变化时，才输出一个系统可识别的单周期按下脉冲。"
    ], st)
    story.append(Paragraph("三段式状态机模板", st['sub_title']))
    story.append(Preformatted("""// 1. 当前状态寄存器：只在时钟边沿更新
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) state <= IDLE;
    else        state <= next_state;
end

// 2. 下一状态组合逻辑：根据当前状态和输入决定跳转
always @(*) begin
    next_state = state;
    case (state)
        IDLE: if (start) next_state = WORK;
        WORK: if (done)  next_state = IDLE;
    endcase
end

// 3. 输出逻辑：把控制信号集中在状态含义里
always @(*) begin
    wr_en = (state == WORK);
end""", st['code']))

    story.append(ChapterMarker("ch3_2", chapter_pages))
    story.append(Paragraph("3.2  I2C/UART/SPI通信协议", st['sec_title']))
    story.append(Paragraph("I2C协议", st['sub_title']))
    add_paras(story, [
        "I2C用SCL和SDA两根线连接多个器件。两根线空闲时都被上拉为高电平，任何器件只能主动拉低，不能主动输出高电平，所以多个器件共享总线时不会直接短路。CT137X上的ADC081C021、DAC5571和AT24C02 EEPROM共用同一组I2C引脚，靠7位器件地址区分目标设备。",
        "一次I2C传输从起始条件开始：SCL保持高电平时，SDA从高变低。随后主机发送7位地址和1位读写方向位，方向位为0表示写，为1表示读。每发送8位数据后，第9个时钟是应答位，接收方把SDA拉低表示ACK；如果SDA保持高电平，则表示NACK，通常代表器件不存在、忙或不接受更多数据。",
        "I2C时序最容易错的地方是SDA变化时机。规则是：SCL高电平期间SDA必须稳定，SCL低电平期间才允许改变数据；只有起始和停止条件例外。因此驱动中通常在SCL低电平的1/4周期更新SDA，在SCL高电平的3/4周期采样SDA。"
    ], st)
    story.append(Preformatted("""I2C字节传输：
SDA: START A6 A5 A4 A3 A2 A1 A0 R/W ACK D7 ... D0 ACK STOP
SCL:       _|‾|_|‾|_|‾|_|‾|_|‾|_|‾|_|‾|_|‾|_|‾|_|‾|_
规则：SCL高电平采样，SCL低电平改变SDA。""", st['code']))
    story.append(Paragraph("UART协议", st['sub_title']))
    add_paras(story, [
        "UART是异步串口，没有专用时钟线，发送端和接收端必须约定同一个波特率。常见配置115200/8N1表示每秒115200个符号，8个数据位，无校验位，1个停止位。线路空闲为高电平，一帧数据以低电平起始位开始，随后按低位在前发送8位数据，最后用高电平停止位结束。",
        "在50MHz系统时钟下，115200波特率对应的计数值约为50_000_000 / 115200 = 434。发送模块每计满434个系统时钟切换到下一位；接收模块检测到下降沿后，先等半个波特周期在起始位中间确认，再每隔一个波特周期采样数据位，这样能避开边沿抖动。"
    ], st)
    story.append(Preformatted("""UART 8N1帧：
空闲  起始位  bit0 bit1 bit2 bit3 bit4 bit5 bit6 bit7  停止位
  1      0      LSB ---------------------------> MSB     1""", st['code']))
    story.append(Paragraph("SPI协议", st['sub_title']))
    add_paras(story, [
        "SPI是主从式同步总线，主机控制CS片选和SCLK时钟，MOSI负责主机到从机，MISO负责从机到主机。和UART不同，SPI每一位都跟随SCLK边沿移动，因此速率可以更高，时序也更直接。标准SPI在发送MOSI的同时采样MISO，所以天然支持全双工。",
        "CPOL决定SCLK空闲电平，CPHA决定第几个边沿采样。CPOL=0时空闲低，CPOL=1时空闲高；CPHA=0表示第一个有效边沿采样，CPHA=1表示第二个有效边沿采样。主从双方的CPOL/CPHA必须一致，否则会出现整体位移一位或采样到错误数据。",
        "DS1302常被称为类SPI器件，但它不是标准四线SPI：它使用CE、SCLK和单根双向DATA，且数据位序通常是LSB first。工程中可先用通用SPI主机产生时钟和移位，再通过ds1302_io_convert模块处理三态方向、CE极性和位序翻转。"
    ], st)
    spi_tbl = [[Paragraph(x, st['th']) for x in ["模式", "CPOL", "CPHA", "空闲时钟", "采样边沿"]],
               [Paragraph(x, st['td']) for x in ["0", "0", "0", "低", "第1边沿"]],
               [Paragraph(x, st['td']) for x in ["1", "0", "1", "低", "第2边沿"]],
               [Paragraph(x, st['td']) for x in ["2", "1", "0", "高", "第1边沿"]],
               [Paragraph(x, st['td']) for x in ["3", "1", "1", "高", "第2边沿"]]]
    t = Table(spi_tbl, colWidths=[2*cm, 2*cm, 2*cm, 3*cm, 3*cm])
    t.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), C['primary']), ('GRID', (0,0), (-1,-1), 0.5, C['border']),
                           ('ROWBACKGROUNDS', (0,1), (-1,-1), [white, C['card_bg']]), ('ALIGN', (0,0), (-1,-1), 'CENTER')]))
    story.append(t)

    story.append(ChapterMarker("ch3_3", chapter_pages))
    story.append(Paragraph("3.3  板载外设时序原理", st['sec_title']))
    story.append(Paragraph("数码管动态扫描", st['sub_title']))
    add_paras(story, [
        "CT137X使用8位共阳极数码管，段选和位选都是低电平有效。多位数码管不是8位同时各接一套段线，而是共用同一组段选线，再用位选逐位点亮。控制器在很短时间内依次显示第1位、第2位直到第8位，只要刷新足够快，人眼因为视觉暂留会认为所有位同时亮。",
        "如果扫描频率过低会闪烁，如果位切换前没有先关断段选，可能出现重影。常用策略是1kHz左右切位，8位平均下来每位约125Hz；每次切换时先关闭所有位选，更新段码，再打开目标位选。"
    ], st)
    story.append(Paragraph("SRAM读写时序", st['sub_title']))
    add_paras(story, [
        "IS63WV1288是异步SRAM，没有SCLK输入，读写靠地址线、数据线和CE/OE/WE控制。写操作时先给出稳定地址和数据，再拉低CE和WE，保持足够写脉宽后释放WE；读操作时先给出地址并拉低CE/OE，等待访问时间后再采样数据总线。",
        "地址建立时间表示控制信号有效前地址必须提前稳定多久，保持时间表示控制信号释放后地址还要继续保持多久。FPGA里通常用状态机把一次访问拆成SETUP、ACCESS、HOLD几个时钟周期，即使板卡和芯片速度足够快，也不要把地址、WE和数据在同一个组合表达式里瞬间改变。"
    ], st)
    story.append(Paragraph("DS1302 RTC", st['sub_title']))
    add_paras(story, [
        "DS1302保存秒、分、时、日、月、星期、年等BCD寄存器。BCD不是普通二进制，例如十进制59表示为0x59，高4位是十位5，低4位是个位9。读出时间后，如果要显示到数码管，BCD格式反而很方便；如果要做加减运算，则应先转成普通二进制。",
        "DS1302通信使用CE、SCLK、DATA三线。CE拉高后开始传输命令字，命令最低位决定读写方向，地址位选择寄存器。它也支持突发读写：先发送burst命令，然后连续读出或写入多个时间寄存器，减少重复片选和命令开销。上电后要注意秒寄存器最高位CH，CH=1表示时钟暂停，需要清零才能让晶振运行。"
    ], st)
    story.append(Paragraph("W25Q128 Flash", st['sub_title']))
    add_paras(story, [
        "W25Q128是128Mbit SPI NOR Flash，容量为16MByte。它的擦除粒度通常大于写入粒度：可以按页编程，一页常见为256字节；但擦除必须按扇区或块进行，常用4KB扇区擦除。Flash只能把1写成0，不能直接把0写回1，所以写入前若目标区域不是全0xFF，必须先擦除。",
        "常用命令包括0x9F读JEDEC ID、0x06写使能、0x05读状态寄存器、0x03读数据、0x02页编程、0x20扇区擦除。页编程和擦除都是内部耗时操作，发完命令不能立刻认为完成，必须轮询状态寄存器WIP位，直到WIP=0再进行下一次访问。"
    ], st)

    story.append(ChapterMarker("ch3_4", chapter_pages))
    story.append(Paragraph("3.4  第16届蓝桥杯FPGA国赛算法拆解", st['sec_title']))
    story.append(Paragraph("基于FPGA设计动态数据采集系统：ADC产生128个数字量，按键触发录入，集成极值统计、"
                           "无损压缩、滑动平均滤波、归一化四种算法，数码管显示结果，串口上报数据。", st['body']))
    add_paras(story, [
        "这类综合题不要先写顶层，而要先把系统分成“采集、存储、计算、显示、上报”五个可验证模块。ADC模块持续刷新当前电压对应的0到127数字量；S1只在按键脉冲到来时把当前ADC值写入数组，同时记录RTC时间戳；S2只改变当前算法编号；S4触发计算状态机；S3根据当前界面选择串口上报或结果翻页。",
        "数据量至少16个，题目又要求支持128个数字量范围，所以存储宽度可按7位或8位设计。为了简化串口格式化，内部通常用8位保存采样值，用额外计数器保存已录入数量。算法计算不要在一个时钟里写完所有循环，应该设计为多拍扫描状态机：每个时钟处理一个元素，处理完后置done标志。"
    ], st)

    for name, desc, example, method in [
        ("极值统计", "统计最小值和最大值及其出现次数",
         "[62,88,88,99,99,9,8,88] → MIN=(8,6), MAX=(99,3)",
         "遍历数组，两个寄存器记录当前最小/最大值，计数器记录次数。O(n)时间复杂度。"),
        ("无损压缩(游程编码)", "对连续重复数据进行RLE压缩",
         "[88,88,88,99,99,9,8,88] → (88,3),(99,2),9,8,88",
         "顺序扫描，当前值与前值相同则计数+1，不同则输出(值,计数)对。游程≥2输出对，否则直接输出值。"),
        ("滑动平均滤波", "窗口=3的滑动平均，保留整数",
         "[62,88,88,99,99,9,8,88] → [79,91,95,69,38,35]",
         "对每个位置i(1~N-2)，取(data[i-1]+data[i]+data[i+1])/3取整。输出长度=N-2。"),
        ("最大-最小归一化", "归一化到[0,1]，保留2位小数",
         "[127,8,10,2,8] → [1.00,0.05,0.06,0.00,0.05]",
         "公式：(value-min)/(max-min)。定点数实现：先×100再÷(max-min)。注意max==min时除零保护。"),
    ]:
        story.append(Paragraph(f"① {name}" if name == "极值统计" else
                               f"② {name}" if "无损" in name else
                               f"③ {name}" if "滑动" in name else f"④ {name}", st['sub_title']))
        story.append(Paragraph(f"<b>功能：</b>{desc}", st['body']))
        story.append(Paragraph(f"<b>示例：</b>{example}", st['body']))
        story.append(Paragraph(f"<b>实现：</b>{method}", st['comment']))

    story.append(Paragraph("串口通信格式", st['sub_title']))
    story.append(Paragraph("115200/8N1，字符串格式输出。", st['body']))
    story.append(Paragraph("录入上报：[时间戳][数值][时间戳][数值]...", st['body']))
    story.append(Paragraph("算法上报：[时间戳][A1/A2/A3/A4][结果数据]", st['body']))

    story.append(ChapterMarker("ch3_5", chapter_pages))
    story.append(Paragraph("3.5  全部真题与模拟题题面", st['sec_title']))
    add_paras(story, [
        "本节把已提取的扫描题面逐页嵌入教材，便于离线复习和对照训练。扫描页主要来自四梯练习系统的个人练习结果解析，题型以客观选择题为主，覆盖FPGA基础、Verilog语法、组合/时序逻辑、复位、PLL、计数器、通信协议和外设应用。由于这些PDF没有可抽取文字层，本版采用原图保真嵌入，后续迭代会继续补充人工文字化解析。",
        "使用方法：先遮住正确答案独立作答，再对照页内答案；错题不要只记选项，要回到本章前面的协议、状态机和时序原理重新解释一遍。能够用自己的话解释错误原因，比单纯记住答案更接近赛场可迁移能力。"
    ], st)
    summaries = {
        "第十六届 蓝桥杯（电子类）FPGA设计与开发省赛真题": "省赛真题客观题，重点覆盖逻辑门、D触发器、PLL、Verilog语法、FPGA资源和基础时序概念。",
        "十六届蓝桥杯FPGA模拟试题I": "模拟试题I，重点覆盖FPGA与ASIC区别、Verilog寄存器声明、组合逻辑、基础时序和常用接口概念。",
        "十六届蓝桥杯FPGA模拟试题Ⅱ": "模拟试题II，重点覆盖数字逻辑、Verilog表达式、时钟复位、存储器和通信协议基础。",
        "十六届蓝桥杯FPGA模拟试题Ⅲ": "模拟试题III，重点覆盖FPGA工程流程、时序约束、状态机、串口/I2C/SPI和板载外设理解。",
        "第十七届FPGA模拟考试Ⅰ": "第17届模拟考试I，重点覆盖同步复位、FPGA可重构优势、有符号位宽、Verilog always敏感列表和协议选择。",
        "第十七届FPGA模拟考试Ⅱ": "第17届模拟考试II，重点覆盖Verilog综合语义、时钟域处理、外设控制、数码管显示和常见赛题知识点。",
    }
    groups = exam_image_groups(base_dir) if base_dir else []
    if not groups:
        story.append(Paragraph("未找到 extracted_images 目录，跳过扫描题面嵌入。", st['tip']))
    for exam_name, pages in groups:
        story.append(PageBreak())
        story.append(Paragraph(safe_xml(exam_name), st['sec_title']))
        story.append(Paragraph(summaries.get(exam_name, "扫描题面页。"), st['desc_box']))
        for idx, img_path in enumerate(pages, 1):
            story.append(Paragraph(f"题面页 {idx}/{len(pages)}", st['sub_title']))
            add_exam_image(story, img_path, st)
            if idx != len(pages):
                story.append(PageBreak())
    story.append(PageBreak())
    return story

# ==================== 模块代码章节 ====================
def build_code_chapter(title, files, ch_num, st):
    story = []
    key = f"ch{ch_num}"
    story.append(ChapterMarker(key, chapter_pages))
    story.append(Paragraph(title, st['ch_title']))
    story.append(DecorLine())
    story.append(Spacer(1, 3*mm))

    for idx, (fname, content) in enumerate(files, 1):
        sub_key = f"ch{ch_num}_{idx}"
        story.append(ChapterMarker(sub_key, chapter_pages))
        story.append(Paragraph(f"{ch_num}.{idx}  {fname}", st['file_title']))
        story.append(Paragraph(f"<b>功能：</b>{get_module_desc(fname)}", st['desc_box']))
        usage = get_usage_info(fname)
        if usage:
            story.append(Paragraph(usage, st['comment']))
        story.extend(build_annotated_code(fname, content, st))
        story.append(Spacer(1, 3*mm))

    story.append(PageBreak())
    return story

# ==================== 附录 ====================
def build_appendix(st):
    story = []
    story.append(ChapterMarker("appendix", chapter_pages))
    story.append(Paragraph("附    录", ParagraphStyle('AT', fontName='SimHei', fontSize=22, alignment=TA_CENTER,
                                                      textColor=C['primary'], spaceBefore=1.5*cm, spaceAfter=8*mm)))
    story.append(DecorLine(color=C['secondary'], thickness=2))
    story.append(Spacer(1, 5*mm))

    def th(t): return Paragraph(t, st['th'])
    def td(t): return Paragraph(t, st['td'])

    story.append(Paragraph("A. DS1302寄存器地址表", st['sec_title']))
    ds = [
        [th("寄存器"), th("写地址"), th("读地址"), th("数据范围")],
        [td("秒"), td("0x80"), td("0x81"), td("00-59, bit7=CH暂停位")],
        [td("分"), td("0x82"), td("0x83"), td("00-59")],
        [td("时"), td("0x84"), td("0x85"), td("00-23(24h制)")],
        [td("日"), td("0x86"), td("0x87"), td("01-31")],
        [td("月"), td("0x88"), td("0x89"), td("01-12")],
        [td("星期"), td("0x8A"), td("0x8B"), td("01-07")],
        [td("年"), td("0x8C"), td("0x8D"), td("00-99")],
        [td("写保护"), td("0x8E"), td("0x8F"), td("bit7=WP, 0=可写")],
    ]
    t = Table(ds, colWidths=[2.5*cm, 2*cm, 2*cm, 5.5*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C['primary']),
        ('GRID', (0,0), (-1,-1), 0.5, C['border']),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [white, C['card_bg']]),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'), ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3), ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t)
    story.append(Spacer(1, 5*mm))

    story.append(Paragraph("B. W25Q128 SPI命令表", st['sec_title']))
    fl = [
        [th("命令"), th("功能"), th("格式")],
        [td("0x06"), td("Write Enable (WREN)"), td("1字节命令")],
        [td("0x05"), td("Read Status Register"), td("命令+1字节返回")],
        [td("0x03"), td("Read Data"), td("命令+3字节地址+N字节返回")],
        [td("0x02"), td("Page Program (Write)"), td("命令+3字节地址+N字节数据")],
        [td("0x20"), td("Sector Erase (4KB)"), td("命令+3字节地址")],
        [td("0x9F"), td("Read JEDEC ID"), td("命令+3字节返回")],
    ]
    t = Table(fl, colWidths=[2*cm, 4*cm, 6*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C['primary']),
        ('GRID', (0,0), (-1,-1), 0.5, C['border']),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [white, C['card_bg']]),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'), ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3), ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t)

    story.append(Spacer(1, 2*cm))
    story.append(DecorLine(color=C['muted'], thickness=0.5))
    story.append(Paragraph("© 2026 极道工作室 · JIDAO STUDIO · 版权所有", ParagraphStyle('CR', fontName='MSYH', fontSize=9, alignment=TA_CENTER, textColor=C['muted'])))
    return story

# ==================== 主函数 ====================
def main():
    register_fonts()
    st = S()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(script_dir)
    driver_files = read_verilog(os.path.join(base_dir, "driver"))
    user_files = read_verilog(os.path.join(base_dir, "user"))
    results_dir = os.path.join(base_dir, "results")
    os.makedirs(results_dir, exist_ok=True)

    output_path = os.path.join(results_dir, "蓝桥杯FPGA开发教程_详细注释版.pdf")

    # ========== 第一遍：生成正文，记录页码 ==========
    # 先生成不含目录的完整内容
    content_story = []
    content_story.extend(build_cover(st))
    # 目录占位（用于让第一遍页码与最终版一致）
    content_story.extend(build_toc(st))
    content_story.extend(build_chapter1(st))
    content_story.extend(build_chapter2(st))
    content_story.extend(build_chapter3(st, base_dir))
    content_story.extend(build_code_chapter("第四章  Driver 驱动模块详解", driver_files, 4, st))
    content_story.extend(build_code_chapter("第五章  User 应用模块详解", user_files, 5, st))
    content_story.extend(build_appendix(st))

    # 第一遍构建，记录页码
    doc1 = SimpleDocTemplate(output_path + ".tmp", pagesize=A4,
                             leftMargin=1.5*cm, rightMargin=1.5*cm,
                             topMargin=2*cm, bottomMargin=2.5*cm)
    doc1.build(list(content_story), onFirstPage=cover_header_footer, onLaterPages=header_footer)
    print(f"Pass 1 done, page map: {chapter_pages}")

    # ========== 第二遍：带页码的目录 + 正文 ==========
    final_story = []
    final_story.extend(build_cover(st))
    final_story.extend(build_toc(st))
    final_story.extend(build_chapter1(st))
    final_story.extend(build_chapter2(st))
    final_story.extend(build_chapter3(st, base_dir))
    final_story.extend(build_code_chapter("第四章  Driver 驱动模块详解", driver_files, 4, st))
    final_story.extend(build_code_chapter("第五章  User 应用模块详解", user_files, 5, st))
    final_story.extend(build_appendix(st))

    doc2 = SimpleDocTemplate(output_path, pagesize=A4,
                             leftMargin=1.5*cm, rightMargin=1.5*cm,
                             topMargin=2*cm, bottomMargin=2.5*cm)
    doc2.build(final_story, onFirstPage=cover_header_footer, onLaterPages=header_footer)

    # 清理临时文件
    try: os.remove(output_path + ".tmp")
    except: pass

    print(f"PDF generated: {output_path}")

if __name__ == "__main__":
    main()
