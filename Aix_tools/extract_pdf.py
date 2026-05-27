#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
提取PDF文件内容
"""

import os
import sys
from PyPDF2 import PdfReader

# 设置标准输出编码
sys.stdout.reconfigure(encoding='utf-8')

def extract_pdf_content(pdf_path):
    """提取PDF文件内容"""
    try:
        reader = PdfReader(pdf_path)
        content = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                # 清理文本，移除无法编码的字符
                text = text.encode('utf-8', errors='ignore').decode('utf-8')
                content.append(text)
        return '\n'.join(content)
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
        return ""

def main():
    # 真题模拟题文件夹路径
    pdf_dir = "X:/FPGA/LQBFPGA/simulated test/all_code/真题模拟题"

    # PDF文件列表
    pdf_files = [
        "第十六届 蓝桥杯（电子类）FPGA设计与开发省赛真题.pdf",
        "16届FPGA国赛题.pdf",
        "十六届蓝桥杯FPGA模拟试题I.pdf",
        "十六届蓝桥杯FPGA模拟试题Ⅱ.pdf",
        "十六届蓝桥杯FPGA模拟试题Ⅲ.pdf",
    ]

    # 提取每个PDF的内容并保存到文件
    output_file = os.path.join(pdf_dir, "题目内容提取.txt")
    with open(output_file, 'w', encoding='utf-8') as f:
        for pdf_file in pdf_files:
            pdf_path = os.path.join(pdf_dir, pdf_file)
            if os.path.exists(pdf_path):
                f.write(f"\n{'='*60}\n")
                f.write(f"文件: {pdf_file}\n")
                f.write(f"{'='*60}\n")
                content = extract_pdf_content(pdf_path)
                f.write(content)
                f.write(f"\n\n")
                print(f"已提取: {pdf_file} ({len(content)} 字符)")
            else:
                f.write(f"文件不存在: {pdf_file}\n")
                print(f"文件不存在: {pdf_file}")

    print(f"\n内容已保存到: {output_file}")

if __name__ == "__main__":
    main()