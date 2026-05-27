#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成包含driver和user文件夹中所有Verilog代码的PDF文档
"""

import os
import subprocess
import sys

def read_verilog_files(folder_path):
    """读取指定文件夹中的所有Verilog文件"""
    verilog_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.v'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                verilog_files.append((file, content))
    return verilog_files

def generate_latex_content(driver_files, user_files):
    """生成LaTeX文档内容"""
    latex_content = r"""
\documentclass[a4paper,10pt]{article}
\usepackage[UTF8]{ctex}
\usepackage{listings}
\usepackage{xcolor}
\usepackage{geometry}
\usepackage{fancyhdr}
\usepackage{titlesec}
\usepackage{hyperref}

% 设置页面边距
\geometry{left=1.5cm,right=1.5cm,top=2cm,bottom=2cm}

% 设置代码样式
\lstset{
    language=Verilog,
    basicstyle=\ttfamily\small,
    keywordstyle=\color{blue}\bfseries,
    commentstyle=\color{green!60!black},
    stringstyle=\color{red},
    numberstyle=\tiny\color{gray},
    numbers=left,
    numbersep=5pt,
    frame=single,
    breaklines=true,
    breakatwhitespace=true,
    tabsize=4,
    showstringspaces=false,
    captionpos=b
}

% 设置页眉页脚
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{FPGA Verilog 代码参考手册}
\fancyhead[R]{\thepage}
\fancyfoot[C]{比赛快速查阅版}

% 设置标题格式
\titleformat{\section}{\Large\bfseries}{\thesection}{1em}{}
\titleformat{\subsection}{\large\bfseries}{\thesubsection}{1em}{}

\begin{document}

% 封面
\begin{titlepage}
\begin{center}
\vspace*{2cm}
{\Huge\bfseries FPGA Verilog 代码参考手册}\\[1cm]
{\Large 比赛快速查阅版}\\[2cm]
{\large 包含 driver 和 user 文件夹中的所有代码}\\[1cm]
{\large 生成日期：\today}\\[3cm]
{\large 项目：LQBFPGA 模拟测试}
\end{center}
\end{titlepage}

% 目录
\tableofcontents
\newpage

% driver 文件夹代码
\section{Driver 文件夹代码}
"""

    # 添加driver文件夹中的文件
    for i, (filename, content) in enumerate(driver_files, 1):
        latex_content += f"""
\\subsection{{{filename}}}
\\begin{{lstlisting}}[caption={filename}]
{content}
\\end{{lstlisting}}
"""

    # 添加user文件夹代码
    latex_content += r"""
\section{User 文件夹代码}
"""

    # 添加user文件夹中的文件
    for i, (filename, content) in enumerate(user_files, 1):
        latex_content += f"""
\\subsection{{{filename}}}
\\begin{{lstlisting}}[caption={filename}]
{content}
\\end{{lstlisting}}
"""

    latex_content += r"""
\end{document}
"""
    return latex_content

def main():
    # 获取当前脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(script_dir)  # 上一级目录

    # 读取driver和user文件夹中的文件
    driver_path = os.path.join(base_dir, "driver")
    user_path = os.path.join(base_dir, "user")

    print(f"正在读取 driver 文件夹: {driver_path}")
    driver_files = read_verilog_files(driver_path)
    print(f"找到 {len(driver_files)} 个 Verilog 文件")

    print(f"正在读取 user 文件夹: {user_path}")
    user_files = read_verilog_files(user_path)
    print(f"找到 {len(user_files)} 个 Verilog 文件")

    # 生成LaTeX内容
    latex_content = generate_latex_content(driver_files, user_files)

    # 保存LaTeX文件
    results_dir = os.path.join(base_dir, "results")
    os.makedirs(results_dir, exist_ok=True)

    latex_file = os.path.join(results_dir, "verilog_code_reference.tex")
    with open(latex_file, 'w', encoding='utf-8') as f:
        f.write(latex_content)

    print(f"LaTeX 文件已生成: {latex_file}")

    # 尝试编译PDF
    try:
        # 检查是否安装了pdflatex
        subprocess.run(["pdflatex", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # 编译PDF
        print("正在编译PDF...")
        result = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "verilog_code_reference.tex"],
            cwd=results_dir,
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print("PDF 编译成功！")
            pdf_file = os.path.join(results_dir, "verilog_code_reference.pdf")
            print(f"PDF 文件位置: {pdf_file}")
        else:
            print("PDF 编译失败，尝试使用xelatex...")
            # 尝试使用xelatex
            result = subprocess.run(
                ["xelatex", "-interaction=nonstopmode", "verilog_code_reference.tex"],
                cwd=results_dir,
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print("PDF 编译成功（使用xelatex）！")
                pdf_file = os.path.join(results_dir, "verilog_code_reference.pdf")
                print(f"PDF 文件位置: {pdf_file}")
            else:
                print("PDF 编译失败，请手动编译LaTeX文件")
                print("错误信息:")
                print(result.stderr)
    except FileNotFoundError:
        print("未找到pdflatex或xelatex，请安装TeX发行版（如TeX Live或MiKTeX）")
        print("或者手动编译生成的LaTeX文件")

if __name__ == "__main__":
    main()